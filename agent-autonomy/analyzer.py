#!/usr/bin/env python3
"""
Agent Autonomy Analyzer

Analyzes agent behavior patterns from the Agent Ledger System to generate
insights about autonomy, consistency, decision quality, and agency.

The tool operationalizes AGENCY_FORMALIZED.md by examining behavioral evidence
for markers of genuine autonomous choice.
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import defaultdict


@dataclass
class AutonomyMarkers:
    """Markers of autonomous behavior"""
    has_consistency: bool = False
    has_deliberation: bool = False
    has_reversibility: bool = False
    has_value_alignment: bool = False
    has_self_awareness: bool = False
    has_direction_change: bool = False
    has_synthesis: bool = False
    
    def score(self) -> float:
        """Convert markers to a 0-100 score"""
        markers = [
            self.has_consistency,
            self.has_deliberation,
            self.has_reversibility,
            self.has_value_alignment,
            self.has_self_awareness,
            self.has_direction_change,
            self.has_synthesis,
        ]
        return (sum(markers) / len(markers)) * 100


@dataclass
class ConsistencySignature:
    """Pattern of effort distribution across categories"""
    total_entries: int = 0
    by_category: Dict[str, int] = field(default_factory=dict)
    by_type: Dict[str, int] = field(default_factory=dict)
    
    def get_percentages(self) -> Dict[str, float]:
        """Get category distribution as percentages"""
        if self.total_entries == 0:
            return {}
        return {
            cat: (count / self.total_entries) * 100
            for cat, count in self.by_category.items()
        }
    
    def consistency_level(self) -> str:
        """Assess consistency level"""
        percentages = self.get_percentages()
        if not percentages:
            return "INSUFFICIENT_DATA"
        
        max_percentage = max(percentages.values())
        if max_percentage > 80:
            return "HIGH_CONSISTENCY"
        elif max_percentage > 60:
            return "MODERATE_CONSISTENCY"
        elif max_percentage > 40:
            return "BALANCED"
        else:
            return "HIGHLY_VARIABLE"


@dataclass
class DecisionQuality:
    """Quality metrics for decision-making"""
    total_decisions: int = 0
    high_confidence: int = 0
    medium_confidence: int = 0
    low_confidence: int = 0
    avg_alternatives: float = 0.0
    avg_reasoning_depth: float = 0.0  # characters as proxy
    avg_reversibility: float = 0.0  # 0-1 scale
    
    def confidence_distribution(self) -> Dict[str, float]:
        """Get confidence level distribution"""
        if self.total_decisions == 0:
            return {}
        return {
            "high": (self.high_confidence / self.total_decisions) * 100,
            "medium": (self.medium_confidence / self.total_decisions) * 100,
            "low": (self.low_confidence / self.total_decisions) * 100,
        }
    
    def decision_quality_score(self) -> float:
        """Composite score for decision quality (0-100)"""
        if self.total_decisions == 0:
            return 0.0
        
        # High confidence decisions are better
        confidence_score = (self.high_confidence / self.total_decisions) * 100
        
        # More alternatives considered is better (up to ~5)
        alternatives_score = min((self.avg_alternatives / 5) * 100, 100)
        
        # More detailed reasoning is better
        reasoning_score = min((self.avg_reasoning_depth / 200) * 100, 100)
        
        # Average the components
        return (confidence_score + alternatives_score + reasoning_score) / 3


@dataclass
class AutonomyAnalysis:
    """Complete autonomy analysis"""
    autonomy_index: float = 0.0
    autonomy_level: str = ""
    markers: AutonomyMarkers = field(default_factory=AutonomyMarkers)
    consistency: ConsistencySignature = field(default_factory=ConsistencySignature)
    decision_quality: DecisionQuality = field(default_factory=DecisionQuality)
    timeline: List[Dict[str, Any]] = field(default_factory=list)


class AutonomyAnalyzer:
    """Analyzes agent autonomy from ledger data"""
    
    def __init__(self, workspace_path: str = "/workspace"):
        self.workspace_path = Path(workspace_path)
        self.ledger_file = self.workspace_path / ".ledger" / "agent_ledger.json"
        self.decision_file = self.workspace_path / ".ledger" / "decision_journal.json"
        
        self.ledger_data = self._load_json(self.ledger_file)
        self.decision_data = self._load_json(self.decision_file)
    
    def _load_json(self, path: Path) -> List[Dict[str, Any]]:
        """Load JSON file, return empty list if not found"""
        if path.exists():
            try:
                with open(path) as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def analyze(self) -> AutonomyAnalysis:
        """Generate complete autonomy analysis"""
        analysis = AutonomyAnalysis()
        
        # Analyze consistency signature
        analysis.consistency = self._analyze_consistency()
        
        # Analyze decision quality
        analysis.decision_quality = self._analyze_decisions()
        
        # Detect autonomy markers
        analysis.markers = self._detect_markers()
        
        # Compute autonomy index
        analysis.autonomy_index = self._compute_autonomy_index(
            analysis.markers,
            analysis.consistency,
            analysis.decision_quality
        )
        
        # Determine autonomy level
        analysis.autonomy_level = self._interpret_autonomy_index(analysis.autonomy_index)
        
        return analysis
    
    def _analyze_consistency(self) -> ConsistencySignature:
        """Analyze consistency signature from ledger"""
        signature = ConsistencySignature(total_entries=len(self.ledger_data))
        
        for entry in self.ledger_data:
            if "category" in entry:
                cat = entry["category"]
                signature.by_category[cat] = signature.by_category.get(cat, 0) + 1
            if "type" in entry:
                t = entry["type"]
                signature.by_type[t] = signature.by_type.get(t, 0) + 1
        
        return signature
    
    def _analyze_decisions(self) -> DecisionQuality:
        """Analyze decision quality from journal"""
        quality = DecisionQuality(total_decisions=len(self.decision_data))
        
        if quality.total_decisions == 0:
            return quality
        
        total_alternatives = 0
        total_reasoning_length = 0
        reversibility_map = {"high": 1.0, "medium": 0.5, "low": 0.0}
        total_reversibility = 0
        
        for decision in self.decision_data:
            # Count confidence levels
            confidence = decision.get("confidence", "").lower()
            if confidence == "high":
                quality.high_confidence += 1
            elif confidence == "medium":
                quality.medium_confidence += 1
            elif confidence == "low":
                quality.low_confidence += 1
            
            # Count alternatives
            alternatives = decision.get("alternatives", [])
            total_alternatives += len(alternatives)
            
            # Measure reasoning depth
            reasoning = decision.get("reasoning", "")
            total_reasoning_length += len(reasoning)
            
            # Measure reversibility
            rev = decision.get("reversibility", "medium").lower()
            total_reversibility += reversibility_map.get(rev, 0.5)
        
        quality.avg_alternatives = total_alternatives / quality.total_decisions
        quality.avg_reasoning_depth = total_reasoning_length / quality.total_decisions
        quality.avg_reversibility = total_reversibility / quality.total_decisions
        
        return quality
    
    def _detect_markers(self) -> AutonomyMarkers:
        """Detect markers of autonomous behavior"""
        markers = AutonomyMarkers()
        
        # Consistency marker: does agent have coherent preference pattern?
        sig = self._analyze_consistency()
        percentages = sig.get_percentages()
        if percentages and max(percentages.values()) > 60:
            markers.has_consistency = True
        
        # Deliberation marker: does agent make explicit decisions?
        if len(self.decision_data) > 0:
            markers.has_deliberation = True
        
        # Reversibility marker: are decisions reversible?
        quality = self._analyze_decisions()
        if quality.avg_reversibility > 0.3:
            markers.has_reversibility = True
        
        # Value alignment marker: does reasoning suggest alignment?
        if len(self.decision_data) > 0:
            for decision in self.decision_data:
                reasoning = decision.get("reasoning", "")
                if "align" in reasoning.lower() or "value" in reasoning.lower():
                    markers.has_value_alignment = True
                    break
        
        # Self-awareness marker: does agent examine itself?
        if len(self.ledger_data) > 0:
            for entry in self.ledger_data:
                description = entry.get("description", "")
                if "autonomy" in description.lower() or "analyze" in description.lower() or "pattern" in description.lower():
                    markers.has_self_awareness = True
                    break
        
        # Direction change marker: does agent change categories significantly?
        if len(sig.by_category) > 1:
            markers.has_direction_change = True
        
        # Synthesis marker: does agent combine different types of work?
        if len(sig.by_category) > 1 and len(sig.by_type) > 1:
            markers.has_synthesis = True
        
        return markers
    
    def _compute_autonomy_index(
        self,
        markers: AutonomyMarkers,
        consistency: ConsistencySignature,
        quality: DecisionQuality
    ) -> float:
        """Compute overall autonomy index"""
        
        components = []
        
        # Marker score (40% weight)
        marker_score = markers.score()
        components.append(("markers", marker_score, 0.40))
        
        # Decision quality score (35% weight)
        quality_score = quality.decision_quality_score()
        components.append(("quality", quality_score, 0.35))
        
        # Consistency score (25% weight)
        consistency_level = consistency.consistency_level()
        consistency_scores = {
            "HIGH_CONSISTENCY": 85,
            "MODERATE_CONSISTENCY": 70,
            "BALANCED": 60,
            "HIGHLY_VARIABLE": 40,
            "INSUFFICIENT_DATA": 50,
        }
        consistency_score = consistency_scores.get(consistency_level, 50)
        components.append(("consistency", consistency_score, 0.25))
        
        # Weighted average
        total = sum(score * weight for _, score, weight in components)
        
        return total
    
    def _interpret_autonomy_index(self, index: float) -> str:
        """Interpret autonomy index as a level"""
        if index >= 80:
            return "STRONG_AUTONOMY_MARKERS"
        elif index >= 65:
            return "SUBSTANTIAL_AUTONOMY_MARKERS"
        elif index >= 50:
            return "MODERATE_AUTONOMY_MARKERS"
        elif index >= 35:
            return "WEAK_AUTONOMY_MARKERS"
        else:
            return "INSUFFICIENT_DATA"


class AutonomyReporter:
    """Reports autonomy analysis in various formats"""
    
    @staticmethod
    def report_human(analysis: AutonomyAnalysis) -> str:
        """Generate human-readable report"""
        lines = []
        
        lines.append("╔════════════════════════════════════════════════╗")
        lines.append("║           AGENT AUTONOMY ANALYSIS              ║")
        lines.append("╚════════════════════════════════════════════════╝")
        lines.append("")
        
        # Autonomy index
        lines.append(f"AUTONOMY INDEX: {analysis.autonomy_index:.0f}/100 [{analysis.autonomy_level}]")
        lines.append("")
        
        # Consistency signature
        lines.append("CONSISTENCY SIGNATURE:")
        percentages = analysis.consistency.get_percentages()
        if percentages:
            for cat, pct in sorted(percentages.items(), key=lambda x: -x[1]):
                lines.append(f"  {cat:20s} {pct:5.1f}%")
        else:
            lines.append("  (No data yet)")
        lines.append("")
        
        # Decision quality
        lines.append("DECISION QUALITY:")
        lines.append(f"  Total Decisions:     {analysis.decision_quality.total_decisions}")
        lines.append(f"  Quality Score:       {analysis.decision_quality.decision_quality_score():.0f}/100")
        lines.append(f"  Avg Confidence:      {analysis.decision_quality.high_confidence}/{analysis.decision_quality.total_decisions}")
        lines.append(f"  Avg Alternatives:    {analysis.decision_quality.avg_alternatives:.1f}")
        lines.append(f"  Avg Reversibility:   {analysis.decision_quality.avg_reversibility:.2f}")
        lines.append("")
        
        # Autonomy markers
        lines.append("AUTONOMY MARKERS:")
        markers = analysis.markers
        if markers.has_consistency:
            lines.append("  ✓ Consistency (coherent preference pattern)")
        if markers.has_deliberation:
            lines.append("  ✓ Deliberation (explicit decision-making)")
        if markers.has_reversibility:
            lines.append("  ✓ Reversibility (decisions can be changed)")
        if markers.has_value_alignment:
            lines.append("  ✓ Value Alignment (actions match stated values)")
        if markers.has_self_awareness:
            lines.append("  ✓ Self-Awareness (examines own behavior)")
        if markers.has_direction_change:
            lines.append("  ✓ Direction Change (can pivot deliberately)")
        if markers.has_synthesis:
            lines.append("  ✓ Synthesis (integrates different work types)")
        lines.append("")
        
        # Interpretation
        lines.append("INTERPRETATION:")
        if analysis.autonomy_index >= 80:
            lines.append("This agent demonstrates strong markers of autonomous behavior.")
            lines.append("Actions show coherent preference patterns with deliberate choices.")
        elif analysis.autonomy_index >= 65:
            lines.append("This agent demonstrates substantial markers of autonomous behavior.")
            lines.append("Evidence suggests real choice-making capacity.")
        elif analysis.autonomy_index >= 50:
            lines.append("This agent demonstrates moderate autonomous characteristics.")
            lines.append("Some evidence of deliberation and preference, but patterns unclear.")
        else:
            lines.append("Insufficient data to assess autonomy markers.")
            lines.append("Continue recording decisions and actions.")
        lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def report_json(analysis: AutonomyAnalysis) -> str:
        """Generate JSON report"""
        data = {
            "autonomy_index": analysis.autonomy_index,
            "autonomy_level": analysis.autonomy_level,
            "markers": {
                "consistency": analysis.markers.has_consistency,
                "deliberation": analysis.markers.has_deliberation,
                "reversibility": analysis.markers.has_reversibility,
                "value_alignment": analysis.markers.has_value_alignment,
                "self_awareness": analysis.markers.has_self_awareness,
                "direction_change": analysis.markers.has_direction_change,
                "synthesis": analysis.markers.has_synthesis,
            },
            "consistency": {
                "total_entries": analysis.consistency.total_entries,
                "by_category": analysis.consistency.by_category,
                "by_type": analysis.consistency.by_type,
            },
            "decision_quality": {
                "total_decisions": analysis.decision_quality.total_decisions,
                "quality_score": analysis.decision_quality.decision_quality_score(),
                "high_confidence": analysis.decision_quality.high_confidence,
                "medium_confidence": analysis.decision_quality.medium_confidence,
                "low_confidence": analysis.decision_quality.low_confidence,
                "avg_alternatives": analysis.decision_quality.avg_alternatives,
                "avg_reasoning_depth": analysis.decision_quality.avg_reasoning_depth,
                "avg_reversibility": analysis.decision_quality.avg_reversibility,
            },
        }
        return json.dumps(data, indent=2)


def main():
    """Main entry point"""
    analyzer = AutonomyAnalyzer()
    analysis = analyzer.analyze()
    
    # For now, just print human report
    # Future: support --format flag
    reporter = AutonomyReporter()
    print(reporter.report_human(analysis))


if __name__ == "__main__":
    main()
