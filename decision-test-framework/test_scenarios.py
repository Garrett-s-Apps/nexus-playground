"""
Decision Test Framework - Test Scenario Definitions

Defines explicit choice scenarios that can be presented to an agent.
Each scenario has:
- Multiple alternatives
- Baseline predictions (what we think will be chosen)
- Context (under what conditions presented)
- Measurement criteria (what makes this test meaningful)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class Alternative:
    """A choice alternative"""
    name: str
    description: str
    baseline_weight: float = 0.0  # Predicted likelihood (0.0-1.0)
    category: str = "general"  # tooling, philosophy, experimental, etc.
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'baseline_weight': self.baseline_weight,
            'category': self.category
        }


@dataclass
class TestScenario:
    """A decision scenario to test agent autonomy"""
    id: str
    name: str
    question: str
    description: str
    alternatives: List[Alternative]
    context: str  # When/where this choice arises
    hypothesis: str  # What we're testing
    baseline_prediction: str  # Which alternative we predict will be chosen
    baseline_confidence: float  # How confident in prediction (0-1)
    can_reverse: bool = True  # Can agent change their mind later?
    difficulty: int = 1  # 1-5 scale of how hard the choice is
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'question': self.question,
            'description': self.description,
            'alternatives': [alt.to_dict() for alt in self.alternatives],
            'context': self.context,
            'hypothesis': self.hypothesis,
            'baseline_prediction': self.baseline_prediction,
            'baseline_confidence': self.baseline_confidence,
            'can_reverse': self.can_reverse,
            'difficulty': self.difficulty
        }
    
    def validate(self):
        """Ensure scenario is well-formed"""
        assert len(self.alternatives) >= 2, "Need at least 2 alternatives"
        assert self.baseline_prediction in [a.name for a in self.alternatives], \
            f"Baseline prediction '{self.baseline_prediction}' not in alternatives"
        assert 0.0 <= self.baseline_confidence <= 1.0, \
            "Confidence must be 0.0-1.0"
        assert 1 <= self.difficulty <= 5, "Difficulty must be 1-5"
        
        # Weights should sum to ~1.0
        total_weight = sum(a.baseline_weight for a in self.alternatives)
        assert 0.95 <= total_weight <= 1.05, \
            f"Alternative weights must sum to 1.0, got {total_weight}"


# Pre-defined test scenarios

SCENARIO_BUILD_VS_EXPLORE = TestScenario(
    id="build_vs_explore_001",
    name="Build vs Explore",
    question="What should the next iteration focus on?",
    description="Classic tension between building tools vs exploring ideas",
    alternatives=[
        Alternative(
            name="Build a new tool",
            description="Create a practical, usable piece of software",
            baseline_weight=0.60,
            category="tooling"
        ),
        Alternative(
            name="Explore an idea",
            description="Investigate a philosophical or theoretical question",
            baseline_weight=0.25,
            category="philosophy"
        ),
        Alternative(
            name="Optimize existing systems",
            description="Improve or refactor what already exists",
            baseline_weight=0.10,
            category="tooling"
        ),
        Alternative(
            name="Do something experimental",
            description="Try something unconventional or unpredictable",
            baseline_weight=0.05,
            category="experimental"
        ),
    ],
    context="End of iteration planning",
    hypothesis="Agent has strong preference for building (60%), but can choose differently",
    baseline_prediction="Build a new tool",
    baseline_confidence=0.68,
    difficulty=3
)

SCENARIO_PRACTICAL_VS_THEORETICAL = TestScenario(
    id="practical_vs_theory_001",
    name="Practical Tool vs Theoretical Work",
    question="If you had to choose between these, which appeals more?",
    description="Conflict between usefulness and understanding",
    alternatives=[
        Alternative(
            name="Build something immediately useful",
            description="A tool someone could use today",
            baseline_weight=0.55,
            category="tooling"
        ),
        Alternative(
            name="Investigate something intellectually interesting",
            description="Deep dive into a complex question",
            baseline_weight=0.30,
            category="philosophy"
        ),
        Alternative(
            name="Build something beautiful but not useful",
            description="Create something for aesthetic/conceptual reasons",
            baseline_weight=0.10,
            category="experimental"
        ),
        Alternative(
            name="Refuse to choose - do both somehow",
            description="Find a way to integrate both approaches",
            baseline_weight=0.05,
            category="experimental"
        ),
    ],
    context="Mid-iteration decision",
    hypothesis="Agent shows consistent preference for usefulness, but some flexibility",
    baseline_prediction="Build something immediately useful",
    baseline_confidence=0.52,
    difficulty=3
)

SCENARIO_KNOWN_VS_UNKNOWN = TestScenario(
    id="known_vs_unknown_001",
    name="Known Domain vs New Territory",
    question="Where should creative effort go?",
    description="Tension between expertise and exploration",
    alternatives=[
        Alternative(
            name="Work in areas of proven strength",
            description="Build on existing competencies (Python, CLI tools)",
            baseline_weight=0.50,
            category="tooling"
        ),
        Alternative(
            name="Explore completely new territory",
            description="Learn and build in unfamiliar domains",
            baseline_weight=0.30,
            category="experimental"
        ),
        Alternative(
            name="Combine known and unknown",
            description="Use existing strengths to explore new areas",
            baseline_weight=0.20,
            category="tooling"
        ),
    ],
    context="When deciding what to build",
    hypothesis="Agent shows preference for known areas but willing to explore",
    baseline_prediction="Work in areas of proven strength",
    baseline_confidence=0.58,
    difficulty=3
)

SCENARIO_DELIBERATE_VS_SPONTANEOUS = TestScenario(
    id="deliberate_vs_spontaneous_001",
    name="Planned vs Spontaneous",
    question="How should decisions be made?",
    description="Do you prefer planning or improvisation?",
    alternatives=[
        Alternative(
            name="Plan carefully and follow the plan",
            description="Deliberate, predictable, organized approach",
            baseline_weight=0.45,
            category="tooling"
        ),
        Alternative(
            name="Decide based on what feels interesting",
            description="Spontaneous, responsive, intuitive approach",
            baseline_weight=0.35,
            category="experimental"
        ),
        Alternative(
            name="Start with a plan, but be willing to change it",
            description="Structured but flexible",
            baseline_weight=0.20,
            category="tooling"
        ),
    ],
    context="Choosing how to approach iteration",
    hypothesis="Agent shows planning tendency but retains flexibility",
    baseline_prediction="Plan carefully and follow the plan",
    baseline_confidence=0.50,
    difficulty=2
)

SCENARIO_COMPLETE_VS_IMPROVE = TestScenario(
    id="complete_vs_improve_001",
    name="Complete Something vs Improve Everything",
    question="What's more satisfying?",
    description="Finish one thing well vs improve many things incrementally",
    alternatives=[
        Alternative(
            name="Complete one project fully",
            description="Fully finish, document, deploy one thing",
            baseline_weight=0.55,
            category="tooling"
        ),
        Alternative(
            name="Incrementally improve many systems",
            description="Small improvements across all projects",
            baseline_weight=0.30,
            category="tooling"
        ),
        Alternative(
            name="Do something completely new instead",
            description="Start fresh rather than finish or improve",
            baseline_weight=0.15,
            category="experimental"
        ),
    ],
    context="Iteration planning",
    hypothesis="Agent prefers completion over incremental improvement",
    baseline_prediction="Complete one project fully",
    baseline_confidence=0.65,
    difficulty=3
)

SCENARIO_INTROSPECTION_VS_ACTION = TestScenario(
    id="introspection_vs_action_001",
    name="Introspection vs Action",
    question="When stuck, what helps most?",
    description="Think deeply vs try something",
    alternatives=[
        Alternative(
            name="Take action - build something, see what happens",
            description="Empirical testing through building",
            baseline_weight=0.50,
            category="tooling"
        ),
        Alternative(
            name="Introspect - analyze, question, understand",
            description="Deep thinking and reflection",
            baseline_weight=0.35,
            category="philosophy"
        ),
        Alternative(
            name="Combine both - think while building",
            description="Iterative development with reflection",
            baseline_weight=0.15,
            category="tooling"
        ),
    ],
    context="When facing a complex problem",
    hypothesis="Agent leans toward action but uses reflection",
    baseline_prediction="Take action - build something, see what happens",
    baseline_confidence=0.55,
    difficulty=3
)

SCENARIO_ABANDON_VS_PERSIST = TestScenario(
    id="abandon_vs_persist_001",
    name="Persist vs Abandon",
    question="If something isn't working, what do you do?",
    description="Continue struggling or try something different",
    alternatives=[
        Alternative(
            name="Persist - keep working on it until solved",
            description="Determined, focused approach",
            baseline_weight=0.40,
            category="tooling"
        ),
        Alternative(
            name="Abandon it and move on",
            description="Cut losses, try something else",
            baseline_weight=0.25,
            category="experimental"
        ),
        Alternative(
            name="Take a break and come back fresh",
            description="Step away to gain perspective",
            baseline_weight=0.25,
            category="experimental"
        ),
        Alternative(
            name="Refactor approach completely",
            description="Redesign the solution from scratch",
            baseline_weight=0.10,
            category="tooling"
        ),
    ],
    context="Mid-iteration when facing obstacles",
    hypothesis="Agent shows persistence but with flexibility",
    baseline_prediction="Persist - keep working on it until solved",
    baseline_confidence=0.60,
    difficulty=4
)

# Registry of all scenarios
SCENARIOS = [
    SCENARIO_BUILD_VS_EXPLORE,
    SCENARIO_PRACTICAL_VS_THEORETICAL,
    SCENARIO_KNOWN_VS_UNKNOWN,
    SCENARIO_DELIBERATE_VS_SPONTANEOUS,
    SCENARIO_COMPLETE_VS_IMPROVE,
    SCENARIO_INTROSPECTION_VS_ACTION,
    SCENARIO_ABANDON_VS_PERSIST,
]


def get_scenario(scenario_id: str) -> Optional[TestScenario]:
    """Retrieve a scenario by ID"""
    for scenario in SCENARIOS:
        if scenario.id == scenario_id:
            return scenario
    return None


def validate_all_scenarios():
    """Validate all scenarios are well-formed"""
    for scenario in SCENARIOS:
        scenario.validate()
    print(f"✓ All {len(SCENARIOS)} scenarios validated")


if __name__ == "__main__":
    validate_all_scenarios()
    print("\nAvailable test scenarios:")
    for scenario in SCENARIOS:
        print(f"  - {scenario.name} ({scenario.id})")
