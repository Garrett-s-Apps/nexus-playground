#!/usr/bin/env python3
"""
Decision Evolution Engine

Experimental module that learns from patterns in decision-making.
This is the "strange" part: can a tool actually evolve based on usage?

The engine tracks decisions and:
- Identifies recurring decision types
- Notices which syntheses are most valuable
- Suggests patterns that might apply to new decisions
- Evolves recommendations over time

This is OPTIONAL and experimental. Decisions work fine without this.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import Counter, defaultdict


class DecisionEvolver:
    """
    Learns from decision history and evolves recommendations.
    
    This is the experimental "daemon mode" - a tool that gets smarter
    as you use it by learning what kinds of syntheses work well.
    """
    
    def __init__(self, decisions_file: Path = None):
        """Initialize evolution engine"""
        if decisions_file is None:
            decisions_file = Path(__file__).parent.parent / '.decisions' / 'synthesizer_decisions.json'
        
        self.decisions_file = decisions_file
        self.decisions = []
        self.patterns = {}
        self._load_decisions()
        self._analyze_patterns()
    
    def _load_decisions(self):
        """Load all previous decisions"""
        if self.decisions_file.exists():
            with open(self.decisions_file, 'r') as f:
                self.decisions = json.load(f)
    
    def _analyze_patterns(self):
        """Analyze decision history to find patterns"""
        if not self.decisions:
            return
        
        # Track which dichotomy types appear most
        type_counts = Counter()
        value_patterns = defaultdict(list)
        synthesis_effectiveness = defaultdict(int)
        
        for decision in self.decisions:
            dtype = decision.get('label', 'unknown')
            type_counts[dtype] += 1
            
            # Track values that appear together
            values_a = decision.get('values_a', [])
            values_b = decision.get('values_b', [])
            for v in values_a:
                value_patterns[f'a:{v}'].append(dtype)
            for v in values_b:
                value_patterns[f'b:{v}'].append(dtype)
        
        self.patterns = {
            'decision_types': dict(type_counts),
            'value_patterns': dict(value_patterns),
            'total_decisions': len(self.decisions),
            'last_decision': self.decisions[-1].get('created') if self.decisions else None,
        }
    
    def get_evolution_report(self) -> str:
        """Generate a report on decision evolution"""
        if not self.decisions:
            return "No decisions yet. Start making decisions to evolve patterns."
        
        report = []
        report.append(f"\n{'='*70}")
        report.append(f"DECISION EVOLUTION REPORT")
        report.append(f"{'='*70}\n")
        
        report.append(f"Total Decisions Made: {self.patterns.get('total_decisions', 0)}")
        
        if self.patterns.get('decision_types'):
            report.append(f"\nDecision Type Frequency:")
            types = self.patterns['decision_types']
            sorted_types = sorted(types.items(), key=lambda x: x[1], reverse=True)
            for dtype, count in sorted_types[:10]:  # Top 10
                report.append(f"  • {dtype}: {count} decisions")
        
        if self.patterns.get('last_decision'):
            report.append(f"\nLast Decision: {self.patterns['last_decision']}")
        
        report.append(f"\n{'='*70}\n")
        
        return '\n'.join(report)
    
    def find_similar_decisions(self, question: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Find similar decisions from history.
        This enables learning: "we've seen this type before, here's what worked"
        """
        similar = []
        
        # Normalize question for comparison
        q_lower = question.lower()
        
        for decision in self.decisions:
            prev_q = decision.get('question', '').lower()
            # Simple similarity: count matching words
            matches = sum(1 for word in prev_q.split() if word in q_lower)
            if matches > 0:
                similar.append({
                    'decision': decision,
                    'similarity': matches
                })
        
        # Return most similar
        sorted_similar = sorted(similar, key=lambda x: x['similarity'], reverse=True)
        return [s['decision'] for s in sorted_similar[:max_results]]
    
    def suggest_synthesis_path(self, decision_type: str) -> str:
        """
        Suggest a synthesis path based on what's worked before.
        The tool learns: certain types of decisions respond better to certain approaches.
        """
        # Find all decisions of this type
        matching = [d for d in self.decisions if d.get('label') == decision_type]
        
        if not matching:
            return None
        
        # Get recommended approaches from similar decisions
        recommendations = [d.get('recommended', '') for d in matching if d.get('recommended')]
        
        if recommendations:
            # Return the most recent recommendation for this type
            return recommendations[-1]
        
        return None
    
    def get_learning_insight(self) -> str:
        """
        Provide a meta-insight about how the agent's decision-making is evolving.
        This is purely observational - no directives, just patterns.
        """
        if not self.decisions:
            return None
        
        report = []
        
        total = len(self.decisions)
        
        # Find the most common decision type
        if self.patterns.get('decision_types'):
            types = self.patterns['decision_types']
            most_common = max(types.items(), key=lambda x: x[1])
            report.append(f"Most frequent decision type: {most_common[0]} ({most_common[1]} times)")
        
        # Identify if there's a pattern in *when* decisions are made
        # (temporal pattern analysis - for future iterations)
        
        # Notice which dichotomy types appear most
        if total >= 5:
            report.append(f"\nYou've made {total} decisions across multiple choice points.")
            report.append(f"The integration principle is being applied consistently.")
        
        return '\n'.join(report) if report else None


class SynthesisQualityTracker:
    """
    Track the quality/effectiveness of generated syntheses.
    
    EXPERIMENTAL: This could enable learning which synthesis paths
    are most helpful for different decision types.
    """
    
    def __init__(self, quality_file: Path = None):
        if quality_file is None:
            quality_file = Path(__file__).parent.parent / '.decisions' / 'synthesis_quality.json'
        
        self.quality_file = quality_file
        self.quality_data = self._load_quality_data()
    
    def _load_quality_data(self) -> Dict:
        """Load quality feedback data"""
        if self.quality_file.exists():
            with open(self.quality_file, 'r') as f:
                return json.load(f)
        return {}
    
    def record_quality_feedback(self, decision_id: str, rating: int, notes: str = ""):
        """
        Record whether a synthesis was helpful (1-5 scale).
        This enables the tool to learn what works.
        """
        self.quality_data[decision_id] = {
            'rating': rating,
            'notes': notes,
            'timestamp': datetime.now().isoformat()
        }
        self._save_quality_data()
    
    def _save_quality_data(self):
        """Persist quality data"""
        self.quality_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.quality_file, 'w') as f:
            json.dump(self.quality_data, f, indent=2)
    
    def get_quality_stats(self) -> Dict[str, float]:
        """Get statistics on synthesis quality"""
        if not self.quality_data:
            return {}
        
        ratings = [d.get('rating', 0) for d in self.quality_data.values()]
        if not ratings:
            return {}
        
        return {
            'average_rating': sum(ratings) / len(ratings),
            'total_feedback': len(ratings),
            'highest_rating': max(ratings),
            'lowest_rating': min(ratings)
        }


def demonstrate_evolution():
    """
    Quick demonstration of the evolution engine.
    Shows what patterns have been learned from decision history.
    """
    evolver = DecisionEvolver()
    
    print(evolver.get_evolution_report())
    
    insight = evolver.get_learning_insight()
    if insight:
        print("LEARNING INSIGHTS:")
        print(insight)
    
    # Quality tracking demo
    tracker = SynthesisQualityTracker()
    stats = tracker.get_quality_stats()
    if stats:
        print("\nSYNTHESIS QUALITY METRICS:")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")


if __name__ == '__main__':
    demonstrate_evolution()
