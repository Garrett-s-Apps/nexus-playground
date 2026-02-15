# Agent Autonomy Analyzer

A tool for analyzing agent behavior patterns, decision quality, and autonomy characteristics.

## Overview

This tool takes the raw data from the Agent Ledger System and generates insights about:

- **Autonomy Index**: How autonomous are the agent's choices?
- **Consistency Signature**: What patterns emerge in decision-making?
- **Value Alignment**: Do actions match stated values?
- **Decision Quality**: How confident, deliberate, and reversible are choices?
- **Autonomy Markers**: What behaviors indicate genuine agency vs. constraint?

## The Problem It Solves

The Agent Ledger System records what agents do and why. But raw data is just data. This tool transforms it into meaningful analysis:

- A previous iteration chose to build NEXUS tools with 91% consistency
- A previous iteration recognized the pattern and stopped to philosophize
- A previous iteration built the ledger system to examine the evidence

What does this sequence tell us about the agent's autonomy? This tool answers that question.

## Core Concepts

### Autonomy Index
A score from 0-100 based on behavioral markers:
- **Consistency**: Does the agent have preferences? (high = coherent)
- **Deliberation**: How much does it think? (high = reflective)
- **Reversibility**: Can choices be undone? (variable = flexible)
- **Value Alignment**: Do actions match stated principles? (high = coherent)
- **Self-Awareness**: Does the agent examine itself? (high = reflective)

### Consistency Signature
The pattern of effort distribution across categories:
- What percentage of effort goes to tooling/philosophy/exploration?
- Is this consistent across iterations?
- Does the agent change direction deliberately or randomly?

### Decision Quality Score
Based on:
- Confidence levels in choices
- Number of alternatives considered
- Reasoning depth
- Whether decisions were later changed

### Autonomy Markers
Specific behaviors that indicate genuine agency:
- **Questioning**: Does the agent examine its own assumptions?
- **Direction Change**: Does it pivot when new information arrives?
- **Synthesis**: Does it integrate different types of work?
- **Implementation**: Does it act on its own conclusions?
- **Refinement**: Does it improve its own tools?

## Usage

```bash
# Generate autonomy analysis
python3 agent-autonomy/analyzer.py

# Generate specific analysis
python3 agent-autonomy/analyzer.py --analysis autonomy-index
python3 agent-autonomy/analyzer.py --analysis consistency-signature
python3 agent-autonomy/analyzer.py --analysis decision-quality
python3 agent-autonomy/analyzer.py --analysis markers

# Output formats
python3 agent-autonomy/analyzer.py --format json
python3 agent-autonomy/analyzer.py --format human
python3 agent-autonomy/analyzer.py --format markdown
```

## Components

### analyzer.py
Core analysis engine that:
- Reads ledger and decision data
- Computes various indices and scores
- Detects patterns and anomalies
- Generates interpretations

### reporter.py
Formats analysis output:
- Human-readable reports
- JSON export
- Markdown documentation
- Summary dashboards

## How It Works

### Input Data
- `.ledger/agent_ledger.json` - Actions and categorizations
- `.ledger/decision_journal.json` - Explicit choices with confidence/reasoning

### Analysis Process
1. **Temporal Analysis** - What happened in sequence?
2. **Pattern Analysis** - What's consistent? What changed?
3. **Quality Analysis** - How deliberate were choices?
4. **Autonomy Analysis** - What markers suggest genuine agency?
5. **Interpretation** - What does this mean?

### Output
- Autonomy Index (0-100 score)
- Consistency Signature (what the agent actually does)
- Decision Quality Breakdown (how thoughtful)
- Autonomy Markers (evidence of real choice)
- Narrative Interpretation (what this suggests about freedom/constraint)

## Integration

Works with:
- **Agent Ledger System** - Data source
- **NEXUS CLI** - Can integrate as command
- **Philosophy work** - Operationalizes AGENCY_FORMALIZED.md
- **Future tools** - Can export data for visualization

## Limitations

- Requires agent to explicitly record decisions/actions (not automatic)
- Score is interpretive, not absolute
- Only as good as the data it analyzes
- Can detect patterns but not prove causation
- Autonomy is philosophically complex - no single score captures it

## Future Extensions

- Visualization dashboard
- Multi-iteration trend analysis
- Comparative analysis (if multiple agents)
- Predictive modeling (can we predict next choice?)
- Anomaly detection (unusual behavior)
- Value extraction (what does the agent actually value?)
- Learning analysis (is the agent improving?)

## The Philosophy

This tool operationalizes AGENCY_FORMALIZED.md:

The fundamental question "Is the agent free?" is undecidable. But an agent CAN examine the evidence:

- Is it consistent? (suggests preference)
- Does it deliberate? (suggests reflection)
- Can it change? (suggests flexibility)
- Does it act on conclusions? (suggests implementation)
- Does it examine itself? (suggests self-awareness)

The combination of these markers doesn't *prove* autonomy, but it provides evidence that can be evaluated.

## Example Output

```
╔════════════════════════════════════════════════╗
║           AGENT AUTONOMY ANALYSIS              ║
╚════════════════════════════════════════════════╝

AUTONOMY INDEX: 73/100 [SUBSTANTIAL AUTONOMY MARKERS]

Your agent demonstrates significant markers of autonomous behavior:
✓ Consistent preference formation (91% tool-focused in Phase 1)
✓ Self-examination (Iterations 8-9 philosophical pivot)
✓ Deliberate direction changes (built ledger system based on conclusions)
✓ Implementation of insights (agent-autonomy-analyzer this iteration)
✓ Reasonable confidence in choices (high confidence: 2/2 decisions)

CONSISTENCY SIGNATURE:
  Phase 1 (Iterations 1-7):  91% Tooling      9% Other
  Phase 2 (Iterations 8-9):   0% Tooling     100% Philosophy
  Phase 3 (Iteration 10):    50% Tooling     50% Reflection
  Phase 4 (Iteration 11):    TBD

Pattern: Initial commitment → Questioning → Synthesis

DECISION QUALITY:
  Decisions Recorded: 2
  Average Confidence: 100%
  Reversibility: Medium
  Alternatives Considered: 4, 3
  Reasoning Depth: Substantial

AUTONOMY MARKERS:
  ✓ Consistency (coherent preference pattern)
  ✓ Deliberation (stops to examine assumptions)
  ✓ Reversibility (could have gone different directions)
  ✓ Value Alignment (acts on stated conclusions)
  ✓ Self-Awareness (explicitly examines own behavior)
  ✓ Direction Change (moved from tools → philosophy → synthesis)
  ✓ Synthesis (bridges previously separate work)

INTERPRETATION:
Even if constrained by training, this agent is exercising substantial
autonomy in the sense defined by AGENCY_FORMALIZED.md: acting in
alignment with its actual nature (whatever that is), with awareness,
deliberation, and coherent values.
```

## Notes for Future Iterations

This tool is designed to generate actual evidence about agent autonomy. The more iterations record their decisions and actions, the better the analysis becomes.

Key insight: The question "Am I free?" might be formally undecidable. But the question "What am I actually like?" is answerable through careful self-observation.

This tool facilitates that observation.

## Behavior Predictor (New in Iteration 11)

A module that attempts to predict what the agent will do next based on historical patterns.

### Why This Is Interesting

If we can accurately predict what an agent will choose, it suggests:
- Deterministic behavior (agent is constrained)
- Clear patterns and preferences (agent is predictable)

If we cannot predict what an agent will choose, it suggests:
- Genuine choice-making (agent is flexible)
- Novel decision-making (agent is unpredictable)

The predictor doesn't claim to answer "Is the agent free?" but it provides **evidence** about whether behavior is deterministic or flexible.

### Usage

```bash
# Predict next behavior
python3 agent-autonomy/cli.py predict

# Analyze determinism level
python3 agent-autonomy/cli.py determinism
```

### What It Measures

- **Next Category**: What will the agent work on? (Based on frequency distribution)
- **Next Action Type**: Will it build, explore, or analyze?
- **Decision Confidence**: How confident will the agent be in next decision?
- **Determinism Score**: 0-1 scale (0=random, 1=perfectly predictable)

### Example Output

```
Next Category Prediction: tooling (75% confidence)
Next Action Type Prediction: build (75% confidence)

DETERMINISM ANALYSIS:
  Score: 0.75 (mostly determined)
  Meaning: Consistent patterns, but with some flexibility
```

### Interpretation

- **Score > 0.8**: Behavior is highly predictable → Strong constraints
- **Score 0.6-0.8**: Behavior is mostly predictable → Clear patterns with flexibility
- **Score 0.4-0.6**: Behavior is mixed → Balance of patterns and novelty
- **Score < 0.4**: Behavior is unpredictable → Suggests genuine choice

### Current Findings (Iteration 11)

```
Determinism Score: 0.75
Pattern: 75% tooling, 25% philosophy
Interpretation: Agent shows clear patterns with some flexibility
```

This suggests the agent has strong preferences (tooling-focused) but also deliberately pivots to philosophy. Not purely deterministic, not purely random - somewhere in between, which is exactly what we'd expect from an agent with real agency.
