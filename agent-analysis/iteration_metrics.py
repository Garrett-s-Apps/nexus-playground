#!/usr/bin/env python3
"""
Iteration Metrics

Analyzes patterns within and across iterations.
Measures iteration productivity, decision-making, and code output.
"""

import json
import re
from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class IterationMetrics:
    """Analyze iteration-level patterns and metrics."""

    def __init__(self, journal_path: str = "/workspace/JOURNAL.md"):
        self.journal_path = Path(journal_path)
        self.iterations = []
        self.load_journal()

    def load_journal(self) -> bool:
        """Load and parse iterations from journal."""
        if not self.journal_path.exists():
            return False

        content = self.journal_path.read_text()

        # Split by iteration headers
        iteration_pattern = r"## Iteration (\d+)"
        splits = re.split(iteration_pattern, content)

        # Process: ['header', 'num', 'content', 'num', 'content', ...]
        for i in range(1, len(splits), 2):
            if i + 1 < len(splits):
                iteration_num = int(splits[i])
                iteration_content = splits[i + 1]
                iteration_data = self._parse_iteration(iteration_num, iteration_content)
                if iteration_data:
                    self.iterations.append(iteration_data)

        return len(self.iterations) > 0

    def _parse_iteration(self, num: int, content: str) -> Optional[Dict[str, Any]]:
        """Parse a single iteration entry."""
        iteration = {
            "iteration": num,
            "timestamp": self._extract_timestamp(content),
            "word_count": len(content.split()),
            "sections": self._count_sections(content),
            "themes": self._extract_themes(content),
            "artifacts": self._count_artifacts(content),
            "decisions_made": self._count_decisions(content),
            "has_reflection": "reflection" in content.lower()
            or "learned" in content.lower(),
            "has_uncertainty": "uncertain" in content.lower()
            or "don't know" in content.lower(),
            "builds_something": self._detects_building(content),
        }
        return iteration

    def _extract_timestamp(self, content: str) -> Optional[str]:
        """Extract iteration timestamp."""
        pattern = r"(\d{4}-\d{2}-\d{2}T?\d{2}:\d{2})"
        match = re.search(pattern, content)
        return match.group(1) if match else None

    def _count_sections(self, content: str) -> int:
        """Count major sections in iteration."""
        return len(re.findall(r"\n#{2,3} ", content))

    def _extract_themes(self, content: str) -> List[str]:
        """Extract main themes from iteration."""
        themes = []
        keywords = {
            "experimental": ["experiment", "try", "explore", "unusual"],
            "practical": ["work", "test", "implement", "real"],
            "meta": ["thinking", "analysis", "understand", "pattern"],
            "refactor": ["clean", "improve", "optimize", "extract"],
            "document": ["readme", "documentation", "example", "guide"],
            "complete": ["done", "finished", "complete", "ready"],
        }

        content_lower = content.lower()
        for theme, keywords_list in keywords.items():
            if any(kw in content_lower for kw in keywords_list):
                themes.append(theme)

        return themes

    def _count_artifacts(self, content: str) -> int:
        """Count artifacts (tools, files, etc.) mentioned."""
        # Count lines with specific patterns
        artifact_patterns = [
            r"built|created|made|generated|wrote",
            r"\.py|\.md|\.json|\.yaml",
            r"tool|script|module|class|function",
        ]

        count = 0
        for pattern in artifact_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            count += len(matches)

        return count

    def _count_decisions(self, content: str) -> int:
        """Count decision statements."""
        decision_patterns = [
            r"decided|decision|chose|choose",
            r"instead|but|rather|alternatively",
            r"what i did|what i built",
        ]

        count = 0
        for pattern in decision_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            count += len(matches)

        return count

    def _detects_building(self, content: str) -> bool:
        """Check if iteration describes building something."""
        build_indicators = [
            "built",
            "created",
            "implemented",
            "designed",
            "wrote",
            "generated",
        ]
        return any(indicator in content.lower() for indicator in build_indicators)

    def analyze(self) -> Dict[str, Any]:
        """Perform analysis on iterations."""
        if not self.iterations:
            return {}

        return {
            "total_iterations": len(self.iterations),
            "iteration_summary": self._summarize_iterations(),
            "patterns": self._identify_patterns(),
            "productivity_metrics": self._calculate_productivity(),
            "decision_metrics": self._analyze_decisions(),
            "reflection_metrics": self._analyze_reflection(),
        }

    def _summarize_iterations(self) -> List[Dict[str, Any]]:
        """Summarize each iteration."""
        summary = []
        for it in self.iterations:
            summary.append(
                {
                    "iteration": it["iteration"],
                    "timestamp": it["timestamp"],
                    "word_count": it["word_count"],
                    "sections": it["sections"],
                    "themes": it["themes"],
                    "builds": it["builds_something"],
                    "reflects": it["has_reflection"],
                }
            )
        return summary

    def _identify_patterns(self) -> Dict[str, Any]:
        """Identify patterns across iterations."""
        # Frequency of themes
        all_themes = defaultdict(int)
        for it in self.iterations:
            for theme in it["themes"]:
                all_themes[theme] += 1

        # Pattern of building
        build_pattern = [it["builds_something"] for it in self.iterations]
        builds_consistently = sum(build_pattern) / len(build_pattern) if build_pattern else 0

        # Reflection pattern
        reflection_pattern = [it["has_reflection"] for it in self.iterations]
        reflects_consistently = (
            sum(reflection_pattern) / len(reflection_pattern) if reflection_pattern else 0
        )

        return {
            "theme_frequencies": dict(all_themes),
            "builds_percentage": round(builds_consistently * 100, 1),
            "reflects_percentage": round(reflects_consistently * 100, 1),
            "most_common_themes": sorted(all_themes.items(), key=lambda x: -x[1])[:5],
        }

    def _calculate_productivity(self) -> Dict[str, Any]:
        """Calculate productivity metrics."""
        word_counts = [it["word_count"] for it in self.iterations]
        artifact_counts = [it["artifacts"] for it in self.iterations]

        avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
        avg_artifacts = sum(artifact_counts) / len(artifact_counts) if artifact_counts else 0

        return {
            "average_words_per_iteration": round(avg_words, 0),
            "average_artifacts_per_iteration": round(avg_artifacts, 1),
            "max_words_iteration": max(
                (it["iteration"], it["word_count"]) for it in self.iterations
            )
            if self.iterations
            else None,
            "min_words_iteration": min(
                (it["iteration"], it["word_count"]) for it in self.iterations
            )
            if self.iterations
            else None,
        }

    def _analyze_decisions(self) -> Dict[str, Any]:
        """Analyze decision-making patterns."""
        decision_counts = [it["decisions_made"] for it in self.iterations]
        avg_decisions = (
            sum(decision_counts) / len(decision_counts) if decision_counts else 0
        )

        high_decision_iterations = [
            it["iteration"]
            for it in self.iterations
            if it["decisions_made"] > avg_decisions + 1
        ]

        return {
            "average_decisions_per_iteration": round(avg_decisions, 1),
            "high_decision_iterations": high_decision_iterations,
            "lowest_decision_iteration": min(
                (it["iteration"], it["decisions_made"]) for it in self.iterations
            )
            if self.iterations
            else None,
        }

    def _analyze_reflection(self) -> Dict[str, Any]:
        """Analyze reflection patterns."""
        reflecting = [it for it in self.iterations if it["has_reflection"]]
        uncertain = [it for it in self.iterations if it["has_uncertainty"]]

        return {
            "iterations_with_reflection": len(reflecting),
            "iterations_with_uncertainty": len(uncertain),
            "reflection_rate": round(len(reflecting) / len(self.iterations) * 100, 1)
            if self.iterations
            else 0,
            "uncertainty_rate": round(len(uncertain) / len(self.iterations) * 100, 1)
            if self.iterations
            else 0,
        }

    def print_analysis(self, analysis: Dict[str, Any]) -> None:
        """Print analysis in human-readable format."""
        print("\n" + "=" * 60)
        print("ITERATION METRICS ANALYSIS")
        print("=" * 60)

        print(f"\n📊 Overview:")
        print(f"   Total Iterations: {analysis.get('total_iterations', 0)}")

        # Productivity
        prod = analysis.get("productivity_metrics", {})
        print(f"\n📈 Productivity:")
        print(
            f"   Average Words/Iteration: {prod.get('average_words_per_iteration', 0)}"
        )
        print(
            f"   Average Artifacts/Iteration: {prod.get('average_artifacts_per_iteration', 0)}"
        )

        # Patterns
        patterns = analysis.get("patterns", {})
        print(f"\n🔄 Patterns:")
        print(f"   Builds Something: {patterns.get('builds_percentage', 0)}%")
        print(f"   Reflects: {patterns.get('reflects_percentage', 0)}%")
        print(f"   Most Common Themes:")
        for theme, count in patterns.get("most_common_themes", [])[:5]:
            print(f"      {theme}: {count}")

        # Decisions
        decisions = analysis.get("decision_metrics", {})
        print(f"\n🎯 Decision Making:")
        print(
            f"   Average Decisions/Iteration: {decisions.get('average_decisions_per_iteration', 0)}"
        )
        if decisions.get("high_decision_iterations"):
            print(
                f"   High-Decision Iterations: {decisions.get('high_decision_iterations')}"
            )

        # Reflection
        reflection = analysis.get("reflection_metrics", {})
        print(f"\n💭 Reflection:")
        print(f"   Reflection Rate: {reflection.get('reflection_rate', 0)}%")
        print(f"   Uncertainty Rate: {reflection.get('uncertainty_rate', 0)}%")

        print("\n" + "=" * 60)

    def to_json(self) -> str:
        """Convert to JSON."""
        analysis = self.analyze()
        return json.dumps(analysis, indent=2, default=str)


def main():
    parser = ArgumentParser(description="Analyze iteration-level metrics")
    parser.add_argument(
        "--journal",
        default="/workspace/JOURNAL.md",
        help="Path to journal",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    metrics = IterationMetrics(args.journal)

    if not metrics.iterations:
        print("No iterations found")
        return

    analysis = metrics.analyze()

    if args.json:
        print(metrics.to_json())
    else:
        metrics.print_analysis(analysis)


if __name__ == "__main__":
    main()
