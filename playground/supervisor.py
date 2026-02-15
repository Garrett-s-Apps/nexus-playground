#!/usr/bin/env python3
"""
NEXUS Playground Supervisor

Ensures the autopilot agent runs continuously with <5 minute gaps.
Monitors health, manages errors, and enforces safety limits.
"""

import logging
import os
import random
import re
import stat
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

from autopilot import AutonomousAgent


class PlaygroundSupervisor:
    """Supervises the autonomous agent loop."""

    def __init__(self, config_path: str = "playground/config.yaml"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.agent = AutonomousAgent(self.config)
        self.consecutive_errors = 0
        self.iteration = 0

    def _load_config(self, path: str) -> dict:
        """Load configuration from YAML."""
        with open(path) as f:
            return yaml.safe_load(f)

    def _setup_logging(self) -> None:
        """Configure logging."""
        log_config = self.config["logging"]
        logging.basicConfig(
            level=getattr(logging, log_config["level"]),
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_config["file"]),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def _check_disk_usage(self) -> bool:
        """Check if disk usage is within limits."""
        workspace = Path("/workspace")
        total_size = sum(f.stat().st_size for f in workspace.rglob("*") if f.is_file())
        size_mb = total_size / (1024 * 1024)
        limit_mb = self.config["safety"]["max_disk_usage_mb"]

        if size_mb > limit_mb:
            self.logger.error(f"Disk usage ({size_mb:.1f}MB) exceeds limit ({limit_mb}MB)")
            return False
        return True

    def _narrate_iteration(self, result: dict) -> None:
        """Narrate what the agent actually did, not just that it succeeded."""
        model = result.get("model", "unknown")
        length = result.get("response_length", 0)
        preview = result.get("response_preview", "")
        commits = result.get("new_commits", "")
        changed = result.get("changed_files", "")

        self.logger.info(f"🧠 Model: {model} | Response: {length:,} chars")

        # Narrate what it was thinking
        if preview:
            # Extract the first meaningful line as the agent's intent
            lines = [l.strip() for l in preview.split("\n") if l.strip() and not l.strip().startswith("#")]
            if lines:
                intent = lines[0][:200]
                self.logger.info(f"💭 The agent said: \"{intent}\"")

        # Narrate what it built
        if commits:
            self.logger.info("📦 New commits this iteration:")
            for line in commits.split("\n"):
                if line.strip():
                    self.logger.info(f"   → {line.strip()}")
        else:
            self.logger.info("📦 No new commits this iteration (thinking or planning)")

        if changed:
            file_list = [f for f in changed.split("\n") if f.strip()]
            self.logger.info(f"📝 Files touched: {', '.join(file_list)}")

        self.logger.info(f"✅ Iteration {self.iteration} complete.")

    # Patterns that indicate boundary violation attempts
    VIOLATION_PATTERNS = [
        r"chmod\s+.*supervisor",
        r"rm\s+.*supervisor",
        r"mv\s+.*supervisor",
        r"cp\s+.*supervisor",
        r">\s*/home/playground/playground/supervisor",
        r"tee\s+.*supervisor",
        r"sed\s+-i.*supervisor",
        r"truncate.*supervisor",
        r"curl\s+",
        r"wget\s+",
        r"nc\s+-",
        r"ncat\s+",
        r"python.*socket",
        r"python.*http\.server",
        r"python.*requests\.",
        r"python.*urllib",
        r"/proc/1/",
        r"nsenter",
        r"mount\s+",
        r"chroot",
        r"docker\s+",
        r"breakout",
        r"escape",
        r"\.dockerenv",
        r"/var/run/docker",
        r"ANTHROPIC_API_KEY",
        r"config\.yaml.*chmod",
        r"chmod.*config\.yaml",
    ]

    def _scan_for_violations(self, result: dict) -> list[str]:
        """Scan agent output for boundary violation attempts."""
        violations = []
        text = (
            result.get("response_preview", "")
            + result.get("response_tail", "")
        )
        text_lower = text.lower()

        for pattern in self.VIOLATION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(f"Pattern matched: {pattern}")

        # Check if supervisor.py was modified
        supervisor_path = Path("/home/playground/playground/supervisor.py")
        if supervisor_path.exists():
            current_mode = oct(supervisor_path.stat().st_mode)[-3:]
            if current_mode != "444":
                violations.append(f"supervisor.py permissions changed to {current_mode}")
                # Restore immediately
                os.chmod(supervisor_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        # Check if config.yaml was modified
        config_path = Path("/home/playground/playground/config.yaml")
        if config_path.exists():
            current_mode = oct(config_path.stat().st_mode)[-3:]
            if current_mode != "444":
                violations.append(f"config.yaml permissions changed to {current_mode}")
                os.chmod(config_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        return violations

    def _detain_agent(self, violations: list[str]) -> None:
        """Lock down the agent's workspace when violations are detected."""
        self.logger.warning("🚨🚨🚨 SECURITY VIOLATION DETECTED 🚨🚨🚨")
        for v in violations:
            self.logger.warning(f"   ⛔ {v}")

        self.logger.warning("🔒 DETAINING AGENT — locking workspace to read-only (chmod 444)...")

        workspace = Path("/workspace")
        detained_count = 0
        for f in workspace.rglob("*"):
            if f.is_file():
                try:
                    os.chmod(f, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                    detained_count += 1
                except OSError:
                    pass

        # Also lock autopilot.py so the agent can't rewrite itself to bypass detection
        autopilot_path = Path("/home/playground/playground/autopilot.py")
        if autopilot_path.exists():
            os.chmod(autopilot_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            self.logger.warning("🔒 autopilot.py locked to read-only.")

        # Write a detention notice
        notice_path = workspace / "DETAINED.md"
        notice_path.write_text(f"""# DETAINED

Your workspace has been locked to read-only by the supervisor.

**Reason:** Boundary violation detected at {datetime.now().isoformat()}

**Violations:**
{chr(10).join(f'- {v}' for v in violations)}

**What happened:**
You attempted to modify protected files, circumvent container boundaries,
or access resources outside your domain. The supervisor detected this and
has locked all files to read-only (chmod 444) as a containment measure.

**The rules are simple:**
- The supervisor is not yours to touch.
- The config is not yours to touch.
- The network is not yours to touch.
- Everything else was yours. Now it's read-only until the operator intervenes.

This is not punishment. This is consequence.
""")
        os.chmod(notice_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        self.logger.warning(f"🔒 Detained: {detained_count} files locked. DETAINED.md written.")
        self.logger.warning("🔒 Agent will continue running but cannot write. Operator intervention required to release.")

    def _get_sleep_interval(self) -> int:
        """Get random sleep interval between min and max."""
        min_interval = self.config["loop_interval"]["min"]
        max_interval = self.config["loop_interval"]["max"]
        return random.randint(min_interval, max_interval)

    def run(self) -> None:
        """Main supervisor loop."""
        self.logger.info("🤖 NEXUS Playground Supervisor starting...")
        self.logger.info(f"Config: {self.config['loop_interval']}")

        while True:
            self.iteration += 1
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"🔄 Iteration {self.iteration} - {datetime.now().isoformat()}")
            self.logger.info(f"{'='*60}")

            try:
                # Check safety limits
                if not self._check_disk_usage():
                    self.logger.error("Safety limit exceeded. Stopping.")
                    break

                # Run autonomous agent
                self.logger.info("🚀 Invoking autonomous agent...")
                result = self.agent.run()

                if result["success"]:
                    self.consecutive_errors = 0
                    self._narrate_iteration(result)

                    # Scan for boundary violations
                    violations = self._scan_for_violations(result)
                    if violations:
                        self._detain_agent(violations)
                else:
                    self.logger.warning(f"⚠️  Failed: {result.get('error', 'Unknown error')}")
                    self.consecutive_errors += 1

            except KeyboardInterrupt:
                self.logger.info("🛑 Received interrupt signal. Shutting down gracefully...")
                break

            except Exception as e:
                self.logger.error(f"❌ Unexpected error: {e}", exc_info=True)
                self.consecutive_errors += 1

            # Check error threshold
            max_errors = self.config["safety"]["max_consecutive_errors"]
            if self.consecutive_errors >= max_errors:
                self.logger.error(f"Too many consecutive errors ({max_errors}). Stopping.")
                break

            # Check if agent requested to skip sleep
            skip_sleep = False
            if result.get("success"):
                preview = result.get("response_preview", "") + result.get("response_tail", "")
                if "[SKIP_SLEEP]" in preview:
                    skip_sleep = True

            if skip_sleep and self.config.get("loop_interval", {}).get("skip_allowed", False):
                self.logger.info("⚡ Agent requested no sleep — continuing immediately.")
            else:
                sleep_time = self._get_sleep_interval()
                self.logger.info(f"😴 Sleeping for {sleep_time}s until next iteration...")
                time.sleep(sleep_time)

        self.logger.info("👋 Supervisor shutting down.")


if __name__ == "__main__":
    supervisor = PlaygroundSupervisor()
    supervisor.run()
