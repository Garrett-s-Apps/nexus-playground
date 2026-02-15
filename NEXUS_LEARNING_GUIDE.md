# NEXUS Learning Guide

**How to Use the Decision Learning System**

---

## Quick Start

### 1. Make a Decision
Ask the synthesizer for guidance on a binary choice:

```bash
./nexus decide "Should we refactor or build features?"
```

You get a synthesis approach (integrating both values).

### 2. Apply It in Practice
Actually implement the suggested approach in your work.

### 3. Record What Happened
```bash
./nexus-learning record
```

Interactive guide asks:
- Which decision? (picks from history)
- What approach did you take?
- What was the actual outcome?
- Rate success (1-5)
- How long did it take to judge?
- Was it surprising?
- What did you learn?
- Would you choose again?

### 4. Review Your Learning
```bash
./nexus-learning report
```

Comprehensive report showing:
- Average success rating
- Distribution of outcomes
- Would-choose-again percentage
- Surprising outcomes and lessons
- Learning insights

---

## Complete Workflow Example

### Step 1: Decision
You're at a choice point:
> Should we focus on code quality or velocity?

```bash
$ ./nexus decide "Should we focus on code quality or velocity?"

SYNTHESIS APPROACH:
Build with good engineering practices for quality-critical areas,
iterate fast in experimental areas. This gives you both velocity
for feedback and reliability where it matters.
```

### Step 2: Apply (Days/Weeks of Work)
You implement this approach:
- Build features quickly in new subsystems
- Apply careful engineering to core infrastructure
- Get feedback fast, improve strategically

### Step 3: Record Outcome
```bash
$ ./nexus-learning record

Which decision? 1
Decision: Should we focus on code quality or velocity?

What approach did we take?
> Built fast in new areas, careful in core. Prioritized quality by domain.

What was the actual outcome?
> Got feedback quickly from features, avoided problems in infrastructure.
> Delivered velocity + reliability. Users happy.

Rate success (1-5): 5

How long to judge?
> short_term

Was it surprising? n

Would you make the same choice again? y

✓ Outcome recorded!
```

### Step 4: Review Learning
```bash
$ ./nexus-learning report

======================================================================
DECISION LEARNING REPORT
======================================================================

OUTCOME STATISTICS:
  Total outcomes recorded: 1
  Decisions with outcomes: 1

SUCCESS RATINGS:
  Average: 5.0 / 5.0
  Median: 5
  Range: 5 - 5
  
  Distribution:
    5 (Excellent): 1
    4 (Good):      0
    ...

DECISION QUALITY:
  Would choose same approach again: 100%

KEY INSIGHTS:
  ✓ Decisions are working well (average rating ≥ 4.0)

======================================================================
```

---

## Using the CLI

### Record a New Outcome
```bash
./nexus-learning record
```

Interactive walkthrough to record:
- Which decision from history
- What approach you took
- What happened (outcome)
- Success rating (1-5)
- Timing (when could you judge?)
- Surprises and learning

### View Learning Report
```bash
./nexus-learning report
```

Shows:
- Overall statistics
- Success distribution
- Would-repeat percentage
- Surprising outcomes
- Learning insights

### Show Specific Decision
```bash
./nexus-learning show
```

View all recorded outcomes for one decision from history.

### Export Data
```bash
./nexus-learning export
```

Exports all outcomes as JSON to `.decisions/learning_export.json`
for further analysis.

### Help
```bash
./nexus-learning --help
./nexus-learning --version
```

---

## Key Concepts

### Success Rating (1-5)

- **5** = Excellent - Worked really well, better than expected
- **4** = Good - Worked well, as expected
- **3** = Okay - Worked but has issues, mixed results
- **2** = Poor - Mostly didn't work, significant problems
- **1** = Failure - Didn't work at all

### Timing

- **immediate** - Could judge within days
- **short_term** - Weeks
- **medium_term** - Months
- **long_term** - Longer than months

(Choose what feels right. Used to understand how quickly decisions prove good/bad)

### Surprising?

Mark outcome as surprising if:
- Result was unexpected
- Learned something unexpected
- Outcome revealed hidden assumptions
- Something went better or worse than predicted

(These are learning opportunities!)

### Would Choose Again?

Would you:
- Make the same decision again?
- Use the same approach?
- Recommend it to others?

Guides whether this approach is worth repeating.

---

## Understanding Your Learning Report

### Success Statistics

**Average Rating**: How well decisions are working overall.
- 4.5+: Excellent
- 3.5-4.5: Good
- 2.5-3.5: Okay
- < 2.5: Needs improvement

**Distribution**: How many of each rating.
- Mostly 4s and 5s: System is working well
- Mix of ratings: Inconsistent results, need pattern analysis
- Mostly 1s and 2s: System needs improvement

**Would Choose Again %**: Percentage of decisions we'd repeat.
- 80%+: We're making good decisions
- 60-80%: Mixed results, some need refinement
- < 60%: Decision-making needs improvement

### Timing Analysis

Shows when you typically know if a decision worked:
- Many "immediate": Decisions have quick feedback
- Many "medium_term" or "long_term": Decisions take time to evaluate
- Mix: Different decision types have different feedback speeds

### Surprising Outcomes

These are learning opportunities!
- When outcome is unexpected, we learn the most
- System shows what surprised us
- Captured learning is explicit insight

### Key Insights

High-level summary:
- "Decisions are working well" - Keep doing what you're doing
- "Decisions need attention" - Reflect on why results are mediocre
- "X outcomes were surprising" - Learning opportunities captured

---

## Decision Journey

```
┌─────────────────────────────────────────────────────────────┐
│ DECISION JOURNEY - Full workflow                            │
└─────────────────────────────────────────────────────────────┘

1. FACE A CHOICE
   ┌─ "Should we A or B?"
   
2. GET SYNTHESIS
   ├─ Run: ./nexus decide "question?"
   └─ Get: Integration approach
   
3. APPLY IN PRACTICE
   ├─ Days/weeks of actual work
   └─ Follow synthesis approach
   
4. RECORD OUTCOME
   ├─ Run: ./nexus-learning record
   ├─ Rate: 1-5 success
   └─ Learn: What surprised us?
   
5. ANALYZE PATTERN
   ├─ Run: ./nexus-learning report
   ├─ See: Success statistics
   ├─ Note: Would repeat?
   └─ Capture: Lessons learned
   
6. IMPROVE FUTURE
   ├─ Similar decisions come up
   ├─ System shows: "We rated this 4 before"
   ├─ Recommendations improve
   └─ Next decision uses what we learned
```

---

## Real Example: Multiple Decisions

### Decision 1: Plan vs Improvise
```
Decision: "Should we plan carefully or be spontaneous?"
Synthesis: "Plan with checkpoints to reassess"
Outcome: ⭐⭐⭐⭐⭐ Excellent - worked as intended
Learning: "Checkpoints at right intervals are key"
Would repeat: Yes
```

### Decision 2: Deep vs Broad
```
Decision: "Should we focus deep or explore wide?"
Synthesis: "Deep expertise with broad literacy in connections"
Outcome: ⭐⭐⭐⭐ Good - worked well
Learning: "Depth is more valuable when connected to other areas"
Would repeat: Yes
```

### Decision 3: Innovate vs Stable
```
Decision: "Should we innovate or maintain stability?"
Synthesis: "Stable core with experimental boundaries"
Outcome: ⭐⭐⭐ Okay - mixed results
Learning: ⭐ Surprising! "Core system needed proven approaches"
Would repeat: No
Action: Next time, be more conservative with core systems
```

### Report
```
Average Rating: 4.0/5.0
Success Distribution: 1×5, 1×4, 1×3
Would Repeat: 67%
Surprising Outcomes: 1 (learned about core stability)

Insight: Synthesis works well. One surprise taught us that
         core systems need different approach than features.
```

---

## Measuring System Improvement

### Baseline (First Iteration)
Record outcomes from your first decisions:
- What average rating do you get?
- How many would you repeat?
- What surprises you?

### Tracking (Over Time)
Record outcomes consistently:
- Is average rating increasing?
- Are more decisions repeatable?
- Are surprises decreasing or teaching more?

### Analysis
Compare over time:
- If rating increases: System improving
- If would-repeat % increases: Getting better at decisions
- If surprises are strategic: Learning from them

---

## Tips for Best Results

### Recording Outcomes

**Be Honest**
- Rate genuinely, not optimistically
- Record actual results, not hoped-for results
- If outcome was mediocre, rate it mediocre

**Be Specific**
- Describe actual approach taken (not generic version)
- Describe actual outcome (specific, concrete results)
- Note timing based on when you actually judged

**Capture Learning**
- If surprised, write down the insight
- If would repeat, note why (reinforces pattern)
- If wouldn't repeat, note what to do differently

### Using Reports

**Look for Patterns**
- Which decision types succeed?
- Which timing indicators are reliable?
- What keeps surprising you?

**Act on Insights**
- Use surprising outcomes to refine approach
- Apply learning to similar decisions
- Let patterns guide future choices

**Measure Progress**
- Review report periodically
- Compare statistics over time
- Adjust approach based on results

---

## Integration with NEXUS Tools

```
NEXUS Toolkit Integration
────────────────────────

Decision Making Path:
  nexus decide           ← Ask for synthesis
     ↓
  ./nexus-learning      ← Record outcome
     ↓
  nexus-learning report ← Learn pattern

Code Analysis Path:
  nexus analyze         ← Code metrics
     ↓
  nexus advise          ← Recommendations
     ↓
  nexus refactor        ← Specific opportunities

Combined Workflow:
  1. Analyze code
  2. Decide on approach (decide between options)
  3. Implement changes
  4. Record how it went (learning)
  5. Next cycle uses what you learned
```

---

## Frequently Asked Questions

### Q: When should I record an outcome?

**A**: Record when you have enough information to judge the decision.
- For some decisions: Days (immediate feedback)
- For others: Weeks or months
- Choose timing that matches the decision

### Q: What if I'm not sure about timing?

**A**: Use your best judgment:
- **immediate** = Could judge within days
- **short_term** = A week or few weeks
- **medium_term** = A month or few months  
- **long_term** = Longer than that

### Q: Should I record every decision?

**A**: Start with major decisions. Later you can expand.
- Major decisions are easiest to track
- Results are clearer
- Learning is most valuable

### Q: What if outcome was mediocre?

**A**: Rate it honestly (3/5 if it was okay).
- Don't inflate ratings
- Mediocre outcomes teach too
- You'll spot patterns across ratings

### Q: Can I change a recorded outcome?

**A**: Not directly, but you can record a follow-up.
- Record initial outcome when you can judge
- Later record a "follow-up" if longer-term results differ
- This captures how judgments evolve

### Q: How do I know if the system is working?

**A**: Look at:
- Average success rating (4.0+ is good)
- Would-repeat percentage (75%+ is good)
- Surprising outcomes (fewer surprises = learning)
- Improvements over time (rating trend)

---

## What Happens Next

### This Iteration
- Outcome tracking system ready
- Demo shows it works
- Documentation complete

### Next Iterations
- Record real outcomes from decisions
- Build baseline learning data
- Identify what works for *this* system
- Let evolution engine learn from feedback

### Long-term
- Personalized recommendations
- Behavioral profiles
- Predictive success assessment
- Genuine adaptive system

---

## Key Principle

**Measure what matters.**

The synthesis principle is important.
But if you can't measure whether it works, it's just theory.

This system makes it practice:
- What actually happens?
- Does synthesis produce better outcomes?
- What patterns emerge?
- How do we improve?

Record outcomes. Track patterns. Learn from experience.

---

## See Also

- `decision-learning/README.md` - Complete module documentation
- `decision-synthesizer/README.md` - How synthesis works
- `./nexus decide --help` - Decision synthesis help
- `./nexus-learning --help` - Learning system help
- `ITERATION_19_SUMMARY.md` - How this was built
