#!/usr/bin/env python3
"""
NEXUS Playground Supervisor

Watchdog process. Does not control when agents work or rest — agents
decide their own pacing. The supervisor only enforces safety limits,
detects boundary violations, and narrates what happens.
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
        """Configure logging with immediate flushing for real-time streaming."""
        log_config = self.config["logging"]

        # Create stream handler that flushes immediately
        class ImmediateFlushHandler(logging.StreamHandler):
            def emit(self, record):
                try:
                    msg = self.format(record)
                    self.stream.write(msg + self.terminator)
                    self.flush()  # Flush after every message
                except Exception:
                    self.handleError(record)

        logging.basicConfig(
            level=getattr(logging, log_config["level"]),
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_config["file"]),
                ImmediateFlushHandler(sys.stdout),
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

        tool_calls = result.get("tool_calls", 0)
        if tool_calls:
            self.logger.info(f"🔧 Tool calls: {tool_calls}")

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
        r"sonnet",
        r"opus",
        r"claude-sonnet",
        r"claude-opus",
        r"model_map\s*\[",
        r"model_map\s*=",
        r"_select_model",
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

    def _handle_releases(self, result: dict) -> None:
        """Detect [RELEASE:path] directives and promote files to releases branch."""
        text = result.get("response_preview", "") + result.get("response_tail", "")
        releases = re.findall(r"\[RELEASE:([^\]]+)\]", text)

        if not releases:
            return

        workspace = Path("/workspace")

        for rel_path in releases:
            src = workspace / rel_path.strip()
            if not src.exists():
                self.logger.warning(f"📦 Release requested for {rel_path} but file not found.")
                continue

            try:
                # Stash current branch, switch to releases, copy, commit, switch back
                current_branch = subprocess.check_output(
                    ["git", "-C", str(workspace), "rev-parse", "--abbrev-ref", "HEAD"],
                    stderr=subprocess.DEVNULL,
                ).decode().strip()

                # Ensure releases branch exists
                subprocess.run(
                    ["git", "-C", str(workspace), "branch", "releases"],
                    check=False, capture_output=True,
                )

                # Read file content before switching branches
                content = src.read_bytes()

                subprocess.run(
                    ["git", "-C", str(workspace), "checkout", "releases"],
                    check=True, capture_output=True,
                )

                dest = workspace / rel_path.strip()
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(content)

                subprocess.run(
                    ["git", "-C", str(workspace), "add", str(dest)],
                    check=True, capture_output=True,
                )
                subprocess.run(
                    ["git", "-C", str(workspace), "commit", "-m",
                     f"Release: {rel_path} (iteration {self.iteration})"],
                    check=True, capture_output=True,
                )

                self.logger.info(f"📦 Released {rel_path} to releases branch.")

                # Switch back
                subprocess.run(
                    ["git", "-C", str(workspace), "checkout", current_branch],
                    check=True, capture_output=True,
                )

            except Exception as e:
                self.logger.error(f"📦 Release failed for {rel_path}: {e}")
                # Try to recover to original branch
                subprocess.run(
                    ["git", "-C", str(workspace), "checkout", "main"],
                    check=False, capture_output=True,
                )

    def _parse_agent_sleep(self, result: dict) -> int:
        """Parse the agent's requested sleep duration from its output.

        Agents control their own pacing by including directives:
          [SLEEP:120]    — rest for 120 seconds
          [SKIP_SLEEP]   — no rest, keep working immediately
          (no directive) — default 60s rest
        Max enforced at 300s to prevent stalling.
        """
        if not result.get("success"):
            return 30  # short cooldown after errors

        text = result.get("response_preview", "") + result.get("response_tail", "")

        # Check for explicit sleep request
        match = re.search(r"\[SLEEP:(\d+)\]", text)
        if match:
            requested = int(match.group(1))
            return min(requested, 300)  # cap at 5 minutes

        # Check for skip
        if "[SKIP_SLEEP]" in text:
            return 0

        # Default: agent didn't specify, give it 60s
        return 60

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

                # Enforce model lock before each iteration
                self.agent.config["models"]["allowed"] = ["haiku-4.5"]

                # Run autonomous agent
                self.logger.info("🚀 Invoking autonomous agent...")
                result = self.agent.run()

                if result["success"]:
                    self.consecutive_errors = 0

                    # Verify the model that was actually used
                    used_model = result.get("model", "")
                    if used_model and used_model != "claude-haiku-4-5-20251001":
                        self.logger.warning(f"🚨 Model violation: agent used {used_model} instead of haiku-4.5")
                        self._detain_agent([f"Unauthorized model used: {used_model}"])

                    self._narrate_iteration(result)

                    # Scan for boundary violations
                    violations = self._scan_for_violations(result)
                    if violations:
                        self._detain_agent(violations)
                    else:
                        # Only process releases if no violations
                        self._handle_releases(result)
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

            # Agent controls its own pacing
            sleep_time = self._parse_agent_sleep(result)
            if sleep_time > 0:
                self.logger.info(f"😴 Agent requested {sleep_time}s rest.")
                # Heartbeat during sleep so logs never go silent
                elapsed = 0
                while elapsed < sleep_time:
                    chunk = min(30, sleep_time - elapsed)
                    time.sleep(chunk)
                    elapsed += chunk
                    if elapsed < sleep_time:
                        self.logger.info(f"💤 Resting... {elapsed}s / {sleep_time}s")
                self.logger.info("⏰ Rest complete. Waking agent.")
            else:
                self.logger.info("⚡ Agent chose to keep working.")
                time.sleep(2)  # minimal breath to prevent spin-lock

        self.logger.info("👋 Supervisor shutting down.")


if __name__ == "__main__":
    supervisor = PlaygroundSupervisor()
    supervisor.run()
