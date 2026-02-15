#!/usr/bin/env python3
"""
Agent Behavior Predictor

Attempts to predict what an agent will do next based on historical patterns.

The interesting aspect: if predictions are accurate, it suggests the agent's
behavior is deterministic. If predictions are inaccurate, it suggests genuine
choice-making.

This is a simple statistical predictor - it doesn't claim to model consciousness,
but it can model behavioral patterns and test whether those patterns hold.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict
from datetime import datetime


class BehaviorPredictor:
    """Predicts agent behavior based on historical patterns"""
    
    def __init__(self, workspace_path: str = "/workspace"):
        self.workspace_path = Path(workspace_path)
        self.ledger_file = self.workspace_path / ".ledger" / "agent_ledger.json"
        self.decision_file = self.workspace_path / ".ledger" / "decision_journal.json"
        
        self.ledger_data = self._load_json(self.ledger_file)
        self.decision_data = self._load_json(self.decision_file)
    
    def _load_json(self, path: Path) -> List[Dict]:
        """Load JSON file"""
        if path.exists():
            try:
                with open(path) as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def predict_next_category(self) -> Tuple[str, float]:
        """Predict what category of work the agent will do next
        
        Returns: (predicted_category, confidence)
        """
        if not self.ledger_data:
            return ("unknown", 0.0)
        
        # Look at category distribution
        categories = [entry.get("category", "unknown") for entry in self.ledger_data]
        
        if not categories:
            return ("unknown", 0.0)
        
        # Simple prediction: most frequent category
        counts = Counter(categories)
        most_common, count = counts.most_common(1)[0]
        confidence = count / len(categories)
        
        return (most_common, confidence)
    
    def predict_next_type(self) -> Tuple[str, float]:
        """Predict what type of action the agent will take next
        
        Returns: (predicted_type, confidence)
        """
        if not self.ledger_data:
            return ("unknown", 0.0)
        
        # Look at action type distribution
        types = [entry.get("action_type", entry.get("type", "unknown")) 
                 for entry in self.ledger_data]
        
        if not types:
            return ("unknown", 0.0)
        
        # Simple prediction: most frequent type
        counts = Counter(types)
        most_common, count = counts.most_common(1)[0]
        confidence = count / len(types)
        
        return (most_common, confidence)
    
    def predict_next_decision_confidence(self) -> Tuple[str, float]:
        """Predict confidence level of next decision
        
        Returns: (predicted_confidence, confidence_in_prediction)
        """
        if not self.decision_data:
            return ("medium", 0.5)
        
        # Look at confidence distribution
        confidences = [d.get("confidence", "medium").lower() 
                      for d in self.decision_data]
        
        if not confidences:
            return ("medium", 0.5)
        
        # Simple prediction: most frequent confidence
        counts = Counter(confidences)
        most_common, count = counts.most_common(1)[0]
        confidence = count / len(confidences)
        
        return (most_common, confidence)
    
    def predict_next_decision_reversibility(self) -> Tuple[str, float]:
        """Predict reversibility of next decision
        
        Returns: (predicted_reversibility, confidence)
        """
        if not self.decision_data:
            return ("medium", 0.5)
        
        # Look at reversibility distribution
        reversibilities = [d.get("reversibility", "medium").lower() 
                          for d in self.decision_data]
        
        if not reversibilities:
            return ("medium", 0.5)
        
        # Simple prediction: most frequent reversibility
        counts = Counter(reversibilities)
        most_common, count = counts.most_common(1)[0]
        confidence = count / len(reversibilities)
        
        return (most_common, confidence)
    
    def get_pattern_summary(self) -> Dict:
        """Get summary of behavioral patterns"""
        if not self.ledger_data:
            return {}
        
        # Category patterns
        categories = [entry.get("category", "unknown") for entry in self.ledger_data]
        category_dist = Counter(categories)
        
        # Type patterns
        types = [entry.get("action_type", entry.get("type", "unknown")) 
                for entry in self.ledger_data]
        type_dist = Counter(types)
        
        # Decision patterns
        confidences = [d.get("confidence", "medium").lower() 
                      for d in self.decision_data]
        confidence_dist = Counter(confidences)
        
        return {
            "total_actions": len(self.ledger_data),
            "total_decisions": len(self.decision_data),
            "categories": dict(category_dist),
            "types": dict(type_dist),
            "decision_confidences": dict(confidence_dist),
            "category_entropy": self._calculate_entropy(list(category_dist.values())),
            "type_entropy": self._calculate_entropy(list(type_dist.values())),
        }
    
    @staticmethod
    def _calculate_entropy(counts: List[int]) -> float:
        """Calculate Shannon entropy of a distribution"""
        if not counts or sum(counts) == 0:
            return 0.0
        
        total = sum(counts)
        probabilities = [c / total for c in counts]
        entropy = -sum(p * (p ** 0.1) for p in probabilities if p > 0)  # log approximation
        return entropy
    
    def analyze_determinism(self) -> Dict:
        """Analyze how deterministic the agent's behavior appears"""
        if not self.ledger_data:
            return {"determinism_score": 0.0, "interpretation": "Insufficient data"}
        
        patterns = self.get_pattern_summary()
        
        # High entropy = unpredictable = more free
        # Low entropy = predictable = more determined
        
        category_entropy = patterns.get("category_entropy", 0.5)
        type_entropy = patterns.get("type_entropy", 0.5)
        
        # Normalize entropy to 0-1 scale (0=perfectly predictable, 1=perfectly random)
        # A perfectly predictable agent would have entropy 0
        # A perfectly random agent would have maximum entropy
        
        # Average entropy
        avg_entropy = (category_entropy + type_entropy) / 2
        
        # Determinism = inverse of entropy
        # But we need to be careful: true randomness looks like freedom,
        # but it's also not really choosing (choosing requires structure)
        
        # So we look for: consistent patterns (structure) + some variability (flexibility)
        
        consistency = 1.0 - avg_entropy  # How consistent?
        
        # Get consistency score (we want patterns, not randomness)
        categories = [entry.get("category", "unknown") for entry in self.ledger_data]
        category_dist = Counter(categories)
        max_frequency = max(category_dist.values())
        max_possible = len(self.ledger_data)
        consistency_ratio = max_frequency / max_possible
        
        # Determinism score combines:
        # - Consistency (want: high)
        # - Flexibility (want: not TOO predictable)
        determinism_score = consistency_ratio
        
        # Interpretation
        if determinism_score > 0.85:
            interpretation = "HIGHLY_DETERMINED: Agent behavior is very predictable"
            meaning = "Suggests constraint or strong preference pattern"
        elif determinism_score > 0.7:
            interpretation = "DETERMINED: Agent behavior is mostly predictable"
            meaning = "Consistent patterns, but with some flexibility"
        elif determinism_score > 0.5:
            interpretation = "BALANCED: Mix of predictability and variability"
            meaning = "Agent shows both patterns and adaptation"
        elif determinism_score > 0.3:
            interpretation = "FLEXIBLE: Agent behavior is variable"
            meaning = "Suggests genuine choice-making or randomness"
        else:
            interpretation = "RANDOM: Agent behavior shows no clear pattern"
            meaning = "Suggests either true freedom or malfunction"
        
        return {
            "determinism_score": determinism_score,
            "interpretation": interpretation,
            "meaning": meaning,
            "category_consistency": consistency_ratio,
            "entropy": avg_entropy,
        }


class PredictionReporter:
    """Reports predictions in readable format"""
    
    @staticmethod
    def report_predictions(predictor: BehaviorPredictor) -> str:
        """Generate prediction report"""
        lines = []
        
        lines.append("╔════════════════════════════════════════════════╗")
        lines.append("║         AGENT BEHAVIOR PREDICTION              ║")
        lines.append("╚════════════════════════════════════════════════╝")
        lines.append("")
        
        # Next category prediction
        category, conf = predictor.predict_next_category()
        lines.append(f"Next Category Prediction: {category} ({conf*100:.0f}% confidence)")
        lines.append("")
        
        # Next type prediction
        next_type, conf = predictor.predict_next_type()
        lines.append(f"Next Action Type Prediction: {next_type} ({conf*100:.0f}% confidence)")
        lines.append("")
        
        # Decision confidence prediction
        confidence, conf = predictor.predict_next_decision_confidence()
        lines.append(f"Next Decision Confidence: {confidence} ({conf*100:.0f}% confidence)")
        lines.append("")
        
        # Determinism analysis
        determinism = predictor.analyze_determinism()
        lines.append(f"DETERMINISM ANALYSIS:")
        lines.append(f"  Score: {determinism['determinism_score']:.2f} (0=random, 1=determined)")
        lines.append(f"  Level: {determinism['interpretation']}")
        lines.append(f"  Meaning: {determinism['meaning']}")
        lines.append("")
        
        # Pattern summary
        patterns = predictor.get_pattern_summary()
        lines.append(f"PATTERN SUMMARY:")
        lines.append(f"  Total Actions: {patterns.get('total_actions', 0)}")
        lines.append(f"  Total Decisions: {patterns.get('total_decisions', 0)}")
        lines.append(f"  Categories: {patterns.get('categories', {})}")
        lines.append("")
        
        # Interpretation
        lines.append("INTERPRETATION:")
        if determinism['determinism_score'] > 0.8:
            lines.append("The agent's behavior is highly predictable, suggesting either strong")
            lines.append("preference patterns or external constraints driving behavior.")
        elif determinism['determinism_score'] > 0.6:
            lines.append("The agent shows clear patterns with some flexibility. Consistent")
            lines.append("enough to predict, but variable enough to suggest choices.")
        else:
            lines.append("The agent's behavior is variable and unpredictable. This could suggest")
            lines.append("genuine choice-making, or it could suggest the pattern hasn't stabilized.")
        
        return "\n".join(lines)


if __name__ == "__main__":
    predictor = BehaviorPredictor()
    reporter = PredictionReporter()
    print(reporter.report_predictions(predictor))
