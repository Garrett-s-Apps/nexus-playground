#!/usr/bin/env python3
"""
NEXUS Playground Supervisor

Ensures the autopilot agent runs continuously with <5 minute gaps.
Monitors health, manages errors, and enforces safety limits.
"""

import logging
import random
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
                    self.logger.info(f"✅ Success: {result.get('summary', 'No summary')}")
                    self.consecutive_errors = 0
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

            # Sleep before next iteration
            sleep_time = self._get_sleep_interval()
            self.logger.info(f"😴 Sleeping for {sleep_time}s until next iteration...")
            time.sleep(sleep_time)

        self.logger.info("👋 Supervisor shutting down.")


if __name__ == "__main__":
    supervisor = PlaygroundSupervisor()
    supervisor.run()
