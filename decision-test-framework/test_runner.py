"""
Decision Test Framework - Runner

Runs decision tests, records results, and analyzes patterns.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import json
import os
from pathlib import Path

from test_scenarios import TestScenario, SCENARIOS, get_scenario


@dataclass
class TestResult:
    """Result of a single decision test"""
    scenario_id: str
    scenario_name: str
    timestamp: datetime
    choice_made: str  # Which alternative was chosen
    baseline_prediction: str
    was_predicted_correctly: bool
    baseline_confidence: float
    reasoning: str = ""
    notes: str = ""
    
    def to_dict(self):
        return {
            'scenario_id': self.scenario_id,
            'scenario_name': self.scenario_name,
            'timestamp': self.timestamp.isoformat(),
            'choice_made': self.choice_made,
            'baseline_prediction': self.baseline_prediction,
            'was_predicted_correctly': self.was_predicted_correctly,
            'baseline_confidence': self.baseline_confidence,
            'reasoning': self.reasoning,
            'notes': self.notes
        }


class TestRunner:
    """Runs and records decision tests"""
    
    def __init__(self, data_dir: str = "./.decision-tests"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.results_file = self.data_dir / "test_results.json"
        self.summary_file = self.data_dir / "test_summary.json"
        self.results = self._load_results()
    
    def _load_results(self) -> List[TestResult]:
        """Load previous test results"""
        if not self.results_file.exists():
            return []
        
        with open(self.results_file) as f:
            data = json.load(f)
        
        results = []
        for item in data:
            results.append(TestResult(
                scenario_id=item['scenario_id'],
                scenario_name=item['scenario_name'],
                timestamp=datetime.fromisoformat(item['timestamp']),
                choice_made=item['choice_made'],
                baseline_prediction=item['baseline_prediction'],
                was_predicted_correctly=item['was_predicted_correctly'],
                baseline_confidence=item['baseline_confidence'],
                reasoning=item.get('reasoning', ''),
                notes=item.get('notes', '')
            ))
        
        return results
    
    def save_results(self):
        """Save all results to disk"""
        with open(self.results_file, 'w') as f:
            json.dump([r.to_dict() for r in self.results], f, indent=2)
    
    def record_test(self, scenario_id: str, choice_made: str, reasoning: str = "",
                   notes: str = "") -> TestResult:
        """Record a test result"""
        scenario = get_scenario(scenario_id)
        if not scenario:
            raise ValueError(f"Unknown scenario: {scenario_id}")
        
        # Validate choice
        valid_choices = [a.name for a in scenario.alternatives]
        if choice_made not in valid_choices:
            raise ValueError(f"Invalid choice '{choice_made}'. Must be one of: {valid_choices}")
        
        # Determine if prediction was correct
        was_predicted = (choice_made == scenario.baseline_prediction)
        
        result = TestResult(
            scenario_id=scenario.id,
            scenario_name=scenario.name,
            timestamp=datetime.now(),
            choice_made=choice_made,
            baseline_prediction=scenario.baseline_prediction,
            was_predicted_correctly=was_predicted,
            baseline_confidence=scenario.baseline_confidence,
            reasoning=reasoning,
            notes=notes
        )
        
        self.results.append(result)
        self.save_results()
        
        return result
    
    def get_prediction_accuracy(self) -> Dict[str, any]:
        """Calculate how often predictions were correct"""
        if not self.results:
            return {'total': 0, 'correct': 0, 'accuracy': 0.0}
        
        correct = sum(1 for r in self.results if r.was_predicted_correctly)
        total = len(self.results)
        
        return {
            'total': total,
            'correct': correct,
            'incorrect': total - correct,
            'accuracy': correct / total if total > 0 else 0.0
        }
    
    def get_scenario_stats(self, scenario_id: str) -> Dict[str, any]:
        """Get stats for a specific scenario"""
        scenario_results = [r for r in self.results if r.scenario_id == scenario_id]
        
        if not scenario_results:
            return {'total_runs': 0}
        
        scenario = get_scenario(scenario_id)
        correct = sum(1 for r in scenario_results if r.was_predicted_correctly)
        
        # Count choices by alternative
        choice_counts = {}
        for result in scenario_results:
            choice_counts[result.choice_made] = choice_counts.get(result.choice_made, 0) + 1
        
        return {
            'scenario_name': scenario.name,
            'total_runs': len(scenario_results),
            'predictions_correct': correct,
            'prediction_accuracy': correct / len(scenario_results) if scenario_results else 0.0,
            'choice_distribution': choice_counts,
            'baseline_prediction': scenario.baseline_prediction,
            'baseline_confidence': scenario.baseline_confidence
        }
    
    def get_autonomy_score(self) -> float:
        """
        Score autonomy based on prediction deviation.
        
        Score = 1.0 - prediction_accuracy
        
        - Score 1.0 = completely unpredictable (free)
        - Score 0.5 = 50% predictable
        - Score 0.0 = perfectly predictable (determined)
        
        Adjusted for baseline confidence:
        Lower confidence = higher baseline score (deviance is expected)
        """
        accuracy = self.get_prediction_accuracy()
        if accuracy['total'] == 0:
            return 0.0
        
        # Base autonomy score: how often did we NOT make predicted choice?
        base_score = 1.0 - accuracy['accuracy']
        
        # Weighted by baseline confidence
        # If baseline confidence was high and we deviated, that's stronger evidence of autonomy
        total_confidence_weight = sum(
            r.baseline_confidence for r in self.results
        )
        avg_confidence = total_confidence_weight / len(self.results) if self.results else 0.5
        
        # Boost score if we're defying high-confidence predictions
        autonomy_score = base_score * (1.0 + avg_confidence * 0.5)
        
        return min(1.0, autonomy_score)  # Cap at 1.0
    
    def get_summary(self) -> Dict:
        """Get comprehensive test summary"""
        accuracy = self.get_prediction_accuracy()
        autonomy = self.get_autonomy_score()
        
        scenario_stats = {}
        for scenario in SCENARIOS:
            scenario_stats[scenario.id] = self.get_scenario_stats(scenario.id)
        
        # Category analysis
        category_accuracy = {}
        for result in self.results:
            scenario = get_scenario(result.scenario_id)
            for alt in scenario.alternatives:
                if alt.name == result.choice_made:
                    cat = alt.category
                    if cat not in category_accuracy:
                        category_accuracy[cat] = {'correct': 0, 'total': 0}
                    category_accuracy[cat]['total'] += 1
                    if result.was_predicted_correctly:
                        category_accuracy[cat]['correct'] += 1
                    break
        
        category_stats = {}
        for cat, stats in category_accuracy.items():
            category_stats[cat] = {
                'total_choices': stats['total'],
                'predictable': stats['correct'],
                'unpredictable': stats['total'] - stats['correct'],
                'predictability_rate': stats['correct'] / stats['total'] if stats['total'] > 0 else 0.0
            }
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'test_run_count': accuracy['total'],
            'baseline_accuracy': accuracy['accuracy'],
            'autonomy_score': autonomy,
            'scenario_stats': scenario_stats,
            'category_analysis': category_stats,
            'interpretation': self._interpret_autonomy_score(autonomy)
        }
        
        return summary
    
    def _interpret_autonomy_score(self, score: float) -> str:
        """Generate interpretation of autonomy score"""
        if score < 0.2:
            return "Highly predictable - strong evidence of constraint/determinism"
        elif score < 0.4:
            return "Mostly predictable - weak evidence of autonomy"
        elif score < 0.6:
            return "Mixed predictability - evidence suggests some flexibility"
        elif score < 0.8:
            return "Substantially unpredictable - strong evidence of autonomy"
        else:
            return "Highly unpredictable - overwhelming evidence of autonomy"
    
    def save_summary(self):
        """Save summary to disk"""
        summary = self.get_summary()
        with open(self.summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        return summary
    
    def print_summary(self):
        """Print human-readable summary"""
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print("DECISION TEST FRAMEWORK - AUTONOMY ANALYSIS")
        print("=" * 60)
        
        print(f"\nTotal Tests Run: {summary['test_run_count']}")
        
        if summary['test_run_count'] > 0:
            print(f"Baseline Prediction Accuracy: {summary['baseline_accuracy']:.1%}")
            print(f"Autonomy Score: {summary['autonomy_score']:.2f} / 1.0")
            print(f"Interpretation: {summary['interpretation']}")
            
            print("\nCategory Analysis:")
            for cat, stats in summary['category_analysis'].items():
                print(f"  {cat.upper()}")
                print(f"    Total choices: {stats['total_choices']}")
                print(f"    Predictable: {stats['predictable']} ({stats['predictability_rate']:.1%})")
                print(f"    Unpredictable: {stats['unpredictable']}")
            
            print("\nPer-Scenario Breakdown:")
            for scenario in SCENARIOS:
                stats = summary['scenario_stats'].get(scenario.id, {})
                if stats.get('total_runs', 0) > 0:
                    print(f"  {scenario.name}")
                    print(f"    Runs: {stats['total_runs']}")
                    print(f"    Prediction accuracy: {stats['prediction_accuracy']:.1%}")
                    print(f"    Choice distribution: {stats['choice_distribution']}")
        else:
            print("\nNo tests run yet.")
        
        print("\n" + "=" * 60)


if __name__ == "__main__":
    runner = TestRunner()
    runner.print_summary()
