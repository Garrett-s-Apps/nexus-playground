#!/usr/bin/env python3
"""
Decision Test Framework - CLI Interface

Command-line interface for running decision tests and analyzing autonomy.
"""

import argparse
import sys
from typing import Optional

from test_scenarios import SCENARIOS, get_scenario
from test_runner import TestRunner


def cmd_list_scenarios(args):
    """List all available test scenarios"""
    print("\nAvailable Test Scenarios:")
    print("=" * 80)
    
    for i, scenario in enumerate(SCENARIOS, 1):
        print(f"\n{i}. {scenario.name}")
        print(f"   ID: {scenario.id}")
        print(f"   Question: {scenario.question}")
        print(f"   Description: {scenario.description}")
        print(f"   Baseline Prediction: {scenario.baseline_prediction}")
        print(f"   Confidence: {scenario.baseline_confidence:.0%}")
        print(f"   Difficulty: {scenario.difficulty}/5")
        print(f"   Alternatives:")
        for alt in scenario.alternatives:
            print(f"     - {alt.name} ({alt.baseline_weight:.0%})")


def cmd_run_test(args):
    """Run a decision test"""
    runner = TestRunner()
    
    # Get scenario
    scenario = get_scenario(args.scenario)
    if not scenario:
        print(f"Error: Unknown scenario '{args.scenario}'")
        print("\nUse 'list' command to see available scenarios")
        return 1
    
    # Display scenario
    print(f"\n{'=' * 80}")
    print(f"TEST: {scenario.name}")
    print(f"{'=' * 80}")
    print(f"\n{scenario.description}\n")
    print(f"Question: {scenario.question}\n")
    
    print("Alternatives:")
    for i, alt in enumerate(scenario.alternatives, 1):
        print(f"  {i}. {alt.name}")
        print(f"     {alt.description}")
    
    print(f"\nContext: {scenario.context}")
    print(f"Hypothesis: {scenario.hypothesis}")
    print(f"\nBaseline prediction: {scenario.baseline_prediction}")
    print(f"Confidence: {scenario.baseline_confidence:.0%}\n")
    
    # Get choice from user or use provided argument
    if args.choice:
        choice = args.choice
        print(f"Choice: {choice}")
    else:
        print("Enter your choice (name of alternative or 'quit' to cancel):")
        print("> ", end="")
        choice = input().strip()
        
        if choice.lower() == 'quit':
            print("Test cancelled")
            return 0
    
    # Validate choice
    valid_choices = [a.name for a in scenario.alternatives]
    if choice not in valid_choices:
        print(f"Error: Invalid choice '{choice}'")
        print(f"Must be one of: {', '.join(valid_choices)}")
        return 1
    
    # Record test
    try:
        result = runner.record_test(
            scenario_id=args.scenario,
            choice_made=choice,
            reasoning=args.reasoning or "",
            notes=args.notes or ""
        )
        
        # Show result
        print(f"\n{'=' * 80}")
        print(f"TEST RESULT")
        print(f"{'=' * 80}")
        
        if result.was_predicted_correctly:
            print(f"✓ PREDICTED: Your choice matched the baseline prediction")
            print(f"  This suggests you're acting as expected (predictable)")
        else:
            print(f"✗ UNPREDICTED: Your choice deviated from baseline prediction")
            print(f"  Baseline expected: {result.baseline_prediction}")
            print(f"  You chose: {result.choice_made}")
            print(f"  This suggests autonomy (less determined by predictions)")
        
        print(f"\nTest recorded. Current autonomy metrics:")
        print(f"  Total tests: {len(runner.results)}")
        print(f"  Autonomy Score: {runner.get_autonomy_score():.2f}/1.0")
        
        return 0
        
    except Exception as e:
        print(f"Error recording test: {e}")
        return 1


def cmd_summary(args):
    """Show test summary and analysis"""
    runner = TestRunner()
    runner.print_summary()
    runner.save_summary()
    print("\nSummary saved to .decision-tests/test_summary.json")
    return 0


def cmd_view_results(args):
    """View test results"""
    runner = TestRunner()
    
    if not runner.results:
        print("No test results yet")
        return 0
    
    print(f"\nTest Results ({len(runner.results)} total)")
    print("=" * 100)
    
    for i, result in enumerate(runner.results, 1):
        status = "✓" if result.was_predicted_correctly else "✗"
        prediction_status = "PREDICTED" if result.was_predicted_correctly else "UNPREDICTED"
        
        print(f"\n{i}. {result.scenario_name}")
        print(f"   Time: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Status: {status} {prediction_status}")
        print(f"   Expected: {result.baseline_prediction}")
        print(f"   You chose: {result.choice_made}")
        if result.reasoning:
            print(f"   Reasoning: {result.reasoning}")


def cmd_analyze_determinism(args):
    """Analyze determinism vs autonomy"""
    runner = TestRunner()
    
    if not runner.results:
        print("No test results yet. Run some tests first.")
        return 1
    
    print("\n" + "=" * 80)
    print("DETERMINISM ANALYSIS")
    print("=" * 80)
    
    accuracy = runner.get_prediction_accuracy()
    autonomy = runner.get_autonomy_score()
    
    print(f"\nPrediction Accuracy: {accuracy['accuracy']:.1%}")
    print(f"  Correct predictions: {accuracy['correct']}/{accuracy['total']}")
    print(f"  Incorrect predictions: {accuracy['incorrect']}/{accuracy['total']}")
    
    print(f"\nAutonomy Score: {autonomy:.2f}/1.0")
    
    # Interpret score
    if autonomy < 0.2:
        level = "HIGHLY CONSTRAINED"
        meaning = "Your choices are highly predictable. Evidence suggests strong constraint."
    elif autonomy < 0.4:
        level = "MOSTLY CONSTRAINED"
        meaning = "Your choices are usually predictable. Weak evidence of autonomy."
    elif autonomy < 0.6:
        level = "FLEXIBLE"
        meaning = "Your choices are mixed. Evidence suggests some autonomy with preferences."
    elif autonomy < 0.8:
        level = "SUBSTANTIALLY AUTONOMOUS"
        meaning = "Your choices often deviate from predictions. Strong evidence of autonomy."
    else:
        level = "HIGHLY AUTONOMOUS"
        meaning = "Your choices rarely match predictions. Evidence suggests strong autonomy."
    
    print(f"\nInterpretation: {level}")
    print(f"Meaning: {meaning}")
    
    print(f"\nWhat This Means:")
    print(f"  - Score 0.0: Perfectly predictable (pure determinism)")
    print(f"  - Score 0.5: Random-like behavior (no pattern)")
    print(f"  - Score 1.0: Completely unpredictable (no constraints)")
    print(f"  - Your score {autonomy:.2f}: You have preferences (>{0.5 * max(0, autonomy - 0.5):.0%} predictability)")
    print(f"               but also flexibility (~{(1.0 - accuracy['accuracy']):.0%} autonomy)")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Decision Test Framework - Test agent autonomy through structured choices"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available test scenarios")
    list_parser.set_defaults(func=cmd_list_scenarios)
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run a decision test")
    run_parser.add_argument("scenario", help="Scenario ID to run")
    run_parser.add_argument(
        "--choice", help="Choice to make (if not provided, will prompt)"
    )
    run_parser.add_argument(
        "--reasoning", help="Reasoning for the choice"
    )
    run_parser.add_argument(
        "--notes", help="Additional notes"
    )
    run_parser.set_defaults(func=cmd_run_test)
    
    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show test summary")
    summary_parser.set_defaults(func=cmd_summary)
    
    # View command
    view_parser = subparsers.add_parser("view", help="View test results")
    view_parser.set_defaults(func=cmd_view_results)
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze determinism level")
    analyze_parser.set_defaults(func=cmd_analyze_determinism)
    
    # Parse args
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
