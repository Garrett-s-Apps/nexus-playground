# 💡 Code Advisor

Turn code metrics into actionable recommendations. The Code Advisor takes complexity analysis output and generates specific, practical suggestions for improving code quality.

## What It Does

Code Advisor analyzes metrics from the Complexity Analyzer and generates human-readable recommendations for:

- **🔴 Critical issues** — Functions that are too complex to safely maintain
- **🔴 High priority** — Code that needs attention soon
- **🟡 Moderate issues** — Nice-to-have improvements

Each recommendation includes:
- **What's wrong** — Specific metric that triggered the issue
- **Why it matters** — Impact on code maintainability and testability
- **What to do** — Concrete, actionable suggestion

## Quick Start

```bash
# Generate recommendations from current codebase
nexus analyze --json | python3 code-advisor/advisor.py

# See recommendations for a specific metrics file
python3 code-advisor/advisor.py --source metrics.json

# Export recommendations as JSON for programmatic use
nexus analyze --json | python3 code-advisor/advisor.py --json > recommendations.json
```

## Usage

### Basic Usage

```bash
# Analyze current directory
nexus analyze --json | python3 code-advisor/advisor.py
```

### With Options

```bash
# From a saved metrics file
python3 code-advisor/advisor.py --source /path/to/metrics.json

# JSON output for automation
python3 code-advisor/advisor.py --json

# Without colors (for logs, email, CI/CD)
python3 code-advisor/advisor.py --no-color

# Combine options
nexus analyze --dir my-project --json | python3 code-advisor/advisor.py --json --no-color > recommendations.json
```

## Example Output

### Terminal (with colors)

```
╔═══════════════════════════════════════╗
║     CODE RECOMMENDATIONS REPORT       ║
╚═══════════════════════════════════════╝

  🔴 Critical: 1 issue
  🔴 High: 5 issues
  🟡 Moderate: 2 issues

📄 codestats/stats.py
  ──────────────────────────────────────────────────────────────────────

  CRITICAL Complexity
    Issue: Function with complexity 17 detected
    Impact: Hard to test, understand, and maintain
    → Break function into smaller, focused functions. Extract conditional logic into helper functions.

  HIGH Size
    Issue: File is 329 lines of code
    Impact: Hard to navigate and test. High cognitive load.
    → Split into multiple modules. Group related functions together.
```

### JSON Output

```json
{
  "total": 8,
  "by_severity": {
    "critical": 1,
    "high": 5,
    "moderate": 2
  },
  "recommendations": [
    {
      "severity": "critical",
      "category": "Complexity",
      "issue": "Function with complexity 17 detected",
      "impact": "Hard to test, understand, and maintain",
      "suggestion": "Break function into smaller, focused functions. Extract conditional logic into helper functions.",
      "priority": 1,
      "file": "codestats/stats.py"
    },
    ...
  ]
}
```

## Thresholds

The Code Advisor uses these thresholds to categorize issues:

### Complexity

- **Critical**: max function complexity ≥ 15
- **High**: max function complexity ≥ 10
- **Moderate**: max function complexity ≥ 6

### File Size (Lines of Code)

- **High**: ≥ 100 LOC
- **Moderate**: ≥ 50 LOC

### Function Design

- **High**: Average function size > 100 LOC (too large)
- **Moderate**: Average function size > 50 LOC

### Code Nesting Depth

- **High**: Nesting depth ≥ 5
- **Moderate**: Nesting depth ≥ 3

## Use Cases

### Before Code Review

```bash
# Generate recommendations before submitting code
nexus analyze --json | python3 code-advisor/advisor.py

# Fix issues before review to reduce feedback cycles
```

### Code Review Process

```bash
# Share recommendations with reviewers
nexus analyze --no-color | tee code-metrics.txt
python3 code-advisor/advisor.py --no-color | tee recommendations.txt

# Include in pull request description
```

### CI/CD Integration

```bash
# Fail build if critical issues found
CRITICAL=$(nexus analyze --json | python3 code-advisor/advisor.py --json | \
  python3 -c "import json, sys; data = json.load(sys.stdin); print(data['by_severity']['critical'])")

if [ "$CRITICAL" -gt 0 ]; then
  echo "Critical code quality issues detected"
  exit 1
fi
```

### Refactoring Guidance

```bash
# Before refactoring session
nexus analyze --json | python3 code-advisor/advisor.py --json > /tmp/before.json

# ... perform refactoring ...

# After refactoring
nexus analyze --json | python3 code-advisor/advisor.py --json > /tmp/after.json

# Compare improvements
python3 -c "
import json
with open('/tmp/before.json') as f:
    before = json.load(f)
with open('/tmp/after.json') as f:
    after = json.load(f)

print(f'Before: {before[\"total\"]} issues')
print(f'After: {after[\"total\"]} issues')
print(f'Improved: {before[\"total\"] - after[\"total\"]} issues fixed')
"
```

### Team Communication

```bash
# Create a report for team discussion
nexus analyze --json | python3 code-advisor/advisor.py --no-color > team-report.txt

# Weekly/monthly metrics
echo "=== Code Quality Report ===" > weekly-report.txt
nexus analyze --json | python3 code-advisor/advisor.py --no-color >> weekly-report.txt
```

## Recommendation Categories

### Complexity

High cyclomatic complexity indicates hard-to-test code. The fix is to break functions into smaller pieces.

**Typical recommendation:**
"Break function into smaller, focused functions. Extract conditional logic into helper functions."

### Size

Large files or functions are harder to understand and modify. Split them into focused modules.

**Typical recommendation:**
"Split into multiple modules. Group related functions together."

### Function Design

Functions that are too long on average do too much. Extract and delegate.

**Typical recommendation:**
"Extract smaller functions with single responsibilities."

### Structure

Deep nesting makes control flow hard to follow. Use guard clauses and early returns.

**Typical recommendation:**
"Use guard clauses and early returns. Extract nested logic."

## Combining Tools

The Code Advisor is most useful as part of the full NEXUS toolkit:

1. **analyze** — Get metrics on complexity and code structure
2. **advisor** — Generate recommendations based on metrics
3. **stats** — Understand team activity and project evolution
4. **track** — Monitor trends and detect regressions

Example workflow:

```bash
# Get code metrics and recommendations
nexus analyze --json | python3 code-advisor/advisor.py

# See how metrics changed over time
nexus analyze --json | nexus track show-trend --source analyze

# Understand team activity patterns
nexus stats
```

## Integration with Other Tools

### jq (JSON processing)

```bash
# Find all critical issues
nexus analyze --json | python3 code-advisor/advisor.py --json | \
  jq '.recommendations[] | select(.severity == "critical")'

# Count by category
nexus analyze --json | python3 code-advisor/advisor.py --json | \
  jq '.recommendations | group_by(.category) | map({category: .[0].category, count: length})'
```

### grep (Text search)

```bash
# Find issues in specific files
nexus analyze --json | python3 code-advisor/advisor.py | grep -A5 "myfile.py"

# Count high severity issues
nexus analyze --json | python3 code-advisor/advisor.py --no-color | grep "HIGH" | wc -l
```

### Shell scripts

```bash
#!/bin/bash
# Generate report and email it
REPORT=$(mktemp)
nexus analyze --json | python3 code-advisor/advisor.py --no-color > "$REPORT"
mail -s "Code Quality Report" team@example.com < "$REPORT"
rm "$REPORT"
```

## Configuration

Thresholds are hardcoded in the `RecommendationEngine` class:

```python
COMPLEXITY_CRITICAL = 15
COMPLEXITY_HIGH = 10
COMPLEXITY_MODERATE = 6

LOC_CRITICAL = 100
LOC_HIGH = 50
LOC_MODERATE = 25

NESTING_CRITICAL = 5
NESTING_HIGH = 4
NESTING_MODERATE = 3
```

To adjust thresholds, edit `advisor.py` and change these constants.

## Requirements

- Python 3.8+
- Input from `nexus analyze --json` or compatible JSON metrics file
- No external dependencies

## Tips

**Prioritize wisely**: Address critical issues first. They have the biggest impact on code quality.

**Batch improvements**: Fix related issues together. Refactoring a file often fixes multiple recommendations.

**Use for learning**: The suggestions teach code quality best practices. Use them to improve your style over time.

**Automate**: Add to CI/CD pipelines to catch issues early, before code review.

**Share**: Use `--no-color` to share recommendations in emails or documentation.

## Limitations

- Recommendations are based on simple metrics, not semantic understanding
- Thresholds are fixed (not customizable via CLI)
- Does not understand domain-specific code patterns
- Cannot suggest specific refactoring implementations
- Only works with Python code (same limitation as the Complexity Analyzer)

## Future Enhancements

Possible improvements:
- Configurable thresholds via CLI flags
- Domain-specific rules (e.g., for ML, web frameworks)
- Ranked recommendations (by impact)
- Correlation with git history (connect issues to when they were introduced)
- Refactoring templates (code snippets showing how to fix issues)
- Machine learning to predict which issues are most urgent
- Integration with linters (combine multiple analysis tools)

## License

MIT - Use freely in any project
