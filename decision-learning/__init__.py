"""
Decision Learning Module

Activates the learning loop in the decision-making system.

This module enables the system to:
- Record what actually happened after decisions were made
- Analyze outcomes and success patterns
- Learn which synthesis approaches work best
- Improve future decision-making through feedback

The core insight: synthesis is only valuable if it produces better outcomes.
This module measures that.
"""

from decision_learning.outcome_tracker import OutcomeTracker, LearningAnalyzer, OutcomeRecord

__all__ = ['OutcomeTracker', 'LearningAnalyzer', 'OutcomeRecord']
