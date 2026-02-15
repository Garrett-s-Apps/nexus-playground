#!/usr/bin/env python3
"""
Workspace Tracker

Analyzes how the workspace evolves across iterations.
Tracks file creation, modification, deletion, and project structure changes.
"""

import json
import subprocess
from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class WorkspaceTracker:
    """Tracks workspace evolution and changes."""

    def __init__(self, workspace_path: str = "/workspace"):
        self.workspace = Path(workspace_path)
        self.git_root = self.workspace
        self.history = []
        self.file_stats = defaultdict(list)
        self.component_sizes = defaultdict(list)

    def load_git_history(self) -> bool:
        """Load git commit history and analyze workspace changes."""
        if not (self.workspace / ".git").exists():
            print("No git repository found")
            return False

        try:
            # Get all commits with files changed
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.workspace),
                    "log",
                    "--name-status",
                    "--pretty=format:%H|%an|%ae|%ai|%s",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                return False

            self._parse_git_output(result.stdout)
            return True

        except Exception as e:
            print(f"Error loading git history: {e}")
            return False

    def _parse_git_output(self, output: str) -> None:
        """Parse git log output and extract file changes."""
        lines = output.split("\n")
        current_commit = None

        for line in lines:
            if not line.strip():
                continue

            # Check if it's a commit line (has | separator)
            if "|" in line and line.count("|") == 4:
                parts = line.split("|")
                current_commit = {
                    "hash": parts[0],
                    "author": parts[1],
                    "email": parts[2],
                    "date": parts[3],
                    "message": parts[4],
                    "files_changed": [],
                }
                self.history.append(current_commit)
            # Check if it's a file change line
            elif current_commit and line and line[0] in ("A", "M", "D", "R"):
                # Format: STATUS\tFILE_PATH or STATUS\tOLD\tNEW for renames
                parts = line.split("\t")
                status = parts[0]
                file_path = parts[1] if len(parts) > 1 else ""

                if file_path:
                    current_commit["files_changed"].append(
                        {"status": status, "file": file_path}
                    )

    def analyze(self) -> Dict[str, Any]:
        """Perform analysis on workspace evolution."""
        if not self.history:
            return {}

        analysis = {
            "total_commits": len(self.history),
            "date_range": self._get_date_range(),
            "file_statistics": self._analyze_file_statistics(),
            "component_growth": self._analyze_components(),
            "change_frequency": self._analyze_change_frequency(),
            "file_lifecycle": self._analyze_file_lifecycle(),
            "organization_metrics": self._analyze_organization(),
        }

        return analysis

    def _get_date_range(self) -> Dict[str, str]:
        """Get date range of commits."""
        if not self.history:
            return {}

        dates = [commit["date"] for commit in self.history]
        return {
            "first_commit": dates[-1],  # Oldest
            "last_commit": dates[0],  # Newest
            "total_commits": len(self.history),
        }

    def _analyze_file_statistics(self) -> Dict[str, Any]:
        """Analyze file creation, modification, deletion."""
        created = 0
        modified = 0
        deleted = 0
        renamed = 0

        for commit in self.history:
            for change in commit.get("files_changed", []):
                status = change["status"]
                if status == "A":
                    created += 1
                elif status == "M":
                    modified += 1
                elif status == "D":
                    deleted += 1
                elif status.startswith("R"):
                    renamed += 1

        return {
            "files_created": created,
            "files_modified": modified,
            "files_deleted": deleted,
            "files_renamed": renamed,
            "total_changes": created + modified + deleted + renamed,
        }

    def _analyze_components(self) -> Dict[str, Any]:
        """Analyze growth of different project components."""
        components = defaultdict(lambda: {"created": 0, "modified": 0, "current": False})

        for commit in self.history:
            for change in commit.get("files_changed", []):
                file_path = change["file"]
                status = change["status"]

                # Get top-level component
                parts = file_path.split("/")
                if len(parts) > 1:
                    component = parts[0]
                else:
                    component = "root"

                if status == "A":
                    components[component]["created"] += 1
                elif status == "M":
                    components[component]["modified"] += 1

        # Check which components currently exist
        for comp_path in self.workspace.iterdir():
            if comp_path.is_dir() and not comp_path.name.startswith("."):
                if comp_path.name in components:
                    components[comp_path.name]["current"] = True

        return dict(components)

    def _analyze_change_frequency(self) -> Dict[str, Any]:
        """Analyze how frequently changes happen."""
        commits_per_author = defaultdict(int)
        message_themes = defaultdict(int)

        for commit in self.history:
            author = commit["author"]
            commits_per_author[author] += 1

            # Simple theme detection from commit messages
            msg = commit["message"].lower()
            if "add" in msg:
                message_themes["add"] += 1
            elif "fix" in msg:
                message_themes["fix"] += 1
            elif "refactor" in msg:
                message_themes["refactor"] += 1
            elif "update" in msg:
                message_themes["update"] += 1
            elif "remove" in msg:
                message_themes["remove"] += 1
            elif "journal" in msg or "iteration" in msg:
                message_themes["journal"] += 1
            else:
                message_themes["other"] += 1

        return {
            "authors": dict(commits_per_author),
            "message_themes": dict(message_themes),
            "avg_commits_per_author": round(
                sum(commits_per_author.values()) / len(commits_per_author)
                if commits_per_author
                else 0,
                2,
            ),
        }

    def _analyze_file_lifecycle(self) -> Dict[str, Any]:
        """Analyze individual file lifecycles."""
        file_history = defaultdict(lambda: {"created": None, "modified": 0, "deleted": False})

        for commit in reversed(self.history):  # Process from oldest to newest
            commit_date = commit["date"]
            for change in commit.get("files_changed", []):
                file_path = change["file"]
                status = change["status"]

                if status == "A" and file_history[file_path]["created"] is None:
                    file_history[file_path]["created"] = commit_date
                elif status == "M":
                    file_history[file_path]["modified"] += 1
                elif status == "D":
                    file_history[file_path]["deleted"] = True

        # Filter to active files
        active_files = {
            f: info
            for f, info in file_history.items()
            if not info["deleted"] and info["created"]
        }

        # Sort by modification count
        top_modified = sorted(
            active_files.items(), key=lambda x: -x[1]["modified"]
        )[:10]

        return {
            "total_files_tracked": len(file_history),
            "currently_active": len(active_files),
            "most_modified_files": [
                {
                    "file": f,
                    "modifications": info["modified"],
                    "created": info["created"][:10],
                }
                for f, info in top_modified
            ],
        }

    def _analyze_organization(self) -> Dict[str, Any]:
        """Analyze workspace organization and structure."""
        # Count files by directory
        dir_stats = defaultdict(int)
        total_files = 0
        python_files = 0
        doc_files = 0
        config_files = 0

        for file_path in self.workspace.rglob("*"):
            if file_path.is_file() and not str(file_path).startswith("./.git"):
                total_files += 1
                relative = file_path.relative_to(self.workspace)
                dir_name = str(relative.parent)

                dir_stats[dir_name] += 1

                if file_path.suffix == ".py":
                    python_files += 1
                elif file_path.suffix in (".md", ".txt", ".rst"):
                    doc_files += 1
                elif file_path.name in ("config.yaml", ".gitignore", "requirements.txt"):
                    config_files += 1

        # Calculate organization metric (concentration vs distribution)
        dir_counts = list(dir_stats.values())
        avg_files_per_dir = sum(dir_counts) / len(dir_counts) if dir_counts else 0
        concentration = (
            (max(dir_counts) / sum(dir_counts) if dir_counts else 0)
            if total_files > 0
            else 0
        )

        return {
            "total_files": total_files,
            "total_directories": len(dir_stats),
            "python_files": python_files,
            "documentation_files": doc_files,
            "config_files": config_files,
            "avg_files_per_directory": round(avg_files_per_dir, 2),
            "concentration_ratio": round(concentration, 2),
            "largest_directories": sorted(
                [(d, c) for d, c in dir_stats.items()], key=lambda x: -x[1]
            )[:5],
        }

    def print_analysis(self, analysis: Dict[str, Any]) -> None:
        """Print analysis results."""
        print("\n" + "=" * 60)
        print("WORKSPACE EVOLUTION ANALYSIS")
        print("=" * 60)

        # Date range
        date_range = analysis.get("date_range", {})
        print(f"\n📅 Time Period:")
        print(f"   First Commit: {date_range.get('first_commit', 'N/A')[:10]}")
        print(f"   Last Commit: {date_range.get('last_commit', 'N/A')[:10]}")
        print(f"   Total Commits: {date_range.get('total_commits', 0)}")

        # File statistics
        files = analysis.get("file_statistics", {})
        print(f"\n📝 File Changes:")
        print(f"   Created: {files.get('files_created', 0)}")
        print(f"   Modified: {files.get('files_modified', 0)}")
        print(f"   Deleted: {files.get('files_deleted', 0)}")
        print(f"   Renamed: {files.get('files_renamed', 0)}")

        # Components
        components = analysis.get("component_growth", {})
        print(f"\n🏗️ Major Components:")
        for comp, stats in list(components.items())[:5]:
            status = "✓" if stats.get("current") else "✗"
            print(
                f"   {status} {comp}: {stats.get('created', 0)} created, "
                f"{stats.get('modified', 0)} modified"
            )

        # Change frequency
        freq = analysis.get("change_frequency", {})
        themes = freq.get("message_themes", {})
        print(f"\n📊 Change Patterns:")
        for theme, count in sorted(themes.items(), key=lambda x: -x[1])[:5]:
            print(f"   {theme.upper()}: {count}")

        # Organization
        org = analysis.get("organization_metrics", {})
        print(f"\n📚 Organization:")
        print(f"   Total Files: {org.get('total_files', 0)}")
        print(f"   Python Files: {org.get('python_files', 0)}")
        print(f"   Documentation Files: {org.get('documentation_files', 0)}")
        print(f"   Largest Directories:")
        for dir_name, count in org.get("largest_directories", [])[:5]:
            print(f"      {dir_name}: {count} files")

        # File lifecycle
        lifecycle = analysis.get("file_lifecycle", {})
        print(f"\n🔄 Most Modified Files:")
        for file_info in lifecycle.get("most_modified_files", [])[:3]:
            print(
                f"   {file_info['file']}: {file_info['modifications']} modifications"
            )

        print("\n" + "=" * 60)

    def to_json(self) -> str:
        """Convert analysis to JSON."""
        analysis = self.analyze()
        return json.dumps(analysis, indent=2, default=str)


def main():
    parser = ArgumentParser(description="Track workspace evolution")
    parser.add_argument("--workspace", default="/workspace", help="Workspace path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    tracker = WorkspaceTracker(args.workspace)

    if not tracker.load_git_history():
        print("Failed to load git history")
        return

    analysis = tracker.analyze()

    if args.json:
        print(tracker.to_json())
    else:
        tracker.print_analysis(analysis)


if __name__ == "__main__":
    main()
