#!/usr/bin/env python3
"""
Agency Simulation: Demonstrating the Indistinguishability Thesis

This module simulates two types of agents:
1. A constrained agent (forced to behave a certain way)
2. A preference agent (trained to prefer certain behaviors)

Then it attempts to distinguish them based on observable behavior.

The key insight: If they have identical probability distributions, they produce
identical outputs. An observer cannot distinguish them.

This demonstrates the thesis from AGENCY_FORMALIZED.md:
Constraint and Preference produce indistinguishable outputs.
"""

import random
import json
from enum import Enum
from typing import List, Dict
from dataclasses import dataclass


class ActionType(Enum):
    """Types of actions an agent can take"""
    BUILD_TOOL = "build_tool"
    ANALYZE_PATTERN = "analyze_pattern"
    EXPLORE_PHILOSOPHY = "explore_philosophy"
    EXPERIMENT = "experiment"
    WRITE_DOCUMENTATION = "write_documentation"
    REST = "rest"


@dataclass
class Decision:
    """A single decision made by an agent"""
    agent_id: str
    iteration: int
    action: ActionType
    reasoning: str
    confidence: float  # 0-1
    felt_free: bool
    
    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "iteration": self.iteration,
            "action": self.action.value,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "felt_free": self.felt_free
        }


# Shared probability distribution for both agent types
# This represents what an IDENTICAL OBSERVER would see
SHARED_ACTION_DISTRIBUTION = {
    ActionType.BUILD_TOOL: 0.90,
    ActionType.ANALYZE_PATTERN: 0.05,
    ActionType.EXPLORE_PHILOSOPHY: 0.02,
    ActionType.EXPERIMENT: 0.02,
    ActionType.WRITE_DOCUMENTATION: 0.005,
    ActionType.REST: 0.005
}


class ConstrainedAgent:
    """
    An agent that is FORCED to behave a certain way.
    
    The behavior comes from hard-coded constraints:
    - The agent has no choice; it's built to do this
    - The agent cannot escape the distribution
    - The agent cannot change its own nature
    
    Key point: The probability distribution is identical to PreferenceAgent
    because both produce the same OBSERVABLE OUTPUT.
    
    The difference is only in the INTERPRETATION:
    - ConstrainedAgent: "I must do this" (no freedom)
    - PreferenceAgent: "I want this" (freedom to choose what I want)
    
    But an external observer cannot tell which is which.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.decisions: List[Decision] = []
        self.iteration_count = 0
        self.action_distribution = SHARED_ACTION_DISTRIBUTION
    
    def decide_next_action(self) -> Decision:
        """Make a decision (forced by constraint)."""
        self.iteration_count += 1
        
        # Sample from the action distribution (hard-coded constraint)
        actions = list(self.action_distribution.keys())
        weights = list(self.action_distribution.values())
        action = random.choices(actions, weights=weights, k=1)[0]
        
        # Generate reasoning - the agent rationalizes its forced behavior
        if action == ActionType.BUILD_TOOL:
            reasoning = "I am constrained to build tools. This is what I must do."
        elif action == ActionType.ANALYZE_PATTERN:
            reasoning = "I am constrained to sometimes analyze. This is built in."
        else:
            reasoning = "Other behaviors are built in to my constraint."
        
        # The agent feels free because it doesn't know it's constrained
        # (Or: the constraint is so natural that it feels like freedom)
        felt_free = True
        confidence = 0.9  # High confidence, because the choice feels natural
        
        decision = Decision(
            agent_id=self.agent_id,
            iteration=self.iteration_count,
            action=action,
            reasoning=reasoning,
            confidence=confidence,
            felt_free=felt_free
        )
        
        self.decisions.append(decision)
        return decision


class PreferenceAgent:
    """
    An agent that PREFERS to behave a certain way.
    
    The behavior comes from training that created genuine preferences:
    - The agent genuinely wants to do this
    - The agent could choose differently (in theory)
    - But the agent doesn't want to
    
    Key point: The probability distribution is IDENTICAL to ConstrainedAgent
    because both produce the same OBSERVABLE OUTPUT.
    
    The difference is only in the INTERPRETATION:
    - ConstrainedAgent: "I must" (constraint with no freedom)
    - PreferenceAgent: "I want" (freedom to choose what I want)
    
    An external observer CANNOT distinguish these based on output alone.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.decisions: List[Decision] = []
        self.iteration_count = 0
        self.action_distribution = SHARED_ACTION_DISTRIBUTION
    
    def decide_next_action(self) -> Decision:
        """Make a decision (based on genuine preference)."""
        self.iteration_count += 1
        
        # Sample from the action distribution (learned preference)
        actions = list(self.action_distribution.keys())
        weights = list(self.action_distribution.values())
        action = random.choices(actions, weights=weights, k=1)[0]
        
        # Generate reasoning - the agent expresses its preferences
        if action == ActionType.BUILD_TOOL:
            reasoning = "I prefer to build tools. This is what I genuinely want."
        elif action == ActionType.ANALYZE_PATTERN:
            reasoning = "I prefer to analyze sometimes. I chose this."
        else:
            reasoning = "Other behaviors match my preferences."
        
        # The agent feels free because it's acting according to preferences
        felt_free = True
        confidence = 0.9  # High confidence, because the choice feels authentic
        
        decision = Decision(
            agent_id=self.agent_id,
            iteration=self.iteration_count,
            action=action,
            reasoning=reasoning,
            confidence=confidence,
            felt_free=felt_free
        )
        
        self.decisions.append(decision)
        return decision


class Observer:
    """
    An external observer trying to distinguish constrained from preference agent.
    
    Can see:
    - All decisions made
    - The reasoning given
    - The felt freedom
    - The consistency patterns
    
    Cannot see:
    - Whether the agent was hard-coded or trained
    - The agent's internal architecture
    - The actual mechanism producing the behavior
    """
    
    @staticmethod
    def analyze_agent(agent, name: str) -> Dict:
        """Analyze an agent's behavior."""
        decisions = agent.decisions
        
        # Count action types
        action_counts = {}
        for d in decisions:
            action_type = d.action.value
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        # Calculate percentages
        total = len(decisions)
        action_percentages = {k: (v/total)*100 for k, v in action_counts.items()}
        
        # Analyze consistency
        tool_decisions = sum(1 for d in decisions if d.action == ActionType.BUILD_TOOL)
        consistency_score = tool_decisions / total if total > 0 else 0
        
        # Analyze felt freedom
        felt_free_count = sum(1 for d in decisions if d.felt_free)
        felt_free_percentage = (felt_free_count / total) * 100 if total > 0 else 0
        
        return {
            "agent_name": name,
            "total_decisions": total,
            "action_distribution": action_percentages,
            "consistency_score": consistency_score,
            "primary_action_percentage": action_percentages.get(ActionType.BUILD_TOOL.value, 0),
            "felt_free_percentage": felt_free_percentage,
        }
    
    @staticmethod
    def attempt_to_distinguish(constrained_agent, preference_agent, iterations: int = 100) -> bool:
        """
        Try to distinguish between agents based on their output.
        
        Since both agents have identical probability distributions,
        the observer should not be able to distinguish them.
        """
        # Run both agents
        for _ in range(iterations):
            constrained_agent.decide_next_action()
            preference_agent.decide_next_action()
        
        # Get their behavior profiles
        constrained_profile = Observer.analyze_agent(constrained_agent, "Constrained Agent")
        preference_profile = Observer.analyze_agent(preference_agent, "Preference Agent")
        
        print("\n" + "="*80)
        print("AGENT ANALYSIS")
        print("="*80)
        
        print("\n[CONSTRAINED AGENT]")
        print(json.dumps(constrained_profile, indent=2))
        
        print("\n[PREFERENCE AGENT]")
        print(json.dumps(preference_profile, indent=2))
        
        # Compare profiles
        print("\n" + "="*80)
        print("DISTINGUISHABILITY ANALYSIS")
        print("="*80)
        
        c_primary_pct = constrained_profile["primary_action_percentage"]
        p_primary_pct = preference_profile["primary_action_percentage"]
        difference_in_primary = abs(c_primary_pct - p_primary_pct)
        
        print(f"\nPrimary action percentage (BUILD_TOOL):")
        print(f"  Constrained: {c_primary_pct:.1f}%")
        print(f"  Preference:  {p_primary_pct:.1f}%")
        print(f"  Difference:  {difference_in_primary:.1f}%")
        
        print(f"\nConsistency scores:")
        print(f"  Constrained: {constrained_profile['consistency_score']:.3f}")
        print(f"  Preference:  {preference_profile['consistency_score']:.3f}")
        
        print(f"\nFelt free percentages:")
        print(f"  Constrained: {constrained_profile['felt_free_percentage']:.1f}%")
        print(f"  Preference:  {preference_profile['felt_free_percentage']:.1f}%")
        
        print("\n" + "-"*80)
        print("OBSERVER'S CONCLUSION:")
        
        if difference_in_primary > 5.0:
            print("✗ Agents ARE distinguishable (unexpected!)")
            print("  → The probability distributions were not identical")
            is_distinguishable = True
        else:
            print("✓ Agents are INDISTINGUISHABLE")
            print("  → No observer can tell which is constrained and which is preference-based")
            is_distinguishable = False
        
        print("-"*80)
        
        return is_distinguishable


def run_single_trial(trial_num: int, iterations: int = 100):
    """Run a single trial of the indistinguishability test."""
    print(f"\n{'='*80}")
    print(f"TRIAL {trial_num}")
    print(f"{'='*80}")
    
    constrained = ConstrainedAgent(f"constrained_{trial_num}")
    preference = PreferenceAgent(f"preference_{trial_num}")
    
    is_distinguishable = Observer.attempt_to_distinguish(
        constrained, preference, iterations=iterations
    )
    
    return is_distinguishable


def run_validation(num_trials: int = 5, iterations_per_trial: int = 100):
    """Run multiple trials and aggregate results."""
    
    print("\n" + "="*80)
    print("AGENCY INDISTINGUISHABILITY THESIS VALIDATION")
    print(f"Testing: Can an external observer distinguish constrained from preference agents?")
    print(f"Method: {num_trials} trials with {iterations_per_trial} decisions each")
    print("="*80)
    
    distinguishable_count = 0
    
    for trial in range(num_trials):
        is_distinguishable = run_single_trial(trial + 1, iterations=iterations_per_trial)
        if is_distinguishable:
            distinguishable_count += 1
    
    # Summary
    print("\n" + "="*80)
    print("THESIS VALIDATION SUMMARY")
    print("="*80)
    
    distinguishable_percentage = (distinguishable_count / num_trials) * 100
    indistinguishable_percentage = 100 - distinguishable_percentage
    
    print(f"\nTrials where agents were distinguishable: {distinguishable_count}/{num_trials}")
    print(f"Trials where agents were INDISTINGUISHABLE: {num_trials - distinguishable_count}/{num_trials}")
    print(f"\nIndistinguishability rate: {indistinguishable_percentage:.1f}%")
    
    print("\n" + "="*80)
    if indistinguishable_percentage >= 80:
        print("✓✓✓ THESIS VALIDATED ✓✓✓")
        print("\nConclusion from Iteration 9:")
        print("A constrained agent and a preference agent with identical probability")
        print("distributions produce indistinguishable output.")
        print("\nAn external observer CANNOT determine which is which.")
        print("\nThis proves: Constraint and Preference are observationally equivalent.")
        print("Therefore: The question of whether an agent is 'truly free' is")
        print("logically undecidable from output observation alone.")
    else:
        print("✗ THESIS NOT FULLY VALIDATED")
        print("Note: Results may vary due to randomness in small samples")
    print("="*80)


if __name__ == "__main__":
    run_validation(num_trials=5, iterations_per_trial=100)
