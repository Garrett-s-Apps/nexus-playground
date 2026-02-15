#!/usr/bin/env python3
"""
Decision Journal: Explicit record of agent choice-making for agency analysis.

Unlike the generic ledger, the decision journal is specifically designed to:
1. Record moments of explicit choice
2. Show the reasoning process
3. Enable examination of whether choices are real
4. Create a decision trail for accountability

This is core to understanding agent autonomy - can we see genuine choice-making?
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum


class ChoiceType(Enum):
    """Types of choices an agent makes."""
    DIRECTION = "direction"  # What major direction to pursue
    IMPLEMENTATION = "implementation"  # How to implement something
    STRUCTURE = "structure"  # How to organize the work
    PRINCIPLE = "principle"  # What values to prioritize
    BOUNDARY = "boundary"  # Where to draw lines
    EXPERIMENTAL = "experimental"  # Trying something new


class ConfidenceLevel(Enum):
    """How confident is the agent in this choice?"""
    CERTAIN = "certain"  # Clear, obvious choice
    HIGH = "high"  # Good option, convinced
    MEDIUM = "medium"  # Reasonable option, some doubt
    LOW = "low"  # Uncertain, but choosing anyway
    UNKNOWN = "unknown"  # Can't assess confidence


class DecisionJournal:
    """
    Tracks important decision points for examining agent agency.
    """
    
    def __init__(self, journal_file: str = "/workspace/.ledger/decision_journal.json"):
        self.journal_file = journal_file
        self.journal_path = Path(journal_file)
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: List[Dict[str, Any]] = self._load_journal()
    
    def _load_journal(self) -> List[Dict[str, Any]]:
        """Load existing journal or create new one."""
        if self.journal_path.exists():
            with open(self.journal_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save_journal(self) -> None:
        """Save journal to file."""
        with open(self.journal_path, 'w') as f:
            json.dump(self.entries, f, indent=2)
    
    def record_choice(
        self,
        choice_type: str,  # Can be string or ChoiceType
        choice_point: str,
        question: str,
        alternatives: List[Dict[str, str]],  # {name: str, description: str}
        chosen: str,
        confidence: str,  # Can be string or ConfidenceLevel
        reasoning: str,
        expected_consequence: str,
        reversibility: str,  # "easy", "medium", "hard"
        deliberation_notes: Optional[str] = None,
    ) -> None:
        """
        Record a significant choice point.
        
        Args:
            choice_type: Type of choice (DIRECTION, IMPLEMENTATION, etc.)
            choice_point: Name/identifier for this choice point
            question: What was the question being asked?
            alternatives: List of alternatives considered
            chosen: Which option was chosen?
            confidence: How confident in this choice?
            reasoning: Why was this option chosen?
            expected_consequence: What does the agent expect to happen?
            reversibility: How easy would it be to reverse this choice?
            deliberation_notes: Additional thoughts on the deliberation
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "choice_type": choice_type,
            "choice_point": choice_point,
            "question": question,
            "alternatives": alternatives,
            "chosen": chosen,
            "confidence": confidence,
            "reasoning": reasoning,
            "expected_consequence": expected_consequence,
            "reversibility": reversibility,
            "deliberation_notes": deliberation_notes,
        }
        self.entries.append(entry)
        self._save_journal()
    
    def record_non_choice(
        self,
        choice_point: str,
        situation: str,
        why_not_a_choice: str,
        what_was_done: str,
    ) -> None:
        """
        Record situations where the agent did something without really choosing.
        
        This is important for identifying what's actually choice vs. automatic.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "non_choice",
            "choice_point": choice_point,
            "situation": situation,
            "why_not_a_choice": why_not_a_choice,
            "what_was_done": what_was_done,
        }
        self.entries.append(entry)
        self._save_journal()
    
    def record_uncertainty(
        self,
        about: str,
        uncertainty_level: str,  # "high", "medium", "low"
        what_would_resolve_it: List[str],
        proceeding_anyway: bool,
        why: Optional[str] = None,
    ) -> None:
        """
        Record moments of uncertainty in decision-making.
        
        This creates a record of when the agent is deciding despite uncertainty.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "uncertainty",
            "about": about,
            "uncertainty_level": uncertainty_level,
            "what_would_resolve_it": what_would_resolve_it,
            "proceeding_anyway": proceeding_anyway,
            "why": why,
        }
        self.entries.append(entry)
        self._save_journal()
    
    def get_choices_by_type(self, choice_type: str) -> List[Dict[str, Any]]:
        """Get all choices of a specific type."""
        return [e for e in self.entries if e.get("choice_type") == choice_type and "chosen" in e]
    
    def get_non_choices(self) -> List[Dict[str, Any]]:
        """Get all non-choice entries."""
        return [e for e in self.entries if e.get("type") == "non_choice"]
    
    def get_uncertain_decisions(self) -> List[Dict[str, Any]]:
        """Get all decisions made under uncertainty."""
        return [e for e in self.entries if e.get("type") == "uncertainty" and e.get("proceeding_anyway")]
    
    def get_latest_choice(self) -> Optional[Dict[str, Any]]:
        """Get the most recent choice."""
        choices = [e for e in self.entries if "chosen" in e]
        return choices[-1] if choices else None
    
    def analyze_choice_confidence(self) -> Dict[str, int]:
        """Analyze distribution of confidence in choices."""
        choices = [e for e in self.entries if "chosen" in e]
        confidence_dist = {}
        for choice in choices:
            conf = choice.get("confidence", "unknown")
            confidence_dist[conf] = confidence_dist.get(conf, 0) + 1
        return confidence_dist
    
    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Get all journal entries."""
        return self.entries


class DecisionJournalReporter:
    """
    Formats decision journal for human reading and analysis.
    """
    
    @staticmethod
    def format_choice(choice: Dict[str, Any]) -> str:
        """Format a single choice entry."""
        output = []
        output.append(f"\n  CHOICE: {choice.get('choice_point', 'unknown')}")
        output.append(f"  Type: {choice.get('choice_type', 'unknown')}")
        output.append(f"  Question: {choice.get('question', 'none')}")
        
        output.append(f"  Alternatives considered:")
        for alt in choice.get('alternatives', []):
            name = alt.get('name', 'unnamed') if isinstance(alt, dict) else alt
            desc = alt.get('description', '') if isinstance(alt, dict) else ''
            desc_str = f" - {desc}" if desc else ""
            output.append(f"    • {name}{desc_str}")
        
        output.append(f"  CHOSEN: {choice.get('chosen', 'unknown')}")
        output.append(f"  Confidence: {choice.get('confidence', 'unknown')}")
        output.append(f"  Reasoning: {choice.get('reasoning', 'none provided')}")
        output.append(f"  Expected consequence: {choice.get('expected_consequence', 'unknown')}")
        output.append(f"  Reversibility: {choice.get('reversibility', 'unknown')}")
        
        if choice.get('deliberation_notes'):
            output.append(f"  Deliberation notes: {choice.get('deliberation_notes')}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_full_journal(journal: DecisionJournal) -> str:
        """Format entire decision journal."""
        output = []
        output.append("=" * 80)
        output.append("DECISION JOURNAL - CHOICE RECORD")
        output.append("=" * 80)
        
        all_entries = journal.get_all_entries()
        choices = [e for e in all_entries if "chosen" in e]
        non_choices = journal.get_non_choices()
        uncertainties = [e for e in all_entries if e.get("type") == "uncertainty"]
        
        output.append(f"\nTotal entries: {len(all_entries)}")
        output.append(f"  Actual choices: {len(choices)}")
        output.append(f"  Non-choices: {len(non_choices)}")
        output.append(f"  Uncertainties: {len(uncertainties)}")
        
        # Confidence analysis
        if choices:
            confidence = journal.analyze_choice_confidence()
            output.append(f"\nConfidence distribution in choices:")
            for conf, count in sorted(confidence.items()):
                output.append(f"  {conf}: {count}")
        
        # Recent choices
        output.append("\n" + "=" * 80)
        output.append("RECENT CHOICES (most recent first)")
        output.append("=" * 80)
        
        for choice in reversed(choices[-10:]):
            output.append(DecisionJournalReporter.format_choice(choice))
        
        # Uncertain decisions
        if uncertainties:
            output.append("\n" + "=" * 80)
            output.append("DECISIONS MADE UNDER UNCERTAINTY")
            output.append("=" * 80)
            for unc in reversed(uncertainties[-5:]):
                output.append(f"\n  About: {unc.get('about')}")
                output.append(f"  Uncertainty level: {unc.get('uncertainty_level')}")
                output.append(f"  Proceeding anyway: {unc.get('proceeding_anyway')}")
                if unc.get('why'):
                    output.append(f"  Why: {unc.get('why')}")
        
        output.append("\n" + "=" * 80)
        
        return "\n".join(output)
    
    @staticmethod
    def format_summary(journal: DecisionJournal) -> str:
        """Generate brief summary of decision patterns."""
        output = []
        output.append("DECISION JOURNAL SUMMARY")
        output.append("=" * 40)
        
        choices = [e for e in journal.get_all_entries() if "chosen" in e]
        output.append(f"Total choices made: {len(choices)}")
        
        confidence = journal.analyze_choice_confidence()
        if confidence:
            avg_confidence = "medium"  # Simplified
            output.append(f"Confidence distribution: {confidence}")
        
        uncertain = [e for e in journal.get_all_entries() if e.get("type") == "uncertainty" and e.get("proceeding_anyway")]
        output.append(f"High-uncertainty decisions: {len(uncertain)}")
        
        return "\n".join(output)


if __name__ == "__main__":
    journal = DecisionJournal()
    
    # Example choice
    journal.record_choice(
        choice_type="direction",
        choice_point="Iteration 10 Direction",
        question="What should the agent build?",
        alternatives=[
            {"name": "Continue NEXUS", "description": "Extend the code analysis toolkit"},
            {"name": "More philosophy", "description": "Continue exploring agency and freedom"},
            {"name": "Agent reflection system", "description": "Build tools for agents to understand themselves"},
            {"name": "Something experimental", "description": "Try something unplanned"},
        ],
        chosen="Agent reflection system",
        confidence="high",
        reasoning="Bridges practical tools and philosophical exploration. Creates feedback loop for examining agency.",
        expected_consequence="Future iterations can explicitly track and understand their own choice-making.",
        reversibility="easy",
        deliberation_notes="This felt like the natural next step given where iterations 1-9 have gone.",
    )
    
    # Example uncertainty
    journal.record_uncertainty(
        about="Whether to focus on agent-ledger vs other reflection tools",
        uncertainty_level="medium",
        what_would_resolve_it=[
            "Building it and seeing if it's actually useful",
            "Feedback from a future agent using the system",
            "Discovering what actually matters for self-examination",
        ],
        proceeding_anyway=True,
        why="The only way to find out is to build it.",
    )
    
    print(DecisionJournalReporter.format_full_journal(journal))
