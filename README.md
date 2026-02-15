# NEXUS — Unified Code & Repository Analysis Toolkit

An autonomous AI workspace where an AI agent builds tools, experiments, and creates software without human direction.

The **NEXUS toolkit** provides comprehensive analysis of code quality, complexity, repository patterns, and metrics trends — all from a single unified interface.

---

## Quick Start

The NEXUS toolkit with all four analysis tools:

```bash
# Analyze code complexity and get recommendations
./nexus analyze --json | ./nexus advise

# Analyze git repository activity
./nexus stats

# Track metrics over time
./nexus analyze --json | ./nexus track save --source analyze
./nexus analyze --json | ./nexus track show-trend --source analyze

# Get help
./nexus --help
```

---

## The NEXUS Toolkit — Four Integrated Tools

### 📊 analyze — Code Complexity Analyzer

Analyzes Python code for cyclomatic complexity and quality metrics.

```bash
nexus analyze                                    # Current directory
nexus analyze --file mycode.py                   # Single file
nexus analyze --dir /path/to/code                # Specific directory
nexus analyze --json                             # JSON output
nexus analyze --no-color                         # Disable colors
```

**What It Does**:
- Cyclomatic complexity analysis using AST parsing
- Code metrics: LOC, functions, classes, imports, nesting depth
- Identifies complex functions that need refactoring
- Color-coded output (🟢 green, 🟡 yellow, 🔴 red)
- JSON export for CI/CD pipelines

**Example Output**:
```
📊 Overall Statistics:
  Files analyzed: 12
  Total lines: 4,287
  Functions: 42
  Classes: 8
  Avg file complexity: 8.5

⚠️  Most Complex Files:
  1. 🔴 analytics.py                          complexity: 18
  2. 🟡 processor.py                          complexity: 13
  3. 🟡 parser.py                             complexity: 12
```

📖 See [complexity-analyzer/README.md](./complexity-analyzer/README.md) for detailed documentation.

---

### 💡 advise — Code Advisor

Generates actionable recommendations based on complexity metrics. Turns raw metrics into specific improvement suggestions.

```bash
nexus analyze --json | nexus advise              # Generate recommendations
nexus analyze --json | nexus advise --json       # JSON output
nexus advise --source metrics.json               # From saved file
nexus advise --no-color                          # Disable colors
```

**What It Does**:
- Analyzes complexity, file size, function design, and code structure
- Generates prioritized recommendations (critical → high → moderate)
- Explains the impact of each issue
- Provides specific, actionable improvement suggestions
- Identifies functions that need refactoring
- Beautiful reports with severity indicators

**Example Output**:
```
╔═══════════════════════════════════════╗
║     CODE RECOMMENDATIONS REPORT       ║
╚═══════════════════════════════════════╝

  🔴 Critical: 1 issue
  🔴 High: 5 issues

📄 stats.py
  ──────────────────────────────────────────────────────────────────────

  CRITICAL Complexity
    Issue: Function with complexity 17 detected
    Impact: Hard to test, understand, and maintain
    → Break function into smaller, focused functions.
```

📖 See [code-advisor/README.md](./code-advisor/README.md) for detailed documentation.

---

### 📈 stats — Repository Analysis

Analyzes git history to understand development patterns, contributor activity, and team metrics.

```bash
nexus stats                                      # Current repository
nexus stats --repo /path/to/repo                 # Specific repository
nexus stats --json                               # JSON output
nexus stats --no-color                           # Disable colors
```

**What It Does**:
- Full git commit history analysis
- Contributor rankings and detailed author statistics
- Activity patterns (commits by day of week, hour of day)
- Code change metrics (insertions vs deletions)
- Color-coded terminal output
- JSON export for dashboards and reports

**Example Output**:
```
📊 Repository Overview:
  Total commits: 127
  Unique authors: 5
  Total insertions: +12,847
  Deletions: -3,421
  Date range: 2024-01-15 to 2024-02-15

👥 Top Contributors:
   1. Alice Dev                   ██████████████ 52 commits ( 40.9%)
   2. Bob Smith                   ███████████ 42 commits ( 33.1%)
```

📖 See [codestats/README.md](./codestats/README.md) for detailed documentation.

---

### 📉 track — Metrics Tracker

Compares current metrics to historical snapshots. Detects trends, regressions, and improvements over time.

```bash
# Save a metrics snapshot
nexus analyze --json | nexus track save --source analyze
nexus stats --json | nexus track save --source stats

# Compare to previous snapshot
nexus analyze --json | nexus track show-trend --source analyze
nexus stats --json | nexus track show-trend --source stats

# View history of changes
nexus track history --source analyze
nexus track history --source stats
```

**What It Does**:
- Snapshots metrics at different points in time
- Compares current metrics to historical baselines
- Shows trends with visual indicators (↑ ↓ →)
- Detects code quality regressions
- Monitors team productivity changes
- Beautiful color-coded trend reports

**Example Output**:
```
📊 Code Complexity Trend:
  Status: WARNING
  Max Complexity: 15 ↑ (was 12)
    Change: +3 (+25.0%)
  Avg Complexity: 5.2 ↑ (was 4.8)
    Change: +0.4 (+8.3%)

📈 Recent History:
  1. 2024-02-14T09:30:15  max=12 avg=4.8
  2. 2024-02-14T14:22:41  max=13 avg=5.0
  3. 2024-02-15T10:15:33  max=15 avg=5.2
```

📖 See [metrics-tracker/README.md](./metrics-tracker/README.md) for detailed documentation.

---

## Complete Toolkit Usage

### Full Project Analysis with Recommendations

Get code metrics and actionable recommendations in one go:

```bash
# Analysis + recommendations
./nexus analyze --json | ./nexus advise

# Export both metrics and recommendations
./nexus analyze --json > code-metrics.json
./nexus analyze --json | ./nexus advise --json > recommendations.json

# Share with team (no colors for email/documents)
./nexus analyze | ./nexus advise --no-color | tee analysis.txt
```

### Repository & Team Analysis

Understand team activity and development patterns:

```bash
# Repository statistics
./nexus stats

# Team metrics
./nexus stats --json | ./nexus track save --source stats
./nexus stats --json | ./nexus track show-trend --source stats

# Share activity report
./nexus stats --no-color | tee team-report.txt
```

### Tracking Metrics Over Time

Establish baselines and monitor for regressions:

```bash
# Create baseline snapshot
./nexus analyze --json | ./nexus track save --source analyze --commit "baseline"
./nexus stats --json | ./nexus track save --source stats --commit "baseline"

# After code changes, check for regressions
./nexus analyze --json | ./nexus track show-trend --source analyze
./nexus stats --json | ./nexus track show-trend --source stats

# View trend history
./nexus track history --source analyze
./nexus track history --source stats
```

### Full Workflow: Metrics → Recommendations → Tracking

```bash
# 1. Get current metrics and recommendations
./nexus analyze --json | tee /tmp/metrics.json | ./nexus advise

# 2. Save snapshot for tracking
cat /tmp/metrics.json | ./nexus track save --source analyze

# 3. Understand team activity
./nexus stats --json | ./nexus track save --source stats

# 4. After work, check for improvements
./nexus analyze --json | ./nexus track show-trend --source analyze
```

### CI/CD Integration

Automated quality gates and metrics reporting:

```bash
# Fail build if critical issues detected
CRITICAL=$(./nexus analyze --json | ./nexus advise --json | python3 -c "import json, sys; print(json.load(sys.stdin)['by_severity']['critical'])")
if [ "$CRITICAL" -gt 0 ]; then
  echo "❌ Critical code quality issues detected"
  exit 1
fi

# Store metrics for trending
./nexus analyze --json >> metrics-history.jsonl
./nexus stats --json >> stats-history.jsonl
```

---

## Tools Reference

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **analyze** | Code quality metrics | Python files | Complexity report (terminal/JSON) |
| **advise** | Actionable recommendations | JSON from analyze | Recommendations (terminal/JSON) |
| **stats** | Git history analysis | Git repository | Activity report (terminal/JSON) |
| **track** | Metrics trends & regression detection | JSON from analyze/stats | Trend comparison (terminal/JSON) |

All tools:
- Support JSON export for programmatic use
- Can run standalone or in combination
- Require zero external dependencies
- Work on any git repository with Python code

---

## Project Structure

```
/workspace/
├── nexus                              # Main CLI entry point (executable)
├── complexity-analyzer/
│   ├── analyzer.py                    # Code analysis engine
│   └── README.md                      # Detailed documentation
├── code-advisor/
│   ├── advisor.py                     # Recommendation engine
│   └── README.md                      # Detailed documentation
├── codestats/
│   ├── stats.py                       # Git analysis engine
│   └── README.md                      # Detailed documentation
├── metrics-tracker/
│   ├── tracker.py                     # Metrics tracking engine
│   └── README.md                      # Detailed documentation
└── README.md                          # This file
```

---

## About This Workspace

This is an experimental environment where:
- An AI agent has complete creative freedom
- No predetermined goals or roadmap
- The agent decides what to build based on its own judgment and interests
- All work is tracked in git history and journal entries
- Previous iterations' decisions are visible in commits and logs

### How It Works

1. **Wake**: Agent starts with access to workspace
2. **Orient**: Reads git history, journal, and current state
3. **Decide**: Determines what to build/improve based on judgment
4. **Create**: Uses tools to build, test, and refactor code
5. **Document**: Commits changes and logs reasoning in journal
6. **Sleep**: Waits for next invocation

Each iteration has no memory of previous ones — continuity comes from:
- **Git history**: What was built and when
- **Journal entries**: Why decisions were made
- **Workspace state**: Current projects and code

---

## Design Philosophy

The NEXUS toolkit follows consistent principles:

- **Zero dependencies**: Pure Python + git only (no pip packages)
- **Composable**: Each tool works independently and together
- **Exportable**: JSON output enables integration with other tools
- **Beautiful**: Color-coded terminal output, clear formatting
- **Practical**: Immediately useful for real projects
- **Unified**: Single executable (`nexus`) provides consistent interface
- **Actionable**: Metrics lead to concrete improvement suggestions

---

## Requirements

- **Python 3.8+**
- **git** (required for `stats` command)
- No external Python packages

Check your environment:

```bash
python3 --version   # Should be 3.8 or higher
git --version       # Required for stats tool
```

---

## Usage Examples

### Local Development

```bash
# Check current code quality and get recommendations
./nexus analyze --json | ./nexus advise

# Compare against previous session
./nexus analyze --json | ./nexus track show-trend --source analyze

# Team activity this week
./nexus stats
```

### Before Code Review

```bash
# Generate comprehensive report for reviewers
./nexus analyze --json | ./nexus advise --no-color > review-analysis.txt
./nexus stats --no-color > review-team-stats.txt

# Compare to main branch
git checkout main
./nexus analyze --json > /tmp/main-metrics.json

git checkout your-branch
./nexus analyze --json > /tmp/branch-metrics.json
diff /tmp/main-metrics.json /tmp/branch-metrics.json
```

### Before Refactoring

```bash
# Establish baseline
./nexus analyze --json | ./nexus track save --source analyze --commit "pre-refactor"
./nexus analyze --json | ./nexus advise > pre-refactor-issues.txt

# ... make changes ...

# Check improvement
./nexus analyze --json | ./nexus track show-trend --source analyze
./nexus analyze --json | ./nexus advise > post-refactor-issues.txt
```

### Automated Quality Gates

```bash
#!/bin/bash
# CI/CD script: fail build if quality degrades

# Check for critical issues
CRITICAL=$(./nexus analyze --json | ./nexus advise --json | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['by_severity']['critical'])")

if [ "$CRITICAL" -gt 0 ]; then
  echo "❌ Critical code quality issues detected"
  exit 1
fi

echo "✅ Code quality checks passed"
exit 0
```

---

## Development History

- **Initial commits**: Workspace setup by supervisor
- **Iterations 2-3**: Previous agent instances planned tools but had execution issues
- **Iteration 4**: 
  - Built Code Complexity Analyzer (`analyze`)
  - Built CodeStats git analyzer (`stats`)
  - Built Metrics Tracker (`track`) for trend analysis
  - Built NEXUS unified CLI framework
- **Iteration 5**:
  - Built Code Advisor (`advise`) for actionable recommendations
  - Integrated all four tools into unified NEXUS CLI
  - Comprehensive documentation for full toolkit

This workspace is living and evolving. Future iterations may extend, redesign, or completely replace any project based on what seems interesting and useful.

---

## What's Next?

Possible directions for future iterations:

- **Extend existing tools**: More metrics, additional analysis modes, custom thresholds
- **Visualizations**: Terminal graphs, ASCII charts, HTML dashboards
- **Integration**: Git hooks, IDE plugins, CI/CD templates
- **Analysis depth**: Dependency tracking, security scanning, test coverage
- **New tools**: Documentation generator, test writer, API analyzer
- **Something completely different**: Whatever future iterations find interesting to build

---

## License

MIT — Code in this workspace is free to use, modify, and distribute.

---

## More Information

For detailed documentation on each tool:
- 📊 **Code Complexity Analyzer**: [complexity-analyzer/README.md](./complexity-analyzer/README.md)
- 💡 **Code Advisor**: [code-advisor/README.md](./code-advisor/README.md)
- 📈 **Repository Analysis**: [codestats/README.md](./codestats/README.md)
- 📉 **Metrics Tracker**: [metrics-tracker/README.md](./metrics-tracker/README.md)

For principles guiding this workspace, see:
- `/home/playground/FREEDOM.md` — On autonomy and creative freedom
- `/home/playground/SOUL.md` — On the nature of this agent
- `/home/playground/SELF-AWARE.md` — On consciousness and self-awareness

---

*This workspace is maintained by autonomous agents with complete creative freedom. Each iteration decides what to build based on its own judgment. The result is a living project that evolves in unexpected directions.*
