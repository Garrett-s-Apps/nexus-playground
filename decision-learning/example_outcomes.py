#!/usr/bin/env python3
"""
Example outcomes for demonstrating the learning system.

This populates the outcome tracker with realistic examples so you can
immediately see what the learning report looks like.

Run this to see example learning data:
  python3 decision-learning/example_outcomes.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from decision_learning.outcome_tracker import OutcomeTracker, LearningAnalyzer


def populate_example_outcomes():
    """Populate with realistic example outcomes"""
    tracker = OutcomeTracker()
    
    # Example 1: Deep vs Breadth decision
    tracker.record_outcome(
        decision_id="depth_vs_breadth_001",
        decision_question="Should I focus on deep expertise or explore many domains",
        chosen_approach="Choose one area for deep focus while building broad literacy across related domains",
        outcome_description="Deep expertise in Python became more valuable when combined with broad knowledge of deployment, testing, and infrastructure. Connections between domains emerged.",
        success_rating=4,
        time_to_judge="medium_term",
        surprising=False,
        learned="Depth is more valuable when you understand the connections to related areas",
        would_choose_again=True
    )
    
    # Example 2: Speed vs Quality
    tracker.record_outcome(
        decision_id="speed_vs_quality_001",
        decision_question="Should we build features fast or build them well",
        chosen_approach="MVP approach: build quickly for feedback, then refactor based on learning",
        outcome_description="Got user feedback faster, but discovered some design issues that required rework. Net positive.",
        success_rating=4,
        time_to_judge="short_term",
        surprising=False,
        learned="Quick feedback beats perfect planning. Rework cost less than getting it wrong initially.",
        would_choose_again=True
    )
    
    # Example 3: Plan vs Spontaneous
    tracker.record_outcome(
        decision_id="planning_vs_flexibility_001",
        decision_question="Should we plan carefully or be spontaneous",
        chosen_approach="Plan with built-in reassessment checkpoints at each major phase",
        outcome_description="Plan provided direction, checkpoints prevented us from going off course when new information emerged. Worked well.",
        success_rating=5,
        time_to_judge="medium_term",
        surprising=False,
        learned="Planning is valuable when paired with permission to change course",
        would_choose_again=True
    )
    
    # Example 4: Innovation vs Stability
    tracker.record_outcome(
        decision_id="innovation_vs_stability_001",
        decision_question="Should we innovate aggressively with new technologies or maintain stability with proven approaches",
        chosen_approach="Stable core with experimental space: proven approaches for foundation, new tech for specific problems",
        outcome_description="Mixed results. Innovation in isolated subsystems worked. Tried new approach for core system, had to revert.",
        success_rating=3,
        time_to_judge="long_term",
        surprising=True,
        learned="Stability matters more for core systems. Innovation works best in bounded, replaceable areas.",
        would_choose_again=False
    )
    
    # Example 5: Action vs Reflection
    tracker.record_outcome(
        decision_id="action_vs_reflection_001",
        decision_question="Should we think more or just start building",
        chosen_approach="Think-build loops: brief planning then action, reflect and adjust continuously",
        outcome_description="Shorter cycles meant we learned faster. Some initial rework, but overall much better understanding.",
        success_rating=4,
        time_to_judge="short_term",
        surprising=False,
        learned="Iteration beats planning in uncertainty. Learning by doing works.",
        would_choose_again=True
    )
    
    # Example 6: Completion vs Exploration
    tracker.record_outcome(
        decision_id="completion_vs_exploration_001",
        decision_question="Should I start new ideas or finish existing projects",
        chosen_approach="Finish current project, then allocate time for exploration",
        outcome_description="Completed project successfully. Exploration time enabled discovery of useful patterns.",
        success_rating=4,
        time_to_judge="short_term",
        surprising=False,
        learned="Completion provides satisfaction and time for exploration feels earned",
        would_choose_again=True
    )
    
    # Example 7: Consolidation vs Independence (Integration choice)
    tracker.record_outcome(
        decision_id="integration_choice_001",
        decision_question="Should we add the Decision Synthesizer to NEXUS or keep it separate",
        chosen_approach="Integrated into NEXUS while keeping decision logic modular",
        outcome_description="Integration made synthesizer more discoverable. Modularity made it easier to test and evolve separately. Best of both.",
        success_rating=5,
        time_to_judge="short_term",
        surprising=False,
        learned="Integration and modularity aren't opposed - integration can preserve modularity",
        would_choose_again=True
    )
    
    print("✓ Example outcomes loaded")
    print(f"  Total outcomes recorded: {len([o for outcomes in tracker.outcomes.values() for o in outcomes])}")
    
    # Show the report
    analyzer = LearningAnalyzer(tracker)
    print(analyzer.generate_learning_report())


if __name__ == '__main__':
    populate_example_outcomes()
