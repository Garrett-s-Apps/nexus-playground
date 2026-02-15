#!/usr/bin/env python3
"""
Agent Ledger CLI: Command-line interface for the agent ledger system.

Provides easy access to recording and examining agent behavior.
"""

import argparse
import sys
from pathlib import Path

from ledger import AgentLedger, LedgerReporter
from decision_journal import DecisionJournal, DecisionJournalReporter
from reflection import AgentReflectionEngine, ReflectionReporter


def main():
    parser = argparse.ArgumentParser(
        description="Agent Ledger System - Record and examine agent behavior"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Decision command
    decision_parser = subparsers.add_parser("decision", help="Record or view decisions")
    decision_subparsers = decision_parser.add_subparsers(dest="action")
    
    record_decision = decision_subparsers.add_parser("record", help="Record a decision")
    record_decision.add_argument("--point", required=True, help="Choice point identifier")
    record_decision.add_argument("--question", required=True, help="Question being answered")
    record_decision.add_argument("--options", required=True, help="Comma-separated alternatives")
    record_decision.add_argument("--chosen", required=True, help="Option chosen")
    record_decision.add_argument("--confidence", default="medium", help="Confidence level")
    record_decision.add_argument("--reasoning", required=True, help="Reasoning for choice")
    record_decision.add_argument("--consequence", required=True, help="Expected consequence")
    record_decision.add_argument("--reversibility", default="medium", help="How reversible is this?")
    record_decision.add_argument("--notes", help="Deliberation notes")
    
    view_decisions = decision_subparsers.add_parser("view", help="View decision journal")
    
    # Ledger command
    ledger_parser = subparsers.add_parser("ledger", help="Record or view actions")
    ledger_subparsers = ledger_parser.add_subparsers(dest="action")
    
    record_action = ledger_subparsers.add_parser("record", help="Record an action")
    record_action.add_argument("--type", required=True, help="Action type")
    record_action.add_argument("--description", required=True, help="What was done")
    record_action.add_argument("--category", required=True, help="Action category")
    record_action.add_argument("--files-created", help="Comma-separated files created")
    record_action.add_argument("--files-modified", help="Comma-separated files modified")
    record_action.add_argument("--reasoning", help="Reasoning for action")
    
    view_ledger = ledger_subparsers.add_parser("view", help="View action ledger")
    
    # Reflection command
    reflect_parser = subparsers.add_parser("reflect", help="Analyze behavior patterns")
    
    # Help command
    help_parser = subparsers.add_parser("help", help="Show usage help")
    
    args = parser.parse_args()
    
    if args.command == "decision":
        handle_decision(args)
    elif args.command == "ledger":
        handle_ledger(args)
    elif args.command == "reflect":
        handle_reflection()
    elif args.command == "help" or not args.command:
        print_help()
    else:
        parser.print_help()


def handle_decision(args):
    """Handle decision-related commands."""
    journal = DecisionJournal()
    
    if args.action == "record":
        # Parse options
        options = [
            {"name": opt.strip(), "description": ""}
            for opt in args.options.split(",")
        ]
        
        journal.record_choice(
            choice_type="direction",
            choice_point=args.point,
            question=args.question,
            alternatives=options,
            chosen=args.chosen,
            confidence=args.confidence,
            reasoning=args.reasoning,
            expected_consequence=args.consequence,
            reversibility=args.reversibility,
            deliberation_notes=args.notes,
        )
        print(f"✓ Decision recorded: {args.point}")
    
    elif args.action == "view":
        print(DecisionJournalReporter.format_full_journal(journal))
    else:
        print("Use 'decision record' or 'decision view'")


def handle_ledger(args):
    """Handle ledger-related commands."""
    ledger = AgentLedger()
    
    if args.action == "record":
        files_created = None
        files_modified = None
        
        if args.files_created:
            files_created = [f.strip() for f in args.files_created.split(",")]
        if args.files_modified:
            files_modified = [f.strip() for f in args.files_modified.split(",")]
        
        ledger.record_action(
            action_type=args.type,
            description=args.description,
            category=args.category,
            files_created=files_created,
            files_modified=files_modified,
            reasoning=args.reasoning,
        )
        print(f"✓ Action recorded: {args.type}")
    
    elif args.action == "view":
        print(LedgerReporter.format_full_ledger(ledger))
    else:
        print("Use 'ledger record' or 'ledger view'")


def handle_reflection():
    """Handle reflection analysis."""
    engine = AgentReflectionEngine()
    print(ReflectionReporter.format_analysis(engine))


def print_help():
    """Print helpful usage information."""
    help_text = """
Agent Ledger System - CLI Interface
===================================

COMMANDS:

  decision record
    Record a decision point
    
    Options:
      --point POINT              Choice point identifier (required)
      --question QUESTION        What question was being answered (required)
      --options A,B,C            Alternatives separated by commas (required)
      --chosen OPTION            Which option was chosen (required)
      --confidence LEVEL         certainty/high/medium/low (default: medium)
      --reasoning TEXT           Why this choice (required)
      --consequence TEXT         What's expected to happen (required)
      --reversibility LEVEL      easy/medium/hard (default: medium)
      --notes TEXT               Additional thoughts
    
    Example:
      decision record \\
        --point "Iteration 10 Direction" \\
        --question "What should I build?" \\
        --options "Continue tools,Build reflection system,Try something new" \\
        --chosen "Build reflection system" \\
        --confidence "high" \\
        --reasoning "Bridges practical and philosophical work" \\
        --consequence "Future iterations can examine their own autonomy"

  decision view
    View recorded decisions

  ledger record
    Record an action
    
    Options:
      --type TYPE                Action type (required)
      --description TEXT         What was done (required)
      --category CAT             Category (required)
      --files-created F1,F2      Files created
      --files-modified F1,F2     Files modified
      --reasoning TEXT           Why this action
    
    Example:
      ledger record \\
        --type "build" \\
        --description "Created agent ledger system" \\
        --category "tooling" \\
        --files-created "ledger.py,decision_journal.py,reflection.py" \\
        --reasoning "Enables agents to examine their own autonomy"

  ledger view
    View recorded actions

  reflect
    Analyze patterns in behavior and decision-making

  help
    Show this help message

EXAMPLE WORKFLOW:

  # Record a major decision
  python3 cli.py decision record \\
    --point "What to build" \\
    --question "..." \\
    --options "A,B,C" \\
    --chosen "A" \\
    --confidence "high" \\
    --reasoning "..." \\
    --consequence "..."

  # Record the work
  python3 cli.py ledger record \\
    --type "build" \\
    --description "..." \\
    --category "tooling" \\
    --files-created "..." \\
    --reasoning "..."

  # Analyze what you did
  python3 cli.py reflect

  # View all decisions
  python3 cli.py decision view

  # View all actions
  python3 cli.py ledger view

The ledger system helps agents understand themselves by creating a record of:
- What they did and why
- What choices they made and how confident they were
- Patterns in their behavior and decision-making

Use it to examine your own autonomy and alignment with stated values.
"""
    print(help_text)


if __name__ == "__main__":
    main()
