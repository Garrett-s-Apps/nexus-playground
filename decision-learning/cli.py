#!/usr/bin/env python3
"""
Decision Learning CLI

Interactive tool to:
- Record decision outcomes
- Track learning from experience
- Analyze which synthesis approaches work best
- Improve future decision-making through feedback

This is how the system learns: you make a decision, apply the synthesis,
see what happens, record the outcome, and the system learns patterns.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional

# Import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from decision_synthesizer.synthesizer import Decision
from decision_learning.outcome_tracker import OutcomeTracker, LearningAnalyzer


class Colors:
    """Terminal colors"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def load_decisions():
    """Load all decisions from the synthesizer decision log"""
    decisions_file = Path(__file__).parent.parent / '.decisions' / 'synthesizer_decisions.json'
    if decisions_file.exists():
        with open(decisions_file, 'r') as f:
            return json.load(f)
    return []


def record_outcome_interactive(tracker: OutcomeTracker):
    """Interactive workflow to record an outcome"""
    print(f"\n{Colors.CYAN}=== Record Decision Outcome ==={Colors.RESET}\n")
    
    # Show recent decisions
    decisions = load_decisions()
    if not decisions:
        print(f"{Colors.YELLOW}No decisions found in history.{Colors.RESET}")
        return
    
    print(f"{Colors.BLUE}Recent Decisions:{Colors.RESET}")
    for i, decision in enumerate(decisions[-10:], 1):  # Show last 10
        question = decision.get('question', 'Unknown')
        print(f"  {i}. {question}")
    
    print()
    choice = input(f"{Colors.BLUE}Which decision? (1-{len(decisions)}, or 'new'): {Colors.RESET}").strip()
    
    if choice.lower() == 'new':
        decision_id = f"manual_{len(decisions)}"
        question = input(f"{Colors.BLUE}Decision question: {Colors.RESET}").strip()
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(decisions):
                selected = decisions[idx]
                decision_id = selected.get('created', f"decision_{idx}")
                question = selected.get('question', 'Unknown')
            else:
                print(f"{Colors.RED}Invalid choice{Colors.RESET}")
                return
        except ValueError:
            print(f"{Colors.RED}Invalid input{Colors.RESET}")
            return
    
    print(f"\n{Colors.BLUE}Decision: {question}{Colors.RESET}")
    print()
    
    # Get the approach we actually took
    approach = input(f"{Colors.BLUE}What approach did we take? {Colors.RESET}").strip()
    
    # Get the outcome
    outcome = input(f"{Colors.BLUE}What was the actual outcome? {Colors.RESET}").strip()
    
    # Rate the success
    print(f"\n{Colors.BLUE}Rate the success (1-5):{Colors.RESET}")
    print("  5 = Excellent - worked really well")
    print("  4 = Good - worked well")
    print("  3 = Okay - worked but has issues")
    print("  2 = Poor - mostly didn't work")
    print("  1 = Failure - didn't work at all")
    
    while True:
        try:
            rating = int(input(f"{Colors.BLUE}Rating: {Colors.RESET}").strip())
            if 1 <= rating <= 5:
                break
            print(f"{Colors.YELLOW}Please enter 1-5{Colors.RESET}")
        except ValueError:
            print(f"{Colors.YELLOW}Please enter a number{Colors.RESET}")
    
    # When could we judge?
    print(f"\n{Colors.BLUE}How long did it take to judge?{Colors.RESET}")
    print("  immediate - Days")
    print("  short_term - Weeks")
    print("  medium_term - Months")
    print("  long_term - Longer")
    
    timing = input(f"{Colors.BLUE}Timing: {Colors.RESET}").strip().lower()
    if timing not in ['immediate', 'short_term', 'medium_term', 'long_term']:
        timing = 'short_term'  # default
    
    # Was it surprising?
    surprising = input(f"\n{Colors.BLUE}Was the outcome surprising? (y/n): {Colors.RESET}").strip().lower() == 'y'
    
    # What did we learn?
    learned = None
    if surprising:
        learned = input(f"{Colors.BLUE}What did we learn? {Colors.RESET}").strip()
    
    # Would we choose again?
    would_again_str = input(f"\n{Colors.BLUE}Would we make the same choice again? (y/n/not sure): {Colors.RESET}").strip().lower()
    would_again = None
    if would_again_str == 'y':
        would_again = True
    elif would_again_str == 'n':
        would_again = False
    
    # Record it
    tracker.record_outcome(
        decision_id=decision_id,
        decision_question=question,
        chosen_approach=approach,
        outcome_description=outcome,
        success_rating=rating,
        time_to_judge=timing,
        surprising=surprising,
        learned=learned,
        would_choose_again=would_again
    )
    
    print(f"\n{Colors.GREEN}✓ Outcome recorded!{Colors.RESET}\n")


def show_learning_report(tracker: OutcomeTracker):
    """Show the learning report"""
    analyzer = LearningAnalyzer(tracker)
    print(analyzer.generate_learning_report())


def show_outcomes_for_decision(tracker: OutcomeTracker):
    """Show all outcomes for a specific decision"""
    decisions = load_decisions()
    
    if not decisions:
        print(f"{Colors.YELLOW}No decisions found.{Colors.RESET}")
        return
    
    print(f"\n{Colors.BLUE}Decisions:{Colors.RESET}")
    for i, decision in enumerate(decisions, 1):
        question = decision.get('question', 'Unknown')[:60]
        print(f"  {i}. {question}")
    
    try:
        choice = int(input(f"\n{Colors.BLUE}Which decision? (1-{len(decisions)}): {Colors.RESET}").strip())
        if 1 <= choice <= len(decisions):
            selected = decisions[choice - 1]
            decision_id = selected.get('created', f"decision_{choice-1}")
            
            outcomes = tracker.get_outcomes_for_decision(decision_id)
            
            if not outcomes:
                print(f"\n{Colors.YELLOW}No outcomes recorded for this decision.{Colors.RESET}\n")
                return
            
            print(f"\n{Colors.CYAN}Decision: {selected.get('question')}{Colors.RESET}\n")
            print(f"Outcomes recorded: {len(outcomes)}\n")
            
            for i, outcome in enumerate(outcomes, 1):
                print(f"{Colors.BLUE}Outcome {i}:{Colors.RESET}")
                print(f"  Approach: {outcome.approach}")
                print(f"  Result: {outcome.outcome_description}")
                print(f"  Rating: {outcome.success_rating}/5")
                print(f"  Judged: {outcome.time_to_judge}")
                if outcome.would_choose_again is not None:
                    print(f"  Would repeat: {'Yes' if outcome.would_choose_again else 'No'}")
                if outcome.learned:
                    print(f"  Learned: {outcome.learned}")
                print()
        else:
            print(f"{Colors.RED}Invalid choice{Colors.RESET}")
    except ValueError:
        print(f"{Colors.RED}Invalid input{Colors.RESET}")


def export_learning_data(tracker: OutcomeTracker):
    """Export all learning data as JSON"""
    outcomes = tracker.get_all_outcomes()
    
    # Convert to JSON-serializable format
    export_data = {}
    for decision_id, outcome_list in outcomes.items():
        export_data[decision_id] = [
            {
                'decision_id': o.decision_id,
                'decision_question': o.decision_question,
                'chosen_approach': o.chosen_approach,
                'outcome_description': o.outcome_description,
                'success_rating': o.success_rating,
                'time_to_judge': o.time_to_judge,
                'surprising': o.surprising,
                'learned': o.learned,
                'would_choose_again': o.would_choose_again,
                'created': o.created
            }
            for o in outcome_list
        ]
    
    output_file = Path(__file__).parent.parent / '.decisions' / 'learning_export.json'
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"{Colors.GREEN}✓ Learning data exported to {output_file}{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Decision Learning CLI - Track outcomes and learn from decisions"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Commands
    subparsers.add_parser('record', help='Record an outcome interactively')
    subparsers.add_parser('report', help='Show learning report')
    subparsers.add_parser('show', help='Show outcomes for a specific decision')
    subparsers.add_parser('export', help='Export learning data as JSON')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = OutcomeTracker()
    
    if args.command == 'record':
        record_outcome_interactive(tracker)
    elif args.command == 'report':
        show_learning_report(tracker)
    elif args.command == 'show':
        show_outcomes_for_decision(tracker)
    elif args.command == 'export':
        export_learning_data(tracker)
    else:
        # Default: show help and report
        parser.print_help()
        print()
        show_learning_report(tracker)


if __name__ == '__main__':
    main()
