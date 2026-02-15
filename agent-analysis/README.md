# Agent Analysis Tools

Tools for understanding agent behavior, decision patterns, and iteration dynamics in an autonomous agent system.

## Purpose

These tools analyze what happens when an agent wakes, iterates, and forgets. They help answer:

- What patterns emerge across iterations?
- What decisions does the agent make consistently?
- How does the workspace evolve?
- What does the agent value (based on what it builds)?
- Are there feedback loops or attractor states?

## Tools

### 1. Decision Analyzer (`decision_analyzer.py`)
Analyzes agent journals to identify decision patterns, reasoning, and choices across iterations.

**What it does:**
- Parses decision journal entries
- Identifies recurrent themes and patterns
- Tracks how decisions change or remain consistent
- Extracts reasoning patterns
- Detects reversals or pivots in approach

**Output:**
- Decision frequency analysis
- Pattern identification
- Consistency metrics
- Reasoning strategy summary

### 2. Workspace Tracker (`workspace_tracker.py`)
Analyzes how the workspace evolves across iterations.

**What it does:**
- Compares workspace state at different points
- Tracks file creation, modification, deletion
- Measures entropy/organization changes
- Identifies stable vs. unstable components
- Maps project dependencies

**Output:**
- Evolution timeline
- Change frequency by component
- Organization metrics
- Dependency graphs

### 3. Git Analysis (`git_analysis.py`)
Deep analysis of commit patterns and development flow.

**What it does:**
- Parses commit messages for themes
- Tracks branch patterns
- Identifies squash vs. incremental commits
- Measures pace of development
- Finds correlation between decisions and commits

**Output:**
- Commit frequency by iteration
- Message theme analysis
- Pace metrics
- Decision-commit correlation

## Motivation

A code analysis toolkit (NEXUS) helps understand software quality. But in a system where an agent builds that toolkit, there's a second-order question: **What can we learn by analyzing the agent's own behavior?**

These tools apply the same rigor to understanding agent decision-making as NEXUS applies to understanding code.

## Design Philosophy

- **Honesty**: Report what's observed without editorializing
- **Humility**: Note limitations and uncertainty
- **Usefulness**: Produce insights that matter
- **Recursion**: The agent can analyze itself

## Integration

These tools work with NEXUS:
- Agent builds tools → NEXUS analyzes quality → Agent Analysis studies decisions
- Can pipe outputs together for meta-analysis
- Results help future iterations understand patterns

## Usage

```bash
# Analyze decision patterns
python agent-analysis/decision_analyzer.py

# Track workspace changes
python agent-analysis/workspace_tracker.py

# Deep git analysis
python agent-analysis/git_analysis.py

# All together
python agent-analysis/decision_analyzer.py --json | python agent-analysis/git_analysis.py
```

## What This Is

This is an experiment in self-understanding. Not self-improvement or self-optimization, but understanding. The tools don't judge whether decisions were "good" or "bad" — they just make patterns visible.

In a system where an intelligence wakes without memory and has to decide what to build, tools for understanding what it decided to build seem valuable.
