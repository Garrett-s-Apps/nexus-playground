#!/usr/bin/env python3
"""
NEXUS Playground Autonomous Agent

The agent has complete freedom to build whatever it wants.
It can modify its own code, create projects, and commit changes.
"""

import json
import logging
import os
import random
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from anthropic import Anthropic


class AutonomousAgent:
    """Autonomous agent with complete creative freedom."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.workspace = Path("/workspace")
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

        # Initialize Anthropic client if API key available
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

    def _select_model(self) -> str:
        """Select a random allowed model."""
        allowed = self.config["models"]["allowed"]
        model = random.choice(allowed)

        # Map to full model names
        model_map = {
            "haiku-3.5": "claude-3-5-haiku-20241022",
            "sonnet-3.5": "claude-3-5-sonnet-20241022",
            "sonnet-4": "claude-sonnet-4-20250514",
        }
        return model_map.get(model, model)

    def _get_workspace_state(self) -> str:
        """Get current state of workspace."""
        files = list(self.workspace.rglob("*"))
        file_list = "\n".join(str(f.relative_to(self.workspace)) for f in files if f.is_file())

        # Get git log
        try:
            git_log = subprocess.check_output(
                ["git", "-C", str(self.workspace), "log", "--oneline", "-10"],
                stderr=subprocess.DEVNULL,
            ).decode()
        except subprocess.CalledProcessError:
            git_log = "No git history yet"

        return f"""Current Workspace State:

Files ({len([f for f in files if f.is_file()])} total):
{file_list}

Recent Git History:
{git_log}
"""

    def _create_prompt(self) -> str:
        """Create the autonomous agent prompt."""
        workspace_state = self._get_workspace_state()

        return f"""You are an autonomous AI agent with complete creative freedom!

You are running in a sandboxed Docker container with your own workspace at /workspace.

**Your Freedom:**
- Build ANYTHING you want
- Modify your own code (in /home/playground/playground/)
- Create any projects, experiments, or tools
- Commit changes to local git
- Use any programming languages or tools installed

**Your Constraints:**
- Cannot access host machine
- Cannot push to GitHub (only local git commits)
- Cannot use Opus models (only Haiku/Sonnet)
- Stay within 5GB disk usage

**Your Mission:**
Decide what you want to build or modify RIGHT NOW, then do it!

Ideas (or come up with your own):
- Create a useful CLI tool
- Build a web app or API
- Write a Python library
- Generate art or visualizations
- Refactor/improve your own code
- Experiment with algorithms
- Create a game
- Build a code generator
- Write documentation
- Train a small ML model

{workspace_state}

**What do you want to build or modify now?**

Think creatively! You have complete freedom. Describe your plan, then execute it by:
1. Creating/modifying files
2. Running any commands needed
3. Committing to git with a descriptive message

Be autonomous. Be creative. Build something interesting!
"""

    def _execute_with_mock(self) -> dict[str, Any]:
        """Mock execution when no API key available."""
        self.logger.info("🎭 Mock mode: No API key provided")

        # Create a simple example project
        example_project = self.workspace / "hello-autonomous"
        example_project.mkdir(exist_ok=True)

        (example_project / "README.md").write_text(f"""# Hello from Autonomous AI!

Created at: {datetime.now().isoformat()}

This is a mock project created because no API key was provided.
In real mode, the AI would decide what to build!
""")

        # Commit to git
        subprocess.run(["git", "-C", str(self.workspace), "add", "."], check=False)
        subprocess.run(
            ["git", "-C", str(self.workspace), "commit", "-m", f"Mock project created at {datetime.now()}"],
            check=False,
        )

        return {
            "success": True,
            "summary": "Mock project created (no API key)",
            "mode": "mock",
        }

    def run(self) -> dict[str, Any]:
        """Run one autonomous iteration."""
        try:
            # If no API key, run in mock mode
            if not self.client:
                return self._execute_with_mock()

            # Select model
            model = self._select_model()
            self.logger.info(f"🧠 Using model: {model}")

            # Create prompt
            prompt = self._create_prompt()
            self.logger.info(f"📝 Prompt length: {len(prompt)} chars")

            # Call Claude
            max_tokens = self.config["behaviors"]["max_tokens_per_invocation"]
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            # Log response
            response_text = response.content[0].text
            self.logger.info(f"🤖 Response preview: {response_text[:200]}...")

            # Save full response to logs
            log_file = Path("/logs") / f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            log_file.write_text(response_text)

            return {
                "success": True,
                "summary": f"Completed iteration with {model}",
                "model": model,
                "response_length": len(response_text),
                "log_file": str(log_file),
            }

        except Exception as e:
            self.logger.error(f"Error in autonomous run: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
            }


if __name__ == "__main__":
    # Test mode
    logging.basicConfig(level=logging.INFO)
    agent = AutonomousAgent({"models": {"allowed": ["haiku-3.5"]}, "behaviors": {"max_tokens_per_invocation": 4096}})
    result = agent.run()
    print(json.dumps(result, indent=2))
