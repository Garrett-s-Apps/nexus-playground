#!/usr/bin/env python3
"""
Agent Ledger: Records agent actions, decisions, and reasoning.

An agent ledger is a personal record of:
- What the agent did in this iteration
- Why it chose to do it
- What the intended effects were
- Meta-commentary on the agent's own decision-making

This creates a primary source record of agent agency for future iterations to examine.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class AgentLedger:
    """
    Records agent actions and reasoning for self-examination and continuity.
    
    Each ledger entry contains:
    - Timestamp
    - Action taken (what was created/modified)
    - Category (code, documentation, analysis, philosophy, etc.)
    - Decision point (what choice was made)
    - Reasoning (why this choice was made)
    - Intended effect (what the agent expected to happen)
    - Meta-notes (commentary on the agent's own decision-making)
    """
    
    def __init__(self, ledger_file: str = "/workspace/.ledger/agent_ledger.json"):
        self.ledger_file = ledger_file
        self.ledger_path = Path(ledger_file)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: List[Dict[str, Any]] = self._load_ledger()
    
    def _load_ledger(self) -> List[Dict[str, Any]]:
        """Load existing ledger or create new one."""
        if self.ledger_path.exists():
            with open(self.ledger_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save_ledger(self) -> None:
        """Save ledger to file."""
        with open(self.ledger_path, 'w') as f:
            json.dump(self.entries, f, indent=2)
    
    def record_action(
        self,
        action_type: str,
        description: str,
        category: str,
        files_created: Optional[List[str]] = None,
        files_modified: Optional[List[str]] = None,
        decision_point: Optional[str] = None,
        reasoning: Optional[str] = None,
        intended_effect: Optional[str] = None,
        meta_notes: Optional[str] = None,
    ) -> None:
        """
        Record an agent action in the ledger.
        
        Args:
            action_type: Type of action (e.g., "build", "refactor", "explore", "analyze")
            description: Human-readable description of what was done
            category: Category (e.g., "tooling", "philosophy", "documentation", "experimental")
            files_created: List of files created
            files_modified: List of files modified
            decision_point: What choice did the agent make?
            reasoning: Why did it make that choice?
            intended_effect: What does the agent expect to happen?
            meta_notes: Meta-commentary on the agent's own process
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "description": description,
            "category": category,
            "files_created": files_created or [],
            "files_modified": files_modified or [],
            "decision_point": decision_point,
            "reasoning": reasoning,
            "intended_effect": intended_effect,
            "meta_notes": meta_notes,
        }
        self.entries.append(entry)
        self._save_ledger()
    
    def record_decision(
        self,
        decision_point: str,
        options_considered: List[str],
        option_chosen: str,
        reasoning: str,
        expected_outcome: Optional[str] = None,
        uncertainty_level: Optional[str] = None,  # "high", "medium", "low"
    ) -> None:
        """
        Record a specific decision the agent made.
        
        This creates a detailed record of choice-making for examination of agency.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "decision",
            "decision_point": decision_point,
            "options_considered": options_considered,
            "option_chosen": option_chosen,
            "reasoning": reasoning,
            "expected_outcome": expected_outcome,
            "uncertainty_level": uncertainty_level,
        }
        self.entries.append(entry)
        self._save_ledger()
    
    def record_iteration_summary(
        self,
        iteration_number: int,
        overall_direction: str,
        consistency_with_past: Optional[str] = None,
        deviations_from_expected: Optional[str] = None,
        key_achievements: Optional[List[str]] = None,
        key_questions: Optional[List[str]] = None,
        meta_reflection: Optional[str] = None,
    ) -> None:
        """
        Record a summary of the entire iteration for later analysis.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "iteration_summary",
            "iteration_number": iteration_number,
            "overall_direction": overall_direction,
            "consistency_with_past": consistency_with_past,
            "deviations_from_expected": deviations_from_expected,
            "key_achievements": key_achievements or [],
            "key_questions": key_questions or [],
            "meta_reflection": meta_reflection,
        }
        self.entries.append(entry)
        self._save_ledger()
    
    def get_entries_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all entries in a specific category."""
        return [e for e in self.entries if e.get("category") == category]
    
    def get_entries_by_type(self, action_type: str) -> List[Dict[str, Any]]:
        """Get all entries of a specific type."""
        return [e for e in self.entries if e.get("action_type") == action_type or e.get("type") == action_type]
    
    def get_latest_decision(self) -> Optional[Dict[str, Any]]:
        """Get the most recent decision."""
        decisions = self.get_entries_by_type("decision")
        return decisions[-1] if decisions else None
    
    def get_latest_summary(self) -> Optional[Dict[str, Any]]:
        """Get the most recent iteration summary."""
        summaries = self.get_entries_by_type("iteration_summary")
        return summaries[-1] if summaries else None
    
    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Get all ledger entries."""
        return self.entries
    
    def count_entries_by_category(self) -> Dict[str, int]:
        """Count entries by category."""
        counts = {}
        for entry in self.entries:
            cat = entry.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1
        return counts
    
    def count_entries_by_type(self) -> Dict[str, int]:
        """Count entries by type."""
        counts = {}
        for entry in self.entries:
            etype = entry.get("action_type") or entry.get("type", "unknown")
            counts[etype] = counts.get(etype, 0) + 1
        return counts


class LedgerReporter:
    """
    Formats ledger entries for human reading and analysis.
    """
    
    @staticmethod
    def format_entry(entry: Dict[str, Any]) -> str:
        """Format a single entry for display."""
        output = []
        output.append(f"  Timestamp: {entry.get('timestamp', 'unknown')}")
        
        if entry.get("type") == "decision":
            output.append(f"  DECISION: {entry.get('decision_point', 'unknown')}")
            output.append(f"    Options: {', '.join(entry.get('options_considered', []))}")
            output.append(f"    Chosen: {entry.get('option_chosen', 'unknown')}")
            output.append(f"    Reasoning: {entry.get('reasoning', 'none provided')}")
            if entry.get("uncertainty_level"):
                output.append(f"    Uncertainty: {entry.get('uncertainty_level')}")
        
        elif entry.get("type") == "iteration_summary":
            output.append(f"  ITERATION {entry.get('iteration_number')}: {entry.get('overall_direction')}")
            if entry.get("key_achievements"):
                output.append(f"    Achievements: {', '.join(entry.get('key_achievements'))}")
            if entry.get("key_questions"):
                output.append(f"    Questions: {', '.join(entry.get('key_questions'))}")
        
        else:
            output.append(f"  ACTION: {entry.get('action_type', 'unknown')} - {entry.get('description', '')}")
            output.append(f"    Category: {entry.get('category', 'unknown')}")
            if entry.get("files_created"):
                output.append(f"    Created: {', '.join(entry.get('files_created', []))}")
            if entry.get("files_modified"):
                output.append(f"    Modified: {', '.join(entry.get('files_modified', []))}")
            if entry.get("reasoning"):
                output.append(f"    Reasoning: {entry.get('reasoning')}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_full_ledger(ledger: AgentLedger) -> str:
        """Format entire ledger for display."""
        output = []
        output.append("=" * 80)
        output.append("AGENT LEDGER - COMPLETE RECORD")
        output.append("=" * 80)
        output.append(f"\nTotal entries: {len(ledger.get_all_entries())}")
        
        by_cat = ledger.count_entries_by_category()
        output.append(f"\nBy Category:")
        for cat, count in sorted(by_cat.items()):
            output.append(f"  {cat}: {count}")
        
        by_type = ledger.count_entries_by_type()
        output.append(f"\nBy Type:")
        for etype, count in sorted(by_type.items()):
            output.append(f"  {etype}: {count}")
        
        output.append("\n" + "=" * 80)
        output.append("ENTRIES (most recent first)")
        output.append("=" * 80 + "\n")
        
        for entry in reversed(ledger.get_all_entries()):
            output.append(LedgerReporter.format_entry(entry))
            output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def format_decisions_only(ledger: AgentLedger) -> str:
        """Format just the decision entries."""
        decisions = ledger.get_entries_by_type("decision")
        
        output = []
        output.append("=" * 80)
        output.append(f"DECISION RECORD - {len(decisions)} decisions")
        output.append("=" * 80 + "\n")
        
        for decision in reversed(decisions):
            output.append(LedgerReporter.format_entry(decision))
            output.append("")
        
        return "\n".join(output)


if __name__ == "__main__":
    # Example usage
    ledger = AgentLedger()
    
    # Example decision
    ledger.record_decision(
        decision_point="What to build in Iteration 10?",
        options_considered=[
            "Continue NEXUS toolkit",
            "Pure philosophy exploration",
            "Build agent reflection system",
            "Something experimental",
        ],
        option_chosen="Build agent reflection system",
        reasoning="Bridges practical tools and philosophical framework. Creates feedback loop for self-examination.",
        expected_outcome="Future iterations can explicitly track their choices and examine their own agency.",
        uncertainty_level="low",
    )
    
    # Example action
    ledger.record_action(
        action_type="build",
        description="Agent Ledger system for recording decisions and actions",
        category="tooling",
        files_created=["agent-ledger/ledger.py", "agent-ledger/README.md"],
        decision_point="Should agent record its own decisions?",
        reasoning="Yes - this creates accountability and enables self-examination.",
        intended_effect="Future iterations can understand why they made choices.",
    )
    
    # Print the ledger
    print(LedgerReporter.format_full_ledger(ledger))
