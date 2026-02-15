#!/usr/bin/env python3
"""
Decision Outcome Tracker - Activate the learning loop

Records what actually happened when a decision was made.
Enables the decision-making system to learn and improve from experience.

This is the missing piece: synthesis is valuable only if it actually leads
to better outcomes. This tool measures that.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class OutcomeRecord:
    """Records what actually happened after a decision"""
    decision_id: str
    decision_question: str
    chosen_approach: str  # What we actually did
    outcome_description: str  # What actually happened
    success_rating: int  # 1-5 scale: how well did it work?
    time_to_judge: str  # "immediate", "short_term" (days), "medium_term" (weeks), "long_term" (months)
    surprising: bool = False  # Was the outcome unexpected?
    learned: Optional[str] = None  # What did we learn?
    would_choose_again: Optional[bool] = None  # Would we make the same choice?
    created: Optional[str] = None
    
    def __post_init__(self):
        if self.created is None:
            self.created = datetime.now().isoformat()


class OutcomeTracker:
    """
    Tracks outcomes of decisions.
    
    This enables the system to learn: Did synthesis actually help?
    Did integration lead to better results than choosing one option?
    """
    
    def __init__(self, outcomes_file: Path = None):
        if outcomes_file is None:
            outcomes_file = Path(__file__).parent.parent / '.decisions' / 'decision_outcomes.json'
        
        self.outcomes_file = outcomes_file
        self.outcomes = self._load_outcomes()
    
    def _load_outcomes(self) -> Dict[str, List[OutcomeRecord]]:
        """Load all outcome records"""
        if self.outcomes_file.exists():
            with open(self.outcomes_file, 'r') as f:
                data = json.load(f)
                # Convert dicts back to OutcomeRecord objects
                return {
                    decision_id: [OutcomeRecord(**outcome) for outcome in outcomes]
                    for decision_id, outcomes in data.items()
                }
        return {}
    
    def _save_outcomes(self):
        """Persist outcomes to disk"""
        self.outcomes_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            decision_id: [asdict(outcome) for outcome in outcomes]
            for decision_id, outcomes in self.outcomes.items()
        }
        with open(self.outcomes_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def record_outcome(self, decision_id: str, decision_question: str,
                       chosen_approach: str, outcome_description: str,
                       success_rating: int, time_to_judge: str,
                       surprising: bool = False, learned: str = None,
                       would_choose_again: bool = None) -> OutcomeRecord:
        """Record an outcome for a decision"""
        
        if success_rating < 1 or success_rating > 5:
            raise ValueError("Success rating must be 1-5")
        
        outcome = OutcomeRecord(
            decision_id=decision_id,
            decision_question=decision_question,
            chosen_approach=chosen_approach,
            outcome_description=outcome_description,
            success_rating=success_rating,
            time_to_judge=time_to_judge,
            surprising=surprising,
            learned=learned,
            would_choose_again=would_choose_again
        )
        
        if decision_id not in self.outcomes:
            self.outcomes[decision_id] = []
        
        self.outcomes[decision_id].append(outcome)
        self._save_outcomes()
        
        return outcome
    
    def get_outcomes_for_decision(self, decision_id: str) -> List[OutcomeRecord]:
        """Get all outcomes for a specific decision"""
        return self.outcomes.get(decision_id, [])
    
    def get_all_outcomes(self) -> Dict[str, List[OutcomeRecord]]:
        """Get all recorded outcomes"""
        return self.outcomes


class LearningAnalyzer:
    """
    Analyze outcomes to learn what works.
    
    Questions it answers:
    - Which synthesis approaches have worked best?
    - Are we making decisions we'd make again?
    - What patterns emerge in successful outcomes?
    - What surprised us? (Insight opportunity)
    """
    
    def __init__(self, tracker: OutcomeTracker):
        self.tracker = tracker
    
    def get_success_stats(self) -> Dict[str, Any]:
        """
        Overall statistics on decision success.
        
        Returns average success rating, success distribution, etc.
        """
        outcomes = self.tracker.get_all_outcomes()
        
        if not outcomes:
            return {
                'status': 'No outcomes recorded yet',
                'total_decisions_with_outcomes': 0,
                'total_outcome_records': 0
            }
        
        all_records = []
        for decision_id, records in outcomes.items():
            all_records.extend(records)
        
        if not all_records:
            return {
                'status': 'No outcome records',
                'total_decisions_with_outcomes': len(outcomes)
            }
        
        ratings = [r.success_rating for r in all_records]
        would_again = [r.would_choose_again for r in all_records if r.would_choose_again is not None]
        
        return {
            'total_outcomes_recorded': len(all_records),
            'decisions_with_outcomes': len(outcomes),
            'average_success_rating': sum(ratings) / len(ratings),
            'median_success_rating': sorted(ratings)[len(ratings) // 2],
            'highest_rating': max(ratings),
            'lowest_rating': min(ratings),
            'ratings_distribution': {
                '5_excellent': ratings.count(5),
                '4_good': ratings.count(4),
                '3_okay': ratings.count(3),
                '2_poor': ratings.count(2),
                '1_failure': ratings.count(1)
            },
            'would_choose_again_rate': (
                sum(1 for w in would_again if w) / len(would_again) * 100
                if would_again else None
            ),
            'surprising_outcomes': len([r for r in all_records if r.surprising])
        }
    
    def get_timing_analysis(self) -> Dict[str, int]:
        """How soon do we typically know if a decision worked?"""
        outcomes = self.tracker.get_all_outcomes()
        all_records = []
        for decision_id, records in outcomes.items():
            all_records.extend(records)
        
        timing_counts = {}
        for record in all_records:
            timing = record.time_to_judge
            timing_counts[timing] = timing_counts.get(timing, 0) + 1
        
        return timing_counts
    
    def get_surprising_outcomes(self) -> List[Dict[str, Any]]:
        """Find outcomes that surprised us - learning opportunities"""
        outcomes = self.tracker.get_all_outcomes()
        all_records = []
        for decision_id, records in outcomes.items():
            all_records.extend(records)
        
        surprising = [
            {
                'question': r.decision_question,
                'outcome': r.outcome_description,
                'learned': r.learned,
                'rating': r.success_rating
            }
            for r in all_records if r.surprising
        ]
        
        return surprising
    
    def get_learning_insights(self) -> List[str]:
        """Generate insights from the outcome data"""
        insights = []
        
        stats = self.get_success_stats()
        
        if stats.get('status'):
            return ["No outcomes recorded yet. Record some decision outcomes to start learning!"]
        
        total = stats.get('total_outcomes_recorded', 0)
        avg_rating = stats.get('average_success_rating')
        
        if total == 0:
            return ["No outcomes recorded yet."]
        
        insights.append(f"Based on {total} recorded outcomes:")
        
        if avg_rating:
            if avg_rating >= 4.0:
                insights.append("✓ Decisions are working well (average rating ≥ 4.0)")
            elif avg_rating >= 3.0:
                insights.append("~ Decisions are working moderately (average rating 3.0-4.0)")
            else:
                insights.append("✗ Decisions need attention (average rating < 3.0)")
        
        would_again = stats.get('would_choose_again_rate')
        if would_again is not None:
            insights.append(f"→ {would_again:.0f}% of decisions we'd make again")
        
        surprising = stats.get('surprising_outcomes', 0)
        if surprising > 0:
            insights.append(f"★ {surprising} outcomes were surprising - learning opportunities!")
        
        return insights
    
    def generate_learning_report(self) -> str:
        """Generate a comprehensive learning report"""
        lines = []
        lines.append("\n" + "=" * 70)
        lines.append("DECISION LEARNING REPORT")
        lines.append("=" * 70 + "\n")
        
        stats = self.get_success_stats()
        
        lines.append("OUTCOME STATISTICS:")
        lines.append(f"  Total outcomes recorded: {stats.get('total_outcomes_recorded', 0)}")
        lines.append(f"  Decisions with outcomes: {stats.get('decisions_with_outcomes', 0)}")
        
        if stats.get('average_success_rating'):
            lines.append(f"\nSUCCESS RATINGS:")
            lines.append(f"  Average: {stats['average_success_rating']:.2f} / 5.0")
            lines.append(f"  Median: {stats['median_success_rating']}")
            lines.append(f"  Range: {stats['lowest_rating']} - {stats['highest_rating']}")
            
            dist = stats['ratings_distribution']
            lines.append(f"\n  Distribution:")
            lines.append(f"    5 (Excellent): {dist['5_excellent']}")
            lines.append(f"    4 (Good):      {dist['4_good']}")
            lines.append(f"    3 (Okay):      {dist['3_okay']}")
            lines.append(f"    2 (Poor):      {dist['2_poor']}")
            lines.append(f"    1 (Failure):   {dist['1_failure']}")
        
        if stats.get('would_choose_again_rate') is not None:
            lines.append(f"\nDECISION QUALITY:")
            lines.append(f"  Would choose same approach again: {stats['would_choose_again_rate']:.1f}%")
        
        timing = self.get_timing_analysis()
        if timing:
            lines.append(f"\nTIMING OF JUDGMENT:")
            for time_period, count in timing.items():
                lines.append(f"  {time_period}: {count}")
        
        insights = self.get_learning_insights()
        lines.append(f"\nKEY INSIGHTS:")
        for insight in insights:
            lines.append(f"  {insight}")
        
        surprising = self.get_surprising_outcomes()
        if surprising:
            lines.append(f"\nSURPRISING OUTCOMES ({len(surprising)}):")
            for i, outcome in enumerate(surprising[:5], 1):
                lines.append(f"  {i}. {outcome['question']}")
                lines.append(f"     Result: {outcome['outcome']}")
                if outcome.get('learned'):
                    lines.append(f"     Learned: {outcome['learned']}")
        
        lines.append("\n" + "=" * 70 + "\n")
        
        return "\n".join(lines)


def main():
    """Quick demo"""
    tracker = OutcomeTracker()
    analyzer = LearningAnalyzer(tracker)
    
    print(analyzer.generate_learning_report())


if __name__ == '__main__':
    main()
