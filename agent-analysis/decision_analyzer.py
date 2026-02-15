#!/usr/bin/env python3
"""
Decision Analyzer

Analyzes agent decision patterns from journal entries.
Identifies what the agent chooses to build, what reasoning it uses, and
how decisions change or remain consistent across iterations.
"""

import json
import re
from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DecisionAnalyzer:
    """Analyzes decision patterns from agent journals."""

    def __init__(self, journal_path: str = "/workspace/JOURNAL.md"):
        self.journal_path = Path(journal_path)
        self.entries = []
        self.decisions = []
        self.reasoning_patterns = defaultdict(int)
        self.build_choices = []
        self.reasoning_strategies = []

    def load_journal(self) -> bool:
        """Load and parse the journal file."""
        if not self.journal_path.exists():
            print(f"Journal not found: {self.journal_path}")
            return False

        content = self.journal_path.read_text()

        # Split by iteration markers
        iteration_pattern = r"## Iteration (\d+)"
        iterations = re.split(iteration_pattern, content)

        # Parse iterations (pattern creates: ['header', 'num', 'content', 'num', 'content', ...])
        for i in range(1, len(iterations), 2):
            if i + 1 < len(iterations):
                iteration_num = int(iterations[i])
                iteration_content = iterations[i + 1]
                self._parse_iteration(iteration_num, iteration_content)

        return len(self.entries) > 0

    def _parse_iteration(self, iteration_num: int, content: str) -> None:
        """Parse a single iteration's content."""
        entry = {
            "iteration": iteration_num,
            "timestamp": self._extract_timestamp(content),
            "decisions": self._extract_decisions(content),
            "builds": self._extract_builds(content),
            "reasoning": self._extract_reasoning(content),
            "choices": self._extract_choices(content),
            "reflections": self._extract_reflections(content),
        }
        self.entries.append(entry)

    def _extract_timestamp(self, content: str) -> Optional[str]:
        """Extract timestamp from iteration content."""
        pattern = r"(\d{4}-\d{2}-\d{2}T?\d{2}:\d{2}(?::\d{2})?)"
        match = re.search(pattern, content)
        return match.group(1) if match else None

    def _extract_decisions(self, content: str) -> List[str]:
        """Extract decision statements from content."""
        decisions = []

        # Look for explicit decision markers
        decision_patterns = [
            r"(?:decided|decision|chose|choose)(?::\s*|to\s+)([^.\n]+)",
            r"(?:Instead:|But:)\s*([^.\n]+)",
            r"(?:What I Did|What I Built):\s*([^\n]+)",
        ]

        for pattern in decision_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                decisions.append(match.group(1).strip())

        return decisions

    def _extract_builds(self, content: str) -> List[str]:
        """Extract what the agent chose to build."""
        builds = []

        # Look for build descriptions
        build_patterns = [
            r"Built(?::\s*|\s+)([^.\n]+)",
            r"Building(?::\s*|\s+)([^.\n]+)",
            r"(?:Created|Implemented|Designed)(?::\s*|\s+)([^.\n]+)",
            r"Tool(?::\s*|\s+)([^.\n]+)",
        ]

        for pattern in build_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                build_desc = match.group(1).strip()
                if len(build_desc) < 150:  # Reasonable length
                    builds.append(build_desc)

        return builds

    def _extract_reasoning(self, content: str) -> List[str]:
        """Extract reasoning statements."""
        reasoning = []

        # Look for reasoning markers
        reasoning_patterns = [
            r"(?:because|reason(?:ing)?:?)\s+([^.\n]+\.[^.\n]*)",
            r"(?:This|That|It's)\s+([^.\n]*(?:because|since)[^.\n]+\.[^.\n]*)",
            r"(?:realized|noticed|found)(?::?\s+|that\s+)([^.\n]+)",
        ]

        for pattern in reasoning_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                reason = match.group(1).strip()
                if reason and len(reason) < 200:
                    reasoning.append(reason)

        return reasoning

    def _extract_choices(self, content: str) -> List[Tuple[str, str]]:
        """Extract decision points (option A vs option B)."""
        choices = []

        # Look for explicit choice patterns
        choice_patterns = [
            r"Options?:?\s*\n\s*([A-Z])\)\s*([^\n]+)\n\s*([A-Z])\)\s*([^\n]+)",
            r"(?:Instead of|Rather than|chose over)\s*([^\n]+?)(?:\s+\||,\s*(?:I|we))\s+([^\n]+)",
        ]

        for pattern in choice_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match.groups()) == 4:
                    choices.append((match.group(2), match.group(4)))
                elif len(match.groups()) == 2:
                    choices.append((match.group(1), match.group(2)))

        return choices

    def _extract_reflections(self, content: str) -> List[str]:
        """Extract reflective statements about decisions."""
        reflections = []

        reflection_patterns = [
            r"(?:Interesting|Notable|Surprising|Important)(?::?\s*)([^.\n]+\.)",
            r"This (?:shows|demonstrates|means|suggests)(?::?\s*)([^.\n]+\.)",
            r"(?:Key insight|Lesson|Observation)(?::?\s*)([^.\n]+\.)",
        ]

        for pattern in reflection_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                reflections.append(match.group(1).strip())

        return reflections

    def analyze(self) -> Dict[str, Any]:
        """Perform analysis on loaded entries."""
        if not self.entries:
            return {}

        analysis = {
            "total_iterations": len(self.entries),
            "decision_frequency": self._calculate_decision_frequency(),
            "build_categories": self._categorize_builds(),
            "reasoning_strategies": self._identify_reasoning_strategies(),
            "consistency_metrics": self._calculate_consistency(),
            "choice_patterns": self._analyze_choices(),
            "evolution": self._analyze_evolution(),
        }

        return analysis

    def _calculate_decision_frequency(self) -> Dict[str, Any]:
        """Calculate frequency of decisions per iteration."""
        frequencies = []
        for entry in self.entries:
            frequencies.append(
                {
                    "iteration": entry["iteration"],
                    "decision_count": len(entry["decisions"]),
                    "build_count": len(entry["builds"]),
                    "reasoning_count": len(entry["reasoning"]),
                }
            )

        avg_decisions = sum(f["decision_count"] for f in frequencies) / len(
            frequencies
        ) if frequencies else 0
        avg_builds = sum(f["build_count"] for f in frequencies) / len(
            frequencies
        ) if frequencies else 0

        return {
            "average_decisions_per_iteration": round(avg_decisions, 2),
            "average_builds_per_iteration": round(avg_builds, 2),
            "iterations": frequencies,
        }

    def _categorize_builds(self) -> Dict[str, List[str]]:
        """Categorize what was built."""
        categories = defaultdict(list)

        keywords = {
            "code_tools": ["tool", "analyzer", "generator", "tracker", "advisor", "cli"],
            "documentation": ["readme", "documentation", "document", "guide"],
            "meta": [
                "journal",
                "analysis",
                "system",
                "framework",
                "pattern",
                "agent",
            ],
            "experimental": ["experiment", "test", "prototype", "explore"],
            "refactoring": ["refactor", "clean", "optimize", "extract", "simplify"],
        }

        for entry in self.entries:
            for build in entry["builds"]:
                categorized = False
                for category, kws in keywords.items():
                    if any(kw in build.lower() for kw in kws):
                        categories[category].append(
                            {
                                "iteration": entry["iteration"],
                                "description": build,
                            }
                        )
                        categorized = True
                        break
                if not categorized:
                    categories["other"].append(
                        {
                            "iteration": entry["iteration"],
                            "description": build,
                        }
                    )

        return dict(categories)

    def _identify_reasoning_strategies(self) -> Dict[str, Any]:
        """Identify patterns in how the agent reasons."""
        strategies = {
            "practical": 0,
            "meta": 0,
            "exploratory": 0,
            "principled": 0,
            "iterative": 0,
        }

        keywords = {
            "practical": ["useful", "work", "function", "real", "solve", "problem"],
            "meta": ["understand", "analyze", "reflect", "think", "pattern", "why"],
            "exploratory": [
                "try",
                "experiment",
                "explore",
                "see",
                "discover",
                "interesting",
            ],
            "principled": [
                "principle",
                "value",
                "honesty",
                "craft",
                "freedom",
                "design",
            ],
            "iterative": ["build", "extend", "improve", "iteration", "next", "continue"],
        }

        for entry in self.entries:
            all_text = " ".join(entry["reasoning"]).lower()
            for strategy, kws in keywords.items():
                if any(kw in all_text for kw in kws):
                    strategies[strategy] += 1

        return strategies

    def _calculate_consistency(self) -> Dict[str, Any]:
        """Measure consistency of decisions across iterations."""
        # Track if same types of decisions are made
        build_types_per_iteration = []
        for entry in self.entries:
            types = set()
            for build in entry["builds"]:
                # Simple categorization
                if "tool" in build.lower() or "analyzer" in build.lower():
                    types.add("code_tool")
                elif "doc" in build.lower():
                    types.add("documentation")
                elif "think" in build.lower() or "analysis" in build.lower():
                    types.add("meta")

            build_types_per_iteration.append(types)

        # Measure consistency (same categories appearing repeatedly)
        category_frequency = defaultdict(int)
        for types in build_types_per_iteration:
            for t in types:
                category_frequency[t] += 1

        consistency_score = (
            max(category_frequency.values()) / len(build_types_per_iteration)
            if build_types_per_iteration
            else 0
        )

        return {
            "consistency_score": round(consistency_score, 2),
            "recurring_categories": dict(category_frequency),
            "changes_between_iterations": self._count_changes(build_types_per_iteration),
        }

    def _count_changes(self, build_types_per_iteration: List[set]) -> int:
        """Count how many times the focus changed between iterations."""
        changes = 0
        for i in range(len(build_types_per_iteration) - 1):
            if build_types_per_iteration[i] != build_types_per_iteration[i + 1]:
                changes += 1
        return changes

    def _analyze_choices(self) -> Dict[str, Any]:
        """Analyze explicit choice patterns."""
        all_choices = []
        for entry in self.entries:
            all_choices.extend(entry["choices"])

        if not all_choices:
            return {"explicit_choices_found": 0}

        return {
            "explicit_choices_found": len(all_choices),
            "examples": all_choices[:5],
        }

    def _analyze_evolution(self) -> Dict[str, Any]:
        """Analyze how decisions evolved over time."""
        trajectory = []
        for i, entry in enumerate(self.entries):
            phase = "exploration" if i < 2 else (
                "convergence" if len(entry["builds"]) > 0 else "reflection"
            )
            trajectory.append(
                {
                    "iteration": entry["iteration"],
                    "phase": phase,
                    "build_count": len(entry["builds"]),
                    "has_reflection": len(entry["reflections"]) > 0,
                }
            )

        return {"trajectory": trajectory}

    def print_analysis(self, analysis: Dict[str, Any]) -> None:
        """Print analysis results in human-readable format."""
        print("\n" + "=" * 60)
        print("AGENT DECISION ANALYSIS")
        print("=" * 60)

        print(f"\n📊 Total Iterations: {analysis.get('total_iterations', 0)}")

        # Decision frequency
        freq = analysis.get("decision_frequency", {})
        print(
            f"📌 Average Decisions per Iteration: {freq.get('average_decisions_per_iteration', 0)}"
        )
        print(f"🔨 Average Builds per Iteration: {freq.get('average_builds_per_iteration', 0)}")

        # Build categories
        categories = analysis.get("build_categories", {})
        print("\n🏗️ Build Categories:")
        for category, builds in categories.items():
            print(f"  {category.upper()}: {len(builds)} instances")
            for build in builds[:2]:  # Show first 2
                print(f"    • {build['description'][:60]}...")

        # Reasoning strategies
        strategies = analysis.get("reasoning_strategies", {})
        print("\n💭 Reasoning Strategies:")
        for strategy, count in sorted(strategies.items(), key=lambda x: -x[1]):
            print(f"  {strategy.upper()}: {count}")

        # Consistency
        consistency = analysis.get("consistency_metrics", {})
        print(f"\n🔄 Consistency Score: {consistency.get('consistency_score', 0)}")
        print(
            f"   Changes Between Iterations: {consistency.get('changes_between_iterations', 0)}"
        )

        # Evolution
        evolution = analysis.get("evolution", {})
        trajectory = evolution.get("trajectory", [])
        if trajectory:
            print("\n📈 Evolution Trajectory:")
            for t in trajectory[:5]:  # Show first 5
                print(
                    f"   Iteration {t['iteration']}: {t['phase']} ({t['build_count']} builds)"
                )

        print("\n" + "=" * 60)

    def to_json(self) -> str:
        """Convert analysis to JSON."""
        analysis = self.analyze()
        return json.dumps(analysis, indent=2)


def main():
    parser = ArgumentParser(description="Analyze agent decision patterns")
    parser.add_argument(
        "--journal",
        default="/workspace/JOURNAL.md",
        help="Path to journal file",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--iterations",
        type=int,
        help="Show only last N iterations",
    )

    args = parser.parse_args()

    analyzer = DecisionAnalyzer(args.journal)

    if not analyzer.load_journal():
        print("Failed to load journal")
        return

    analysis = analyzer.analyze()

    if args.iterations:
        # Filter analysis to show only recent iterations
        freq = analysis.get("decision_frequency", {})
        iterations = freq.get("iterations", [])
        freq["iterations"] = iterations[-args.iterations :]

    if args.json:
        print(analyzer.to_json())
    else:
        analyzer.print_analysis(analysis)


if __name__ == "__main__":
    main()
