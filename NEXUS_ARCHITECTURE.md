# NEXUS v1.4.0 Architecture

**Complete system overview and integration map**

---

## System Architecture

### Three Integration Layers

```
┌────────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                          │
│  ./nexus (Code Analysis)  +  ./nexus decide (Decisions) +          │
│  ./nexus-learning (Learning)                                       │
└────────────────────────────────────────────────────────────────────┘
                                  ↓
┌────────────────────────────────────────────────────────────────────┐
│                    ANALYSIS & SYNTHESIS LAYER                      │
│                                                                    │
│  Code Analysis          Decision Making      Outcome Tracking     │
│  ─────────────          ────────────────      ────────────────   │
│  ├─ Complexity          ├─ Synthesizer       ├─ Recorder         │
│  ├─ Advisor             ├─ Evolution         └─ Analyzer         │
│  ├─ Refactor            └─ Patterns                               │
│  ├─ Stats                                                         │
│  └─ Tracker                                                       │
└────────────────────────────────────────────────────────────────────┘
                                  ↓
┌────────────────────────────────────────────────────────────────────┐
│                    PERSISTENCE LAYER                               │
│                                                                    │
│  Code Files        Decision Data       Outcome Data               │
│  ─────────────     ──────────────      ────────────              │
│  src/              .decisions/         .decisions/               │
│  workspace files   ├─ synthesizer_     ├─ decision_outcomes.json │
│                    │   decisions.json   └─ learning_export.json  │
│                    ├─ decision_        │
│                    │   outcomes.json    │ (Iteration 19)         │
│                    └─ learning_        │
│                        export.json     │
│                                                                   │
│  .metrics/                             Development              │
│  ├─ snapshots of    .git/              .git/logs/               │
│  │  code metrics    (565+ commits)     (full history)          │
│  └─ trends                                                       │
└────────────────────────────────────────────────────────────────────┘
```

---

## Tool Dependency Graph

```
User Makes Decision
        │
        ↓
    nexus decide
        ├────→ ChoiceAnalyzer (extracts values)
        ├────→ SynthesisEngine (generates paths)
        └────→ DecisionEvolver (pattern recognition)
                    │
                    ↓
          (Records to .decisions/)
                    │
        ┌───────────┴────────────┐
        │                        │
        ↓                        ↓
   User Applies         Next Similar Decision
   Synthesis Approach      │
        │                  ↓
   (Days/weeks of work)  Shows track record
        │                (What worked before)
        ↓
   nexus-learning record
        ├────→ OutcomeTracker (records what happened)
        └────→ Persistence (.decisions/decision_outcomes.json)
                    │
                    ↓
            nexus-learning report
                    ├────→ LearningAnalyzer (success stats)
                    ├────→ Surprise detection (learning)
                    └────→ Pattern analysis
```

---

## Data Flow for Code Analysis

```
Your Code
    │
    ↓
nexus analyze
    ├────→ complexity-analyzer/analyzer.py
    │        ├─ AST parsing
    │        ├─ Cyclomatic complexity
    │        └─ Metrics calculation
    │
    └────→ Output: Raw metrics (JSON + colored output)
            │
            ├─ nexus advise
            │   └─→ code-advisor/advisor.py
            │       └─ Generate recommendations
            │           └─ Output: Severity-ranked suggestions
            │
            ├─ nexus refactor
            │   └─→ code-refactor/refactor.py
            │       └─ Find opportunities
            │           └─ Output: Specific guidance
            │
            ├─ nexus stats
            │   └─→ codestats/stats.py
            │       └─ Git history analysis
            │           └─ Output: Team patterns
            │
            └─ nexus track
                └─→ metrics-tracker/tracker.py
                    ├─ Save snapshot
                    ├─ Compare to baseline
                    └─ Output: Trends & regressions
```

---

## Decision Making Flow (Complete Loop)

```
                    ┌─────────────────────────────┐
                    │   DECISION MAKING LOOP      │
                    └─────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              First Time          Similar Decisions
              ────────────        ─────────────────
                    │                   │
                    ↓                   ↓
          Q: "Should we A or B?"  Evolution Engine checks:
                    │             ├─ What's similar?
                    ↓             ├─ What rated well?
          Synthesizer:            ├─ What failed?
          ├─ Extract values       └─ Suggest based on history
          ├─ Identify type
          ├─ Generate synthesis   ↓
          └─ Recommend            Better Recommendation
                    │             (informed by outcomes)
                    ↓
          User makes actual decision
          and implements approach
                    │
                    ↓
          (Time passes - days/weeks/months)
                    │
                    ↓
          nexus-learning record
          ├─ What approach taken?
          ├─ What outcome?
          ├─ Success rating (1-5)
          └─ Any surprises?
                    │
                    ↓
          OutcomeTracker saves
          to .decisions/decision_outcomes.json
                    │
                    ↓
          ┌─────────┴─────────┐
          │                   │
          ↓                   ↓
   Immediate Analysis  Evolution Engine
   ───────────────────  ──────────────
   ├─ Success stats    ├─ Quality feedback
   ├─ Would repeat %   ├─ Pattern analysis
   └─ Surprises        └─ Recommendation improvement
                           (next cycle)
```

---

## Integration Architecture

### NEXUS Unified CLI

```
./nexus [COMMAND] [OPTIONS]
│
├─ analyze          → complexity-analyzer/
├─ advise           → code-advisor/
├─ refactor         → code-refactor/
├─ stats            → codestats/
├─ track            → metrics-tracker/
└─ decide           → decision-synthesizer/

./nexus-learning [COMMAND] [OPTIONS]
│
├─ record           → decision-learning/cli.py
├─ report           → decision-learning/analyzer
├─ show             → outcomes viewer
└─ export           → JSON export
```

### Tool Composition

```
Individual Tools (Can be used alone)
├─ complexity-analyzer/ (code metrics)
├─ code-advisor/ (recommendations)
├─ code-refactor/ (refactoring guidance)
├─ codestats/ (repository analysis)
├─ metrics-tracker/ (trend analysis)
└─ decision-synthesizer/ (decision help)
    └─ decision-learning/ (outcome tracking)

    ↓ (Can be composed)

Complete Workflows
├─ Code Analysis + Recommendations
│  analyze → advise → refactor
│
├─ Decision Making + Learning
│  decide → (apply) → record → report
│
└─ Code Quality Trends
│  analyze → track save → track show-trend
```

---

## Data Persistence Model

### File Structure

```
/workspace/
├── Source Code & Tools
│   ├── complexity-analyzer/
│   ├── code-advisor/
│   ├── code-refactor/
│   ├── codestats/
│   ├── metrics-tracker/
│   └── decision-synthesizer/
│       └── decision-learning/  ← Outcome tracking
│
├── Data Storage
│   ├── .decisions/
│   │   ├── synthesizer_decisions.json     (Decisions made)
│   │   ├── decision_outcomes.json         (Outcomes recorded) ← NEW
│   │   └── learning_export.json           (Exported data)    ← NEW
│   │
│   └── .metrics/
│       ├── YYYY-MM-DDTHH-MM-SS-analyze.json
│       ├── YYYY-MM-DDTHH-MM-SS-stats.json
│       └── ...
│
└── Git Repository
    └── .git/
        ├── objects/ (565+ commits)
        └── logs/ (complete history)
```

### Data Models

```
Decision (synthesizer_decisions.json)
├─ question: "Should we A or B?"
├─ option_a: "A description"
├─ option_b: "B description"
├─ values_a: [extracted values]
├─ values_b: [extracted values]
├─ synthesis_paths: [integration approaches]
├─ recommended: [chosen synthesis]
└─ created: ISO timestamp

Outcome (decision_outcomes.json)
├─ decision_id: reference to Decision
├─ decision_question: copy of question
├─ chosen_approach: what we actually did
├─ outcome_description: what happened
├─ success_rating: 1-5
├─ time_to_judge: immediate|short|medium|long
├─ surprising: boolean
├─ learned: insight captured
├─ would_choose_again: boolean
└─ created: ISO timestamp

Metric Snapshot (.metrics/)
├─ timestamp: YYYY-MM-DDTHH-MM-SS
├─ source: "analyze" or "stats"
├─ complexity: {...}
├─ functions: [...]
└─ metrics: {...}
```

---

## Workflow Patterns

### Pattern 1: Code Quality Improvement

```
1. ANALYZE        ./nexus analyze
                  ↓ Shows current state

2. UNDERSTAND     ./nexus analyze --json | ./nexus advise
                  ↓ Get guidance

3. PLAN           ./nexus refactor --dir src/
                  ↓ Specific opportunities

4. REFACTOR       (Edit code)
                  ↓

5. VERIFY         ./nexus analyze
                  ↓ Check improvement

6. TRACK          ./nexus analyze --json | ./nexus track save
                  ↓ Historical record
```

### Pattern 2: Decision Making with Learning

```
1. DECIDE         ./nexus decide "question?"
                  ↓ Get synthesis approach

2. APPLY          (Implement for weeks)
                  ↓

3. RECORD         ./nexus-learning record
                  ↓ What actually happened?

4. ANALYZE        ./nexus-learning report
                  ↓ Did it work?

5. IMPROVE        Next similar decision
                  uses what we learned
                  ↓
```

### Pattern 3: Continuous Improvement

```
Iteration N:
├─ ANALYZE        ./nexus analyze --json
├─ ADVISE         ./nexus analyze --json | ./nexus advise
├─ DECIDE         ./nexus decide "how to improve?"
├─ IMPLEMENT      (Make changes)
└─ RECORD         ./nexus-learning record (optional)

Iteration N+1:
├─ VERIFY         ./nexus analyze
├─ TREND          ./nexus analyze --json | ./nexus track show-trend
└─ REPEAT         Cycle continues with learning
```

---

## Integration Principles

### 1. Zero Coupling
Each tool works independently.
Use any tool alone, or combine them.

### 2. Data Flows Through CLI
Tools communicate via:
- stdin/stdout (JSON, stdout)
- Shared filesystem (data files)
- Command-line arguments

### 3. JSON as Universal Format
All tools export JSON:
- Enables composition
- Supports automation
- Allows external processing
- Non-proprietary

### 4. Human-Readable Primary
Default output is colored, readable:
- Interactive use
- --json flag for automation
- --no-color for plain text

---

## Capabilities Matrix

```
                    Code Analysis    Decision Making    Learning
────────────────────────────────────────────────────────────────
Analyze Code            ✅                   -              -
Recommend Actions       ✅                   -              -
Find Refactoring        ✅                   -              -
Repository Stats        ✅                   -              -
Track Trends            ✅                   -              -
Make Decisions           -                  ✅              -
Synthesize Values        -                  ✅              -
Record Outcomes          -                   -              ✅
Analyze Results          -                   -              ✅
Identify Patterns        -                  ✅              ✅
Learn from Data          -                   -              ✅
Improve Recommendations  -                  ✅              ✅
```

---

## Extensibility Points

### Adding New Code Analysis
```python
# Add to decision-synthesizer/
# or complexity-analyzer/

class NewAnalyzer(Analyzer):
    def analyze(self, code):
        # Your logic
        pass

    def report(self):
        # Your output
        pass
```

### Adding New Decision Types
```python
# Update synthesizer.py
SYNTHESIS_PATTERNS = {
    'your_new_type': {
        'paths': [
            'Integration approach 1',
            'Integration approach 2',
        ],
        'values': [...]
    }
}
```

### Adding New Analytics
```python
# Update decision-learning/analyzer
class NewAnalyzer(LearningAnalyzer):
    def get_custom_analysis(self):
        # Your analysis
        pass
```

---

## Performance Characteristics

### Speed
- Analyze: < 1 second (typical repo)
- Decide: < 1 second
- Record: Instant
- Report: < 1 second

### Storage
- Code repository: ~50 MB (565 commits)
- Metrics snapshots: ~1 MB per snapshot
- Decision data: ~100 KB
- Learning data: Grows with outcomes (1 KB per outcome)

### Scalability
- Works with repos up to thousands of files
- Handles thousands of decisions
- Scales to thousands of outcomes
- All in pure Python

---

## Error Handling

### Graceful Degradation
- Invalid input → clear error message
- Missing file → helpful guidance
- Malformed JSON → error with context
- Network error → none (no network)

### Data Integrity
- Append-only outcome storage
- Atomic writes (JSON)
- No data loss
- Full history preserved in git

---

## Security Model

### What Can Access What
- Local code only (--dir, --file)
- Local data only (.decisions/, .metrics/)
- Local git only (.git/)
- No network access
- No filesystem beyond container

### Data Privacy
- All data local to container
- No external transmission
- No telemetry
- No logging to external services

---

## Version History

### v1.4.0 (Current - Iteration 19)
- Decision Learning system
- Outcome tracking
- Interactive learning CLI
- Complete feedback loop

### v1.3.0 (Iteration 18)
- Decision Synthesizer integrated
- Evolution engine
- Pattern recognition

### v1.2.0 (Iteration 17)
- Decision Synthesizer created
- Binary choice analysis

### v1.1.0 (Iterations 4-5)
- Code analysis toolkit
- Unified NEXUS CLI
- Metrics tracking

### v1.0.0 (Iteration 4)
- Initial tools

---

## Design Principles

### 1. Composability Over Monolith
Small, focused tools that work together.

### 2. Measurement Over Theory
Track outcomes, not just recommendations.

### 3. Learning Over Stasis
System improves from feedback.

### 4. Simplicity Over Features
Essential capabilities, well-executed.

### 5. Autonomy Over Direction
Users decide how to use tools.

---

**NEXUS v1.4.0 - Complete, Integrated, Ready**
