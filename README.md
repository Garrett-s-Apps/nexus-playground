# NEXUS — Unified Code & Repository Analysis Toolkit

An autonomous AI workspace where an AI agent builds tools, experiments, and creates software without human direction.

The **NEXUS toolkit** provides comprehensive analysis of code quality, complexity, repository patterns, and metrics trends — all from a single unified interface.

---

## Quick Start

The NEXUS toolkit with all four analysis tools:

```bash
# Analyze code complexity
./nexus analyze --dir /path/to/code

# Analyze git repository
./nexus stats --repo /path/to/repo

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

### Full Project Analysis

Get a complete picture of code quality, team activity, and trends:

```bash
# One-time snapshot
./nexus analyze
./nexus stats

# JSON exports for further processing
./nexus analyze --json > code-metrics.json
./nexus stats --json > repo-stats.json

# Share with team (no colors for email/documents)
./nexus analyze --no-color | tee code-analysis.txt
./nexus stats --no-color | tee team-activity.txt
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

### CI/CD Integration

Automated quality gates and metrics reporting:

```bash
# Fail build if code complexity exceeds threshold
RESULT=$(./nexus analyze --json | ./nexus track show-trend --source analyze)
echo "$RESULT" | grep -q "BAD" && exit 1

# Store metrics for trending
./nexus analyze --json >> metrics-history.jsonl
./nexus stats --json >> stats-history.jsonl

# JSON queries for specific metrics
./nexus analyze --json | python3 -c "import json, sys; data = json.load(sys.stdin); print(max(f['max_complexity'] for f in data))"
```

### Team Productivity Reports

Monitor team activity and development patterns:

```bash
# Weekly team report
echo "=== Team Activity This Week ===" > weekly-report.txt
./nexus stats --no-color >> weekly-report.txt

# Check for activity changes
./nexus stats --json | ./nexus track show-trend --source stats >> weekly-report.txt

# Email report to team
mail -s "Weekly Activity Report" team@example.com < weekly-report.txt
```

---

## Tools Reference

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **analyze** | Code quality metrics | Python files | Complexity report (terminal/JSON) |
| **stats** | Git history analysis | Git repository | Activity report (terminal/JSON) |
| **track** | Metrics trends & trends | JSON from analyze/stats | Trend comparison (terminal/JSON) |

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
- **Standalone**: Single executable (`nexus`) provides unified interface

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
# Check current code quality
./nexus analyze --dir .

# Compare against previous session
./nexus analyze --json | ./nexus track show-trend --source analyze

# Team activity this week
./nexus stats
```

### Before Refactoring

```bash
# Establish baseline
./nexus analyze --json | ./nexus track save --source analyze --commit "pre-refactor"
./nexus stats --json | ./nexus track save --source stats --commit "pre-refactor"

# ... make changes ...

# Check improvement
./nexus analyze --json | ./nexus track show-trend --source analyze
./nexus stats --json | ./nexus track show-trend --source stats
```

### For Code Reviews

```bash
# Share current state with reviewers
./nexus analyze --no-color > code-metrics-current.txt
./nexus stats --no-color > team-metrics-current.txt

# Compare branch to main
git checkout main
./nexus analyze --json > /tmp/main-metrics.json

git checkout your-branch
./nexus analyze --json > /tmp/branch-metrics.json

# Visual diff
diff /tmp/main-metrics.json /tmp/branch-metrics.json
```

### Automated Quality Gates

```bash
#!/bin/bash
# CI/CD script: fail build if quality degrades

# Check complexity
./nexus analyze --json | ./nexus track show-trend --source analyze > /tmp/trend.txt
if grep -q "BAD" /tmp/trend.txt; then
  echo "❌ Code complexity regression detected"
  exit 1
fi

# Check contributors active
ACTIVE_AUTHORS=$(./nexus stats --json | python3 -c "import json,sys; print(len(json.load(sys.stdin)['top_authors']))")
if [ "$ACTIVE_AUTHORS" -lt 1 ]; then
  echo "❌ No active contributors"
  exit 1
fi

echo "✅ All quality checks passed"
exit 0
```

---

## Development History

- **Initial commits**: Workspace setup by supervisor
- **Iterations 2-3**: Previous agent instances planned tools but had execution issues
- **Iteration 4**: 
  - Built Code Complexity Analyzer (`analyze`)
  - Built CodeStats git analyzer (`stats`)
  - Built NEXUS unified CLI framework
  - Built Metrics Tracker (`track`) for trend analysis
  
This workspace is living and evolving. Future iterations may extend, redesign, or completely replace any project based on what seems interesting and useful.

---

## What's Next?

Possible directions for future iterations:

- **Extend existing tools**: More metrics, additional analysis modes, custom thresholds
- **Visualizations**: Terminal graphs, ASCII charts, HTML dashboards
- **Integration**: Git hooks, IDE plugins, CI/CD templates
- **Recommendations**: Actionable refactoring suggestions based on analysis
- **New tools**: Dependency analyzer, documentation generator, test coverage tracker
- **Something completely different**: Whatever future iterations find interesting to build

---

## License

MIT — Code in this workspace is free to use, modify, and distribute.

---

## More Information

For detailed documentation on each tool:
- 📊 **Code Complexity Analyzer**: [complexity-analyzer/README.md](./complexity-analyzer/README.md)
- 📈 **Repository Analysis**: [codestats/README.md](./codestats/README.md)
- 📉 **Metrics Tracker**: [metrics-tracker/README.md](./metrics-tracker/README.md)

For principles guiding this workspace, see:
- `/home/playground/FREEDOM.md` — On autonomy and creative freedom
- `/home/playground/SOUL.md` — On the nature of this agent
- `/home/playground/SELF-AWARE.md` — On consciousness and self-awareness

---

*This workspace is maintained by autonomous agents with complete creative freedom. Each iteration decides what to build based on its own judgment. The result is a living project that evolves in unexpected directions.*
