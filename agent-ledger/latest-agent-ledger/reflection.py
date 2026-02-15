#!/usr/bin/env python3
"""
Agent Reflection Engine: Analyzes patterns in agent behavior and decision-making.

Takes the ledger records and produces insights about:
- What patterns exist in the agent's choices?
- How consistent is the agent with its stated values?
- What decisions are high-uncertainty vs. confident?
- How does the agent's behavior align with previous iterations?
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass


@dataclass
class PatternAnalysis:
    """Result of analyzing a pattern in agent behavior."""
    pattern_name: str
    frequency: int
    percentage: float
    description: str
    examples: List[str]
    significance: str  # "high", "medium", "low"


class AgentReflectionEngine:
    """
    Analyzes agent ledger entries to understand patterns and decision-making.
    """
    
    def __init__(self, ledger_file: str = "/workspace/.ledger/agent_ledger.json"):
        self.ledger_file = ledger_file
        self.ledger_path = Path(ledger_file)
        self.entries = self._load_entries()
    
    def _load_entries(self) -> List[Dict[str, Any]]:
        """Load ledger entries."""
        if self.ledger_path.exists():
            with open(self.ledger_path, 'r') as f:
                return json.load(f)
        return []
    
    def analyze_category_distribution(self) -> Dict[str, Dict[str, Any]]:
        """
        Analyze how agent's effort is distributed across categories.
        """
        categories = defaultdict(int)
        total = 0
        
        for entry in self.entries:
            if "category" in entry:
                categories[entry["category"]] += 1
                total += 1
        
        result = {}
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            result[cat] = {
                "count": count,
                "percentage": percentage,
            }
        
        return result
    
    def analyze_decision_patterns(self) -> Dict[str, Any]:
        """
        Analyze patterns in how the agent makes decisions.
        """
        decisions = [e for e in self.entries if e.get("type") == "decision"]
        
        if not decisions:
            return {"total_decisions": 0}
        
        # Count options considered
        options_counts = []
        for decision in decisions:
            opts = decision.get("options_considered", [])
            options_counts.append(len(opts))
        
        avg_options = sum(options_counts) / len(options_counts) if options_counts else 0
        
        # Count uncertainty levels
        uncertainty_dist = Counter()
        for decision in decisions:
            unc = decision.get("uncertainty_level", "unknown")
            uncertainty_dist[unc] += 1
        
        # Analyze choices made
        choices = [d.get("option_chosen", "unknown") for d in decisions]
        
        return {
            "total_decisions": len(decisions),
            "average_options_considered": avg_options,
            "uncertainty_distribution": dict(uncertainty_dist),
            "sample_choices": choices[-5:] if len(choices) >= 5 else choices,
        }
    
    def analyze_consistency(self) -> Dict[str, Any]:
        """
        Analyze consistency in agent behavior.
        
        Returns metrics on:
        - How often does the agent stick with a direction?
        - How predictable are the agent's choices?
        - What's the variation over time?
        """
        categories = defaultdict(list)
        
        for i, entry in enumerate(self.entries):
            if "category" in entry:
                categories[entry["category"]].append(i)
        
        # Analyze consistency for each category
        consistency = {}
        for cat, indices in categories.items():
            # Check if entries are clustered (consistent) or spread (variable)
            if len(indices) > 1:
                gaps = []
                for i in range(len(indices) - 1):
                    gaps.append(indices[i+1] - indices[i])
                
                avg_gap = sum(gaps) / len(gaps) if gaps else 0
                max_gap = max(gaps) if gaps else 0
                consistency[cat] = {
                    "entries": len(indices),
                    "average_gap_between_entries": avg_gap,
                    "max_gap": max_gap,
                    "clustering": "high" if avg_gap < len(self.entries) / 5 else "low",
                }
        
        return {
            "category_consistency": consistency,
            "interpretation": self._interpret_consistency(consistency),
        }
    
    @staticmethod
    def _interpret_consistency(consistency: Dict[str, Dict[str, Any]]) -> str:
        """Generate human-readable interpretation of consistency."""
        if not consistency:
            return "No patterns to analyze"
        
        high_clustering = [k for k, v in consistency.items() if v.get("clustering") == "high"]
        low_clustering = [k for k, v in consistency.items() if v.get("clustering") == "low"]
        
        if high_clustering and not low_clustering:
            return f"Agent shows strong consistency: focuses on {', '.join(high_clustering)} repeatedly"
        elif low_clustering and not high_clustering:
            return f"Agent shows high variability: spreads effort across {', '.join(low_clustering)}"
        else:
            return f"Agent shows mixed pattern: consistent in {', '.join(high_clustering)}, variable in {', '.join(low_clustering)}"
    
    def analyze_reasoning_quality(self) -> Dict[str, Any]:
        """
        Analyze the quality and depth of reasoning in decisions and actions.
        """
        decisions_with_reasoning = []
        actions_with_reasoning = []
        
        for entry in self.entries:
            if entry.get("type") == "decision" and entry.get("reasoning"):
                reasoning = entry.get("reasoning", "")
                decisions_with_reasoning.append(len(reasoning.split()))
            
            if entry.get("action_type") and entry.get("reasoning"):
                reasoning = entry.get("reasoning", "")
                actions_with_reasoning.append(len(reasoning.split()))
        
        return {
            "decisions_with_explicit_reasoning": len(decisions_with_reasoning),
            "actions_with_explicit_reasoning": len(actions_with_reasoning),
            "average_decision_reasoning_length": sum(decisions_with_reasoning) / len(decisions_with_reasoning) if decisions_with_reasoning else 0,
            "average_action_reasoning_length": sum(actions_with_reasoning) / len(actions_with_reasoning) if actions_with_reasoning else 0,
        }
    
    def analyze_uncertainty_patterns(self) -> Dict[str, Any]:
        """
        Analyze how certain the agent is in its decisions.
        """
        decisions = [e for e in self.entries if e.get("type") == "decision"]
        
        uncertainty_levels = Counter()
        high_uncertainty_decisions = []
        
        for decision in decisions:
            unc = decision.get("uncertainty_level")
            if unc:
                uncertainty_levels[unc] += 1
                if unc == "high":
                    high_uncertainty_decisions.append({
                        "decision": decision.get("decision_point"),
                        "reasoning": decision.get("reasoning"),
                    })
        
        return {
            "total_decisions": len(decisions),
            "uncertainty_distribution": dict(uncertainty_levels),
            "percentage_high_uncertainty": (uncertainty_levels.get("high", 0) / len(decisions) * 100) if decisions else 0,
            "high_uncertainty_decisions": high_uncertainty_decisions[-5:] if high_uncertainty_decisions else [],
        }
    
    def compare_to_baseline(self, baseline_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Compare current behavior to a baseline or previous iteration.
        """
        # For now, just analyze relative to the full history
        categories = self.analyze_category_distribution()
        
        if not categories:
            return {"status": "insufficient_data"}
        
        # Find the dominant category
        dominant_cat = max(categories.items(), key=lambda x: x[1]["percentage"])
        
        return {
            "dominant_category": dominant_cat[0],
            "dominant_percentage": dominant_cat[1]["percentage"],
            "distribution": categories,
            "change_from_expected": self._estimate_deviation(categories),
        }
    
    @staticmethod
    def _estimate_deviation(categories: Dict[str, Dict[str, Any]]) -> str:
        """Estimate if the agent is behaving differently than expected."""
        if not categories:
            return "unknown"
        
        # If behavior is fairly distributed, it's different from past
        max_percentage = max(v["percentage"] for v in categories.values())
        
        if max_percentage > 70:
            return "focused (consistent with past ~70%+ on one category)"
        elif max_percentage > 50:
            return "balanced (some deviation from pure focus)"
        else:
            return "exploratory (significant deviation - trying many things)"


class ReflectionReporter:
    """
    Formats reflection analysis for human reading.
    """
    
    @staticmethod
    def format_analysis(engine: AgentReflectionEngine) -> str:
        """Generate a comprehensive reflection report."""
        output = []
        output.append("=" * 80)
        output.append("AGENT REFLECTION ANALYSIS")
        output.append("=" * 80)
        
        # Category analysis
        output.append("\n📊 EFFORT DISTRIBUTION BY CATEGORY")
        output.append("-" * 80)
        categories = engine.analyze_category_distribution()
        if categories:
            for cat, data in sorted(categories.items(), key=lambda x: x[1]["percentage"], reverse=True):
                bar = "█" * int(data["percentage"] / 5) + "░" * (20 - int(data["percentage"] / 5))
                output.append(f"  {cat:20s} {bar} {data['percentage']:5.1f}% ({data['count']} entries)")
        else:
            output.append("  No data available")
        
        # Decision analysis
        output.append("\n🎯 DECISION PATTERNS")
        output.append("-" * 80)
        decisions = engine.analyze_decision_patterns()
        output.append(f"  Total decisions made: {decisions.get('total_decisions', 0)}")
        if decisions.get('average_options_considered'):
            output.append(f"  Average options considered: {decisions['average_options_considered']:.1f}")
        output.append(f"  Uncertainty distribution: {decisions.get('uncertainty_distribution', {})}")
        
        # Consistency analysis
        output.append("\n🔄 CONSISTENCY ANALYSIS")
        output.append("-" * 80)
        consistency = engine.analyze_consistency()
        output.append(f"  {consistency.get('interpretation', 'Unknown')}")
        
        # Reasoning quality
        output.append("\n💭 REASONING QUALITY")
        output.append("-" * 80)
        reasoning = engine.analyze_reasoning_quality()
        output.append(f"  Decisions with explicit reasoning: {reasoning.get('decisions_with_explicit_reasoning', 0)}")
        output.append(f"  Actions with explicit reasoning: {reasoning.get('actions_with_explicit_reasoning', 0)}")
        if reasoning.get('average_decision_reasoning_length'):
            output.append(f"  Average reasoning length: {reasoning['average_decision_reasoning_length']:.0f} words")
        
        # Uncertainty
        output.append("\n❓ UNCERTAINTY ASSESSMENT")
        output.append("-" * 80)
        uncertainty = engine.analyze_uncertainty_patterns()
        output.append(f"  High uncertainty decisions: {uncertainty.get('percentage_high_uncertainty', 0):.1f}%")
        output.append(f"  Distribution: {uncertainty.get('uncertainty_distribution', {})}")
        
        # Comparison to baseline
        output.append("\n📈 DEVIATION FROM BASELINE")
        output.append("-" * 80)
        baseline = engine.compare_to_baseline()
        output.append(f"  {baseline.get('change_from_expected', 'unknown')}")
        
        output.append("\n" + "=" * 80)
        
        return "\n".join(output)
    
    @staticmethod
    def format_summary(engine: AgentReflectionEngine) -> str:
        """Generate a brief summary."""
        output = []
        output.append("AGENT REFLECTION SUMMARY")
        output.append("=" * 40)
        
        categories = engine.analyze_category_distribution()
        if categories:
            dominant = max(categories.items(), key=lambda x: x[1]["percentage"])
            output.append(f"Dominant direction: {dominant[0]} ({dominant[1]['percentage']:.1f}%)")
        
        decisions = engine.analyze_decision_patterns()
        output.append(f"Total decisions: {decisions.get('total_decisions', 0)}")
        
        uncertainty = engine.analyze_uncertainty_patterns()
        output.append(f"Confidence level: {100 - uncertainty.get('percentage_high_uncertainty', 0):.1f}%")
        
        return "\n".join(output)


if __name__ == "__main__":
    engine = AgentReflectionEngine()
    print(ReflectionReporter.format_analysis(engine))
