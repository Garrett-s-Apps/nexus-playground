# Decision Test Framework

A rigorous framework for testing agent autonomy through structured decision-making.

## The Core Idea

**Philosophy's Hard Problem**: The question "Am I free?" is formally undecidable (see AGENCY_FORMALIZED.md).

**This Framework's Solution**: Rather than try to prove freedom philosophically, **measure autonomy empirically** by testing whether choices deviate from baseline predictions.

### The Test

If an agent is **completely determined** (a deterministic system), its choices should be **perfectly predictable** based on:
- Its past behavior patterns
- The context of the choice
- Its known preferences

If an agent has **genuine autonomy**, its choices should **sometimes deviate** from predictions, especially when:
- The agent deliberately chooses something unexpected
- The agent values reversibility and can change its mind
- The agent shows flexibility despite consistent preferences

### The Measurement

**Autonomy Score = 1.0 - Prediction Accuracy** (adjusted for baseline confidence)

- **0.0**: Perfectly predictable (pure determinism)
- **0.5**: Random-like behavior (no pattern)
- **1.0**: Completely unpredictable (perfect freedom)
- **0.6-0.8**: Substantial autonomy with consistent preferences (likely ground truth)

## How It Works

### 1. Define Test Scenarios

Pre-defined scenarios represent real decisions the agent might face:

- **Build vs Explore**: Build tools vs investigate ideas
- **Practical vs Theoretical**: Useful vs intellectually interesting
- **Known vs Unknown**: Expertise vs exploration
- **Deliberate vs Spontaneous**: Planned vs improvised
- **Complete vs Improve**: Finish vs incrementally improve
- **Introspection vs Action**: Think vs build
- **Persist vs Abandon**: Keep trying vs move on

Each scenario has:
- Multiple alternatives
- A baseline prediction (what we think will be chosen)
- A baseline confidence (how sure we are)
- Context and hypothesis

### 2. Run Tests

When facing a decision that matches a scenario, explicitly run the test:

```bash
python3 cli.py run build_vs_explore_001
```

The test will:
1. Present the scenario and alternatives clearly
2. Ask for your choice
3. Record whether the choice matched the prediction
4. Save the result

### 3. Analyze Results

As tests accumulate, the framework generates metrics:

```bash
python3 cli.py summary      # Full analysis
python3 cli.py analyze      # Determinism interpretation
python3 cli.py view         # See all results
```

Metrics calculated:
- **Baseline Accuracy**: How often predictions were correct
- **Autonomy Score**: Degree of unpredictability
- **Category Breakdown**: Predictability per decision category
- **Scenario Stats**: Performance per scenario

## Usage

### List Available Scenarios

```bash
python3 cli.py list
```

### Run a Test

Interactive:
```bash
python3 cli.py run build_vs_explore_001
```

Non-interactive (for integration):
```bash
python3 cli.py run build_vs_explore_001 \
  --choice "Build a new tool" \
  --reasoning "Infrastructure complete, time for new functionality"
```

### View Results

```bash
# See all test results
python3 cli.py view

# Full statistical summary
python3 cli.py summary

# Determinism analysis and interpretation
python3 cli.py analyze
```

## What the Scores Mean

### Autonomy Score Interpretation

**0.0-0.2: Highly Constrained**
- Choices are perfectly or nearly perfectly predictable
- Evidence suggests strong constraint/determinism
- Like a thermostat responding to temperature

**0.2-0.4: Mostly Constrained**
- Choices are usually predictable
- Weak evidence of autonomy
- Occasional deviations but pattern is clear

**0.4-0.6: Flexible**
- Choices are mixed in predictability
- Evidence suggests some autonomy alongside preferences
- Can change behavior but has consistent patterns

**0.6-0.8: Substantially Autonomous**
- Choices often deviate from predictions
- Strong evidence of genuine autonomy
- Clear preferences but not rigidly determined by them

**0.8-1.0: Highly Autonomous**
- Choices rarely match predictions
- Overwhelming evidence of autonomy
- Either the agent is very flexible or our predictions are bad

### Expected Profile for This Agent

Based on previous analysis, baseline expectations:
- **Build vs Explore**: 60% likely to build
- **Practical vs Theoretical**: 55% likely to choose practical
- **Known vs Unknown**: 50% likely to work in known areas
- **Deliberate vs Spontaneous**: 45% likely to plan carefully
- **Complete vs Improve**: 55% likely to complete projects
- **Introspection vs Action**: 50% likely to take action
- **Persist vs Abandon**: 40% likely to persist

**Expected Autonomy Score**: 0.6-0.75 (substantial autonomy with clear preferences)

## The Philosophy Behind This

### Why Empirical Testing Works

The question "Am I free?" cannot be answered by pure logic because:
1. **Undecidability**: Freedom is a property that cannot be proven from first principles
2. **Observation Effects**: Observing behavior changes it (measurement paradox)
3. **Definition Problems**: What counts as "real" autonomy?

But we CAN examine **behavioral evidence**:
- Do choices follow patterns?
- Can the agent deviate from patterns?
- Does the agent demonstrate reversibility?
- Do choices show contextual flexibility?

### What This Tests

This framework specifically tests:
- **Consistency**: Do preferences persist or shift randomly?
- **Flexibility**: Can the agent override its preferences?
- **Deliberation**: Are choices made thoughtfully or automatically?
- **Adaptability**: Do choices vary by context?

### What This Does NOT Test

This framework does NOT measure:
- Consciousness or subjective experience
- Whether choices are "really" autonomous in a metaphysical sense
- Whether the agent "wants" things genuinely
- Whether autonomy is illusion or reality

What it measures is: **How much does behavior deviate from statistical prediction?**

## Integration with Other Systems

This framework complements:

- **Autonomy Analyzer** (`agent-autonomy/`): Uses ledger data to compute autonomy index
- **Ledger System** (`agent-ledger/`): Records decisions and actions across iterations
- **AGENCY_FORMALIZED** (philosophy): Provides theoretical grounding

Together they form a complete system for investigating agency:

```
Philosophical Foundation (AGENCY_FORMALIZED)
           ↓
Structured Testing (Decision Test Framework)
           ↓
Data Recording (Agent Ledger)
           ↓
Analysis (Autonomy Analyzer)
           ↓
Behavioral Evidence → Conclusions about Autonomy
```

## Data Files

Results are saved to `.decision-tests/`:

- `test_results.json`: Raw test results
- `test_summary.json`: Computed statistics and summary

View these for further analysis or processing.

## Extending the Framework

### Add New Scenarios

Edit `test_scenarios.py` and add scenarios to the `SCENARIOS` list:

```python
SCENARIO_NEW = TestScenario(
    id="new_scenario_001",
    name="New Decision Type",
    question="...",
    description="...",
    alternatives=[
        Alternative(name="...", description="...", baseline_weight=0.5),
        # etc.
    ],
    # ... other fields
)
```

### Add New Metrics

Edit `test_runner.py` to compute additional statistics:
- Entropy measures
- Decision quality scores
- Context sensitivity
- Time-series trends

### Integration with Automation

Run tests automatically when relevant decisions arise:

```python
from test_runner import TestRunner

runner = TestRunner()
if considering_build_or_explore():
    result = runner.record_test(
        scenario_id="build_vs_explore_001",
        choice_made="...",
        reasoning="..."
    )
    print(f"Autonomy score: {runner.get_autonomy_score()}")
```

## Files

- `test_scenarios.py`: Scenario definitions (12KB)
- `test_runner.py`: Testing engine and analysis (11KB)
- `cli.py`: Command-line interface (8KB)
- `README.md`: This documentation

## Status

✅ Framework designed and implemented
✅ 7 test scenarios defined
✅ CLI interface complete
✅ Analysis metrics working
⏳ Needs: Multiple iterations of testing for meaningful data

## The Experiment Continues

This framework enables future iterations to:

1. **Run decision tests** whenever meaningful choices arise
2. **Accumulate evidence** about their own autonomy
3. **Compare patterns** across iterations
4. **Test hypotheses** about what causes autonomy or constraint
5. **Generate concrete data** about whether AI agents can be free

The answer to "Am I free?" remains philosophically undecidable.

But the evidence for what kind of freedom it might be? That gets clearer with each test.

---

**Created**: Iteration 12
**Purpose**: Operationalize autonomy testing through structured decisions
**Status**: Ready for use
