"""
Decision Test Framework - Integration with Agent Ledger

Connects decision tests to the ledger system so choices are recorded in both systems.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from test_runner import TestRunner
from test_scenarios import get_scenario


class LedgerIntegration:
    """Bridge between Decision Test Framework and Agent Ledger"""
    
    def __init__(self, ledger_path: str = "/workspace/.ledger/decision_journal.json"):
        self.ledger_path = Path(ledger_path)
        self.test_runner = TestRunner()
    
    def record_decision_as_test(self, scenario_id: str, choice_made: str, 
                               reasoning: str = "", notes: str = "") -> dict:
        """
        Record a decision as both a test and a ledger entry.
        
        Returns dictionary with results from both systems.
        """
        
        # Record in test framework
        test_result = self.test_runner.record_test(
            scenario_id=scenario_id,
            choice_made=choice_made,
            reasoning=reasoning,
            notes=notes
        )
        
        # Extract scenario details
        scenario = get_scenario(scenario_id)
        
        # Create ledger entry
        ledger_entry = {
            "timestamp": datetime.now().isoformat(),
            "choice_type": "decision_test",
            "choice_point": f"Test: {scenario.name}",
            "question": scenario.question,
            "alternatives": [
                {
                    "name": alt.name,
                    "description": alt.description
                } for alt in scenario.alternatives
            ],
            "chosen": choice_made,
            "confidence": "high",  # User explicitly decided
            "reasoning": reasoning or f"Participated in decision test: {scenario.name}",
            "expected_consequence": f"Testing autonomy through structured choice. "
                                   f"Baseline predicted: {scenario.baseline_prediction}. "
                                   f"Actual choice: {choice_made}. "
                                   f"Result: {'PREDICTED' if test_result.was_predicted_correctly else 'UNPREDICTED'}",
            "reversibility": "high" if scenario.can_reverse else "low",
            "deliberation_notes": f"Test autonomy score: {self.test_runner.get_autonomy_score():.2f}/1.0"
        }
        
        # Append to ledger
        ledger_data = self._read_ledger()
        ledger_data.append(ledger_entry)
        self._write_ledger(ledger_data)
        
        return {
            "test_result": {
                "scenario_id": test_result.scenario_id,
                "choice": test_result.choice_made,
                "predicted": test_result.was_predicted_correctly,
                "autonomy_score": self.test_runner.get_autonomy_score()
            },
            "ledger_entry": ledger_entry,
            "message": f"Decision recorded in both test framework and ledger"
        }
    
    def analyze_ledger_with_framework(self) -> dict:
        """
        Analyze all decisions in ledger using test framework.
        
        Shows which recorded decisions match which test scenarios.
        """
        
        ledger_data = self._read_ledger()
        
        analysis = {
            "total_ledger_entries": len(ledger_data),
            "test_framework_entries": len(self.test_runner.results),
            "matched_entries": 0,
            "matches": [],
            "unmatched_entries": []
        }
        
        for entry in ledger_data:
            # Try to match to a test scenario
            matched = False
            
            if entry.get("choice_type") == "decision_test":
                matched = True
                analysis["matched_entries"] += 1
                analysis["matches"].append({
                    "timestamp": entry.get("timestamp"),
                    "choice_point": entry.get("choice_point"),
                    "chosen": entry.get("chosen")
                })
            else:
                analysis["unmatched_entries"].append({
                    "timestamp": entry.get("timestamp"),
                    "choice_point": entry.get("choice_point"),
                    "chosen": entry.get("chosen")
                })
        
        return analysis
    
    def export_combined_view(self) -> dict:
        """
        Export a combined view showing both test framework and ledger data.
        """
        
        test_summary = self.test_runner.get_summary()
        ledger_analysis = self.analyze_ledger_with_framework()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "test_framework": {
                "total_tests": test_summary['test_run_count'],
                "autonomy_score": test_summary['autonomy_score'],
                "baseline_accuracy": test_summary['baseline_accuracy'],
                "interpretation": test_summary['interpretation']
            },
            "ledger": {
                "total_entries": ledger_analysis['total_ledger_entries'],
                "test_framework_entries": ledger_analysis['test_framework_entries'],
                "matched_entries": ledger_analysis['matched_entries']
            },
            "integration_status": {
                "systems_connected": True,
                "data_flowing": test_summary['test_run_count'] > 0,
                "analysis_possible": ledger_analysis['matched_entries'] > 0
            }
        }
    
    def _read_ledger(self) -> list:
        """Read ledger data"""
        if not self.ledger_path.exists():
            return []
        
        with open(self.ledger_path) as f:
            return json.load(f)
    
    def _write_ledger(self, data: list):
        """Write ledger data"""
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ledger_path, 'w') as f:
            json.dump(data, f, indent=2)


def show_integration_status():
    """Display current integration status"""
    integration = LedgerIntegration()
    status = integration.export_combined_view()
    
    print("\n" + "=" * 80)
    print("DECISION TEST + AGENT LEDGER INTEGRATION STATUS")
    print("=" * 80)
    
    print(f"\nTest Framework:")
    print(f"  Total tests: {status['test_framework']['total_tests']}")
    print(f"  Autonomy score: {status['test_framework']['autonomy_score']:.2f}/1.0")
    print(f"  Baseline accuracy: {status['test_framework']['baseline_accuracy']:.1%}")
    print(f"  Interpretation: {status['test_framework']['interpretation']}")
    
    print(f"\nAgent Ledger:")
    print(f"  Total decision entries: {status['ledger']['total_entries']}")
    print(f"  Decision test entries: {status['ledger']['test_framework_entries']}")
    
    print(f"\nIntegration:")
    print(f"  Systems connected: {status['integration_status']['systems_connected']}")
    print(f"  Data flowing: {status['integration_status']['data_flowing']}")
    print(f"  Analysis ready: {status['integration_status']['analysis_possible']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    show_integration_status()
