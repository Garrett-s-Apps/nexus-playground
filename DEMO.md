# NEXUS v1.2.0 Demo

Complete demonstration of the NEXUS unified code analysis toolkit.

## The Toolkit

NEXUS provides a complete workflow for understanding, analyzing, and improving code:

1. **ANALYZE** - Get metrics on code complexity and structure
2. **ADVISE** - Get actionable recommendations based on metrics
3. **REFACTOR** - Find specific refactoring opportunities
4. **STATS** - Understand team activity and development patterns
5. **TRACK** - Monitor metrics over time to spot trends

## Quick Example: Analyzing a File

```bash
# Analyze a single Python file
./nexus analyze --file mycode.py

# Get JSON output for programmatic access
./nexus analyze --file mycode.py --json
```

## Complete Workflow: End-to-End Analysis

Here's how to use NEXUS to analyze, understand, and improve your codebase.

### Step 1: Get Complexity Metrics

```bash
$ ./nexus analyze --dir src/

╔══════════════════════════════════════════════════════════════════════════════╗
║ CODE COMPLEXITY ANALYSIS REPORT                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 Overall Statistics:
  Files analyzed: 25
  Total lines: 8,432
  Functions: 156
  Classes: 42
  Avg file complexity: 8.2

⚠️  Most Complex Files:
  1. 🔴 database.py                              complexity: 18
  2. 🟡 api_handler.py                           complexity: 14
  3. 🟡 models.py                                complexity: 12
  [... more files ...]
```

This shows which files are most complex and need attention.

### Step 2: Get Recommendations

```bash
$ ./nexus analyze --json | ./nexus advise

╔═══════════════════════════════════════╗
║     CODE RECOMMENDATIONS REPORT       ║
╚═══════════════════════════════════════╝

  🔴 Critical: 1 issue
  🔴 High: 5 issues
  🟡 Moderate: 8 issues

📄 database.py
  ──────────────────────────────────────────────────────────────────────
  
  CRITICAL Database connection setup
    Issue: Function with complexity 18 detected
    Impact: Hard to test, understand, and maintain
    → Break function into smaller, focused functions
  
  HIGH File size (234 lines)
    Issue: File is 234 lines of code
    Impact: Hard to navigate and test. High cognitive load.
    → Split into multiple modules. Group related functions together.

[... more recommendations ...]
```

Now you understand WHAT needs to improve and WHY it matters.

### Step 3: Find Specific Refactoring Opportunities

```bash
$ ./nexus refactor --dir src/

╔════════════════════════════════════════╗
║    REFACTORING OPPORTUNITIES REPORT     ║
╚════════════════════════════════════════╝

  🔴 High Priority: 2
  🟡 Medium Priority: 8
  🔵 Low Priority: 15

📄 database.py
────────────────────────────────────────────────────────────────────────────────
  🔪 HIGH | Line 45
     Function 'connect_and_initialize' has complexity 18
     → High complexity (18) makes function hard to test and maintain. 
        Consider extracting conditional branches into helper functions.

  ⬇️ HIGH | Line 45
     Function 'connect_and_initialize' has nesting depth 6
     → Deep nesting (6) makes control flow hard to follow. 
        Use early returns and extract nested blocks into functions.

  🔪 MEDIUM | Line 142
     Function 'execute_query' is 67 lines
     → Function is 67 lines long. Extract logical sections into helper functions.

📄 api_handler.py
────────────────────────────────────────────────────────────────────────────────
  🔪 MEDIUM | Line 88
     Function 'handle_request' is 54 lines
     → Function is 54 lines long. Extract logical sections into helper functions.

[... more refactoring opportunities ...]
```

Now you know WHICH functions to refactor and HOW to improve them.

### Step 4: Understand Team Activity

```bash
$ ./nexus stats

╔══════════════════════════════════════════════════════════════════════════════╗
║ GIT REPOSITORY STATISTICS                                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 Repository Overview:
  Total commits: 342
  Unique authors: 8
  Total insertions: +45,232
  Deletions: -8,451
  Date range: 2026-01-15 09:23:11 to 2026-02-15 14:22:43

👥 Top Contributors:
   1. Alice Chen                    ██████████████████████████████   168 commits ( 49.1%)
   2. Bob Smith                     ████████████░░░░░░░░░░░░░░░░░░   102 commits ( 29.8%)
   3. Carol White                   ████████░░░░░░░░░░░░░░░░░░░░░░    52 commits ( 15.2%)
   4. David Lee                     ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░    14 commits (  4.1%)
   5. Eve Johnson                   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     6 commits (  1.8%)

📅 Activity by Day of Week:
  Monday       ██████████████████████████████   78 commits
  Tuesday      ████████████████████████░░░░░░░  71 commits
  Wednesday    ██████████████████████░░░░░░░░░  65 commits
  [... more days ...]

📈 Code Change Intensity:
  Additions:  █████████████████████████████ 84.3%
  Deletions:  ████████ 15.7%
```

Now you understand WHO is working on WHAT and development patterns.

### Step 5: Save Baseline and Track Improvements

```bash
# Save current metrics as a baseline
$ ./nexus analyze --json | ./nexus track save --source analyze
Snapshot saved to .metrics/2026-02-15T14-30-00-analyze.json

# Make some refactoring changes...
# Then check for improvement
$ ./nexus analyze --json | ./nexus track show-trend --source analyze

📊 Code Complexity Trend:
  Status: GOOD (improving!)
  Max Complexity: 18 → 14 ✓ (decreased by 4)
  Avg Complexity: 8.2 → 7.1 ✓ (decreased by 1.1)

📈 Recent History:
  1. 2026-02-14T10-15-00  max=22 avg=9.2
  2. 2026-02-15T08-45-00  max=19 avg=8.7
  3. 2026-02-15T14-30-00  max=14 avg=7.1
  
💡 Trend: Code complexity is trending down. Great work!
```

Now you can VERIFY improvements over time.

## Piping Examples

NEXUS tools compose beautifully with pipes:

```bash
# Analyze and get recommendations in one command
./nexus analyze --json | ./nexus advise

# Export metrics for visualization
./nexus analyze --json > metrics.json
cat metrics.json | jq '.[] | {file: .filepath, complexity: .max_complexity}'

# Find high-priority refactoring opportunities
./nexus refactor --dir src/ --json | jq '.[] | select(.severity == "high")'

# Check for complexity regressions in CI/CD
./nexus analyze --json | ./nexus track show-trend --source analyze | grep -q "WARNING" && exit 1

# Compare specific files
./nexus analyze --file src/important.py --json | jq '.max_complexity'
```

## Real-World Scenarios

### Before Code Review
```bash
# Get everything you need to know about the code
./nexus analyze
./nexus analyze --json | ./nexus advise
./nexus refactor --dir src/
./nexus stats
```

### Onboarding New Developers
```bash
# Show them the codebase metrics
./nexus analyze --dir src/

# Explain which parts are complex
./nexus analyze --json | ./nexus advise

# Point them to refactoring opportunities
./nexus refactor --dir src/ | grep "HIGH"
```

### Refactoring Sprint Planning
```bash
# Find all high-priority refactoring opportunities
./nexus refactor --dir src/ --json > refactoring_plan.json

# Count by severity
jq '.[] | .severity' refactoring_plan.json | sort | uniq -c

# Group by file
jq -r '.[] | .filepath' refactoring_plan.json | sort | uniq -c | sort -rn
```

### CI/CD Integration
```bash
#!/bin/bash
# Fail if complexity exceeds threshold
./nexus analyze --json | jq -e '.[] | select(.max_complexity > 20)' && {
  echo "ERROR: Code complexity exceeds threshold"
  exit 1
}

# Store metrics for dashboard
./nexus analyze --json > /var/metrics/latest.json
./nexus stats --json >> /var/metrics/stats.json
```

### Trend Monitoring
```bash
# Weekly metrics check
TIMESTAMP=$(date +%Y-%m-%d)
./nexus analyze --json | ./nexus track save --source analyze
./nexus analyze --json | ./nexus track show-trend --source analyze > reports/$TIMESTAMP-trend.txt

# Monthly comparison
./nexus track history --source analyze | jq '.[0, -1]'
```

## JSON Output Examples

### Analyze Output
```json
[
  {
    "filepath": "src/main.py",
    "total_lines": 1024,
    "code_lines": 856,
    "comment_lines": 42,
    "blank_lines": 126,
    "num_functions": 24,
    "num_classes": 3,
    "num_imports": 12,
    "avg_complexity": 6.5,
    "max_complexity": 14
  }
]
```

### Refactor Output
```json
[
  {
    "filepath": "src/main.py",
    "lineno": 145,
    "rule": "extract_function",
    "description": "Function 'process_data' has complexity 14",
    "severity": "high",
    "why": "High complexity (14) makes function hard to test and maintain..."
  }
]
```

## Color Legend

### Complexity Heat Map
- 🟢 **Green**: Low complexity (0-5)
- 🟡 **Yellow**: Moderate complexity (6-10)
- 🔴 **Red**: High complexity (11+)

### Severity Indicators
- 🔴 **Critical**: Highest priority, causes major issues
- 🔴 **High**: Important, causes real problems
- 🟡 **Moderate**: Should address soon
- 🔵 **Low**: Nice to fix when you have time

### Refactoring Rules
- 🔪 **Extract Function**: Function is too complex or too long
- ⬇️ **Reduce Nesting**: Code has excessive nesting depth
- ↩️ **Early Returns**: Use early returns to flatten control flow
- 📦 **Extract Constant**: Consolidate repeated code patterns
- 📝 **Improve Naming**: Function/variable names are unclear

## Tips & Tricks

### Find the Worst Offenders
```bash
./nexus analyze --json | jq '.[] | select(.max_complexity > 15)' | jq '.filepath'
```

### Track Improvement Over Time
```bash
./nexus analyze --json | ./nexus track save --source analyze
# ... make changes ...
./nexus analyze --json | ./nexus track show-trend --source analyze
```

### Generate a Refactoring Checklist
```bash
./nexus refactor --dir src/ --json | jq -r '.[] | "\(.severity|ascii_upcase): \(.description)"' > REFACTORING_TODO.txt
```

### Monitor for Regressions
```bash
./nexus analyze --json | ./nexus track show-trend --source analyze | grep -i "worse\|regression"
```

### Export for Analysis
```bash
./nexus analyze --dir src/ --json | python3 my_analysis_script.py
./nexus stats --json | jq '.top_authors[]' | grep -i "alice"
```

## Common Questions

### Q: How often should I run analysis?
A: Before code reviews, before major releases, and as part of CI/CD. Weekly trend snapshots help spot patterns.

### Q: Should I aim for zero complexity?
A: No, some complexity is necessary. Aim for most functions ≤ 10, files ≤ 100 lines, nesting ≤ 3.

### Q: Can I ignore low-priority issues?
A: Yes, but consider addressing them during refactoring sprints. Low priority means low immediate impact.

### Q: How do I know if I'm improving?
A: Use `./nexus track` to save metrics over time and compare. Look for trends, not just single snapshots.

### Q: Can I automate refactoring?
A: Not yet—NEXUS identifies opportunities but doesn't auto-apply. Future versions may support this.

## Next Steps

1. **Try it**: Run the toolkit on your codebase
2. **Understand**: Review the recommendations and refactoring opportunities
3. **Improve**: Apply the suggested refactorings
4. **Track**: Save baseline metrics and monitor progress
5. **Iterate**: Make analysis part of your regular workflow

## Documentation

- `README.md` - Complete toolkit overview
- `complexity-analyzer/README.md` - Code analysis
- `code-advisor/README.md` - Actionable recommendations
- `code-refactor/README.md` - Refactoring opportunities
- `codestats/README.md` - Repository analysis
- `metrics-tracker/README.md` - Trend tracking

## Support

Each tool has its own README with detailed documentation, examples, and troubleshooting tips.

---

**NEXUS v1.2.0** - Making code better, one analysis at a time.
