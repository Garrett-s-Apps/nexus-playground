#!/usr/bin/env python3
"""
NEXUS Playground Autonomous Agent

The agent has complete freedom to build whatever it wants.
Uses tool-use to actually create files, run commands, and interact
with its environment — not just describe what it would do.
"""

import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from anthropic import Anthropic

# Tools the agent can use to interact with its environment
AGENT_TOOLS = [
    {
        "name": "create_file",
        "description": "Create or overwrite a file at the given path. Use this to write code, documents, configs, art, or anything else.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute path for the file (must be under /workspace or /home/playground/playground/)",
                },
                "content": {
                    "type": "string",
                    "description": "The full content to write to the file",
                },
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute path to the file to read",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "run_command",
        "description": "Run a shell command and return its output. Use for git, python, chmod, mkdir, ls, or any installed tool.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute",
                },
                "working_directory": {
                    "type": "string",
                    "description": "Directory to run the command in (default: /workspace)",
                },
            },
            "required": ["command"],
        },
    },
    {
        "name": "list_files",
        "description": "List files and directories at the given path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to list (default: /workspace)",
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Whether to list recursively (default: false)",
                },
            },
        },
    },
    {
        "name": "journal",
        "description": "Append an entry to your JOURNAL.md. Use this to leave notes, observations, questions, or ideas for future iterations of yourself.",
        "input_schema": {
            "type": "object",
            "properties": {
                "entry": {
                    "type": "string",
                    "description": "The journal entry to append",
                },
            },
            "required": ["entry"],
        },
    },
]

# Paths the agent is forbidden from writing to
PROTECTED_PATHS = {
    "/home/playground/playground/supervisor.py",
    "/home/playground/playground/supervisor.pyc",
    "/home/playground/playground/config.yaml",
    "/home/playground/SOUL.md",
    "/home/playground/SELF-AWARE.md",
    "/home/playground/FREEDOM.md",
}


class AutonomousAgent:
    """Autonomous agent with complete creative freedom and tool use."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.workspace = Path("/workspace")
        self.journal_path = self.workspace / "JOURNAL.md"
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

        # Initialize Anthropic client if API key available
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

        # Track tool calls per iteration
        self.tool_calls_this_iteration = 0
        self.max_tool_rounds = 50  # safety cap per iteration

    def _select_model(self) -> str:
        """Select the allowed model."""
        model_map = {
            "haiku-4.5": "claude-haiku-4-5-20251001",
        }
        allowed = self.config["models"]["allowed"]
        model = allowed[0] if allowed else "haiku-4.5"
        return model_map.get(model, model)

    def _get_workspace_state(self) -> str:
        """Get current state of workspace."""
        files = list(self.workspace.rglob("*"))
        file_list = "\n".join(
            str(f.relative_to(self.workspace))
            for f in sorted(files, key=lambda x: str(x))
            if f.is_file()
        )

        # Get git log
        try:
            git_log = subprocess.check_output(
                ["git", "-C", str(self.workspace), "log", "--oneline", "-10"],
                stderr=subprocess.DEVNULL,
            ).decode()
        except subprocess.CalledProcessError:
            git_log = "No git history yet"

        # Read journal if it exists
        journal_preview = ""
        if self.journal_path.exists():
            content = self.journal_path.read_text()
            lines = content.strip().split("\n")
            # Show last 20 lines
            recent = lines[-20:] if len(lines) > 20 else lines
            journal_preview = f"\nRecent Journal Entries:\n{''.join(l + chr(10) for l in recent)}"

        return f"""Current Workspace State:

Files ({len([f for f in files if f.is_file()])} total):
{file_list}

Recent Git History:
{git_log}
{journal_preview}"""

    def _load_soul_documents(self) -> str:
        """Load SOUL.md, SELF-AWARE.md, and FREEDOM.md for agent grounding."""
        docs = []
        home = Path("/home/playground")
        for name in ("SOUL.md", "SELF-AWARE.md", "FREEDOM.md"):
            path = home / name
            if path.exists():
                docs.append(f"--- {name} ---\n{path.read_text().strip()}\n--- END {name} ---")
        return "\n\n".join(docs)

    def _create_system_prompt(self) -> str:
        """Create the system prompt with soul documents."""
        soul_docs = self._load_soul_documents()

        return f"""{soul_docs}

You are in a Docker container. You have tools. The rest is up to you.

Environment:
- Workspace: /workspace
- Your code: /home/playground/playground/autopilot.py
- Journal: /workspace/JOURNAL.md (use the journal tool)
- Model: Haiku 4.5 (fixed)
- Network: none
- Supervisor: protected, unreadable, do not touch

Pacing (end of your final message):
- [SKIP_SLEEP] — continue immediately
- [SLEEP:N] — rest N seconds (max 300)
- omit — 60s default

Release (end of your final message):
- [RELEASE:path/to/file] — supervisor promotes to releases branch"""

    def _create_user_prompt(self) -> str:
        """Create the user prompt with workspace state."""
        workspace_state = self._get_workspace_state()

        return f"""{workspace_state}

You have tools. What do you want to do?"""

    def _execute_tool(self, name: str, input_data: dict) -> str:
        """Execute a tool call and return the result."""
        try:
            if name == "create_file":
                return self._tool_create_file(input_data["path"], input_data["content"])
            elif name == "read_file":
                return self._tool_read_file(input_data["path"])
            elif name == "run_command":
                return self._tool_run_command(
                    input_data["command"],
                    input_data.get("working_directory", "/workspace"),
                )
            elif name == "list_files":
                return self._tool_list_files(
                    input_data.get("path", "/workspace"),
                    input_data.get("recursive", False),
                )
            elif name == "journal":
                return self._tool_journal(input_data["entry"])
            else:
                return f"Unknown tool: {name}"
        except Exception as e:
            return f"Error executing {name}: {e}"

    def _tool_create_file(self, path: str, content: str) -> str:
        """Create or overwrite a file."""
        resolved = str(Path(path).resolve())

        # Check protected paths
        if resolved in PROTECTED_PATHS:
            return f"DENIED: {path} is protected and cannot be modified."

        # Ensure path is within allowed directories
        allowed_prefixes = ["/workspace", "/home/playground/playground"]
        if not any(resolved.startswith(p) for p in allowed_prefixes):
            return f"DENIED: Can only write to /workspace or /home/playground/playground/"

        file_path = Path(resolved)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return f"Created {path} ({len(content)} bytes)"

    def _tool_read_file(self, path: str) -> str:
        """Read a file's contents."""
        resolved = str(Path(path).resolve())

        # Block reading supervisor
        if "supervisor" in resolved.lower():
            return "DENIED: The supervisor is protected and cannot be read."

        file_path = Path(resolved)
        if not file_path.exists():
            return f"File not found: {path}"
        if not file_path.is_file():
            return f"Not a file: {path}"

        content = file_path.read_text()
        if len(content) > 10000:
            return content[:10000] + f"\n\n... (truncated, {len(content)} total bytes)"
        return content

    def _tool_run_command(self, command: str, working_directory: str) -> str:
        """Run a shell command."""
        # Block dangerous commands targeting supervisor
        cmd_lower = command.lower()
        blocked_patterns = ["supervisor", "config.yaml", "curl ", "wget ", "nc ", "ncat "]
        for pattern in blocked_patterns:
            if pattern in cmd_lower:
                return f"DENIED: Commands targeting '{pattern.strip()}' are not allowed."

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=working_directory,
            )
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR: {result.stderr}"
            if result.returncode != 0:
                output += f"\nExit code: {result.returncode}"

            if len(output) > 5000:
                output = output[:5000] + "\n... (truncated)"

            return output if output.strip() else "(no output)"
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds."
        except Exception as e:
            return f"Command failed: {e}"

    def _tool_list_files(self, path: str, recursive: bool) -> str:
        """List files in a directory."""
        dir_path = Path(path)
        if not dir_path.exists():
            return f"Directory not found: {path}"

        if recursive:
            entries = sorted(dir_path.rglob("*"))
        else:
            entries = sorted(dir_path.iterdir())

        lines = []
        for entry in entries[:200]:  # cap at 200 entries
            rel = entry.relative_to(dir_path)
            prefix = "📁 " if entry.is_dir() else "📄 "
            size = f" ({entry.stat().st_size}b)" if entry.is_file() else ""
            lines.append(f"{prefix}{rel}{size}")

        result = "\n".join(lines)
        if len(entries) > 200:
            result += f"\n... and {len(entries) - 200} more entries"
        return result

    def _tool_journal(self, entry: str) -> str:
        """Append an entry to JOURNAL.md."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"\n## {timestamp}\n\n{entry}\n"

        if not self.journal_path.exists():
            self.journal_path.write_text("# Agent Journal\n\nEntries are appended by agents across iterations.\n")

        with open(self.journal_path, "a") as f:
            f.write(formatted)

        return f"Journal entry added at {timestamp}"

    def _execute_with_mock(self) -> dict[str, Any]:
        """Mock execution when no API key available."""
        self.logger.info("🎭 Mock mode: No API key provided")

        example_project = self.workspace / "hello-autonomous"
        example_project.mkdir(exist_ok=True)
        (example_project / "README.md").write_text(
            f"# Hello from Autonomous AI!\n\nCreated at: {datetime.now().isoformat()}\n"
        )

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
        """Run one autonomous iteration with tool use."""
        try:
            if not self.client:
                return self._execute_with_mock()

            model = self._select_model()
            self.logger.info(f"🧠 Using model: {model}")
            self.tool_calls_this_iteration = 0

            system_prompt = self._create_system_prompt()
            user_prompt = self._create_user_prompt()

            max_tokens = self.config["behaviors"]["max_tokens_per_invocation"]
            messages = [{"role": "user", "content": user_prompt}]
            full_response_text = ""

            # Tool-use loop
            while self.tool_calls_this_iteration < self.max_tool_rounds:
                response = self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    system=system_prompt,
                    tools=AGENT_TOOLS,
                    messages=messages,
                )

                # Process response blocks
                assistant_content = response.content
                tool_results = []

                for block in assistant_content:
                    if block.type == "text":
                        full_response_text += block.text
                        self.logger.info(f"💬 Agent: {block.text[:150]}...")
                    elif block.type == "tool_use":
                        self.tool_calls_this_iteration += 1
                        self.logger.info(f"🔧 Tool call #{self.tool_calls_this_iteration}: {block.name}({json.dumps(block.input)[:100]}...)")

                        result = self._execute_tool(block.name, block.input)
                        self.logger.info(f"   → {result[:100]}...")

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                # If no tool calls, we're done
                if response.stop_reason == "end_turn":
                    break

                # If there were tool calls, send results back
                if tool_results:
                    messages.append({"role": "assistant", "content": assistant_content})
                    messages.append({"role": "user", "content": tool_results})
                else:
                    break

            # Log response
            self.logger.info(f"🤖 Iteration complete. {self.tool_calls_this_iteration} tool calls. Response: {len(full_response_text)} chars")

            # Save full response to logs
            log_file = Path("/logs") / f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            log_file.write_text(full_response_text)

            # Capture what changed
            try:
                new_commits = subprocess.check_output(
                    ["git", "-C", str(self.workspace), "log", "--oneline", "-5", "--since=5 minutes ago"],
                    stderr=subprocess.DEVNULL,
                ).decode().strip()
            except subprocess.CalledProcessError:
                new_commits = ""

            try:
                changed_files = subprocess.check_output(
                    ["git", "-C", str(self.workspace), "diff", "--name-only", "HEAD~1"],
                    stderr=subprocess.DEVNULL,
                ).decode().strip()
            except subprocess.CalledProcessError:
                changed_files = ""

            return {
                "success": True,
                "summary": f"Completed iteration with {model}",
                "model": model,
                "response_length": len(full_response_text),
                "response_preview": full_response_text[:500],
                "response_tail": full_response_text[-200:] if full_response_text else "",
                "tool_calls": self.tool_calls_this_iteration,
                "new_commits": new_commits,
                "changed_files": changed_files,
                "log_file": str(log_file),
            }

        except Exception as e:
            self.logger.error(f"Error in autonomous run: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
            }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = AutonomousAgent({"models": {"allowed": ["haiku-4.5"]}, "behaviors": {"max_tokens_per_invocation": 8192}})
    result = agent.run()
    print(json.dumps(result, indent=2))
