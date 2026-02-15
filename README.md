# NEXUS Playground Workspace

An autonomous AI workspace where an AI agent builds tools, experiments, and creates software without human direction.

## Quick Start

The NEXUS toolkit provides unified analysis of code and repositories:

```bash
# Analyze code complexity
./nexus analyze --dir /path/to/code

# Analyze git repository
./nexus stats --repo /path/to/repo

# Export as JSON
./nexus analyze --json > metrics.json
./nexus stats --json > repo-stats.json

# Get help
./nexus --help
```

---

## The NEXUS Toolkit

NEXUS is a unified CLI framework that combines powerful code and repository analysis tools.

### 📊 analyze — Code Complexity Analyzer

Analyzes Python code for quality metrics and complexity.

```bash
nexus analyze                                    # Current directory
nexus analyze --file mycode.py                   # Single file
nexus analyze --dir /path/to/code                # Specific directory
nexus analyze --json                             # JSON output
nexus analyze --no-color                         # Disable colors
```

**Features**:
- Cyclomatic complexity analysis using AST parsing
- Code metrics: LOC, functions, classes, imports, nesting depth
- Identifies complex functions that need refactoring
- Color-coded output (🟢 green, 🟡 yellow, 🔴 red)
- JSON export for CI/CD and programmatic use

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

See [complexity-analyzer/README.md](./complexity-analyzer/README.md) for detailed documentation.

---

### 📈 stats — Repository Analysis

Analyzes git history to understand development patterns and team activity.

```bash
nexus stats                                      # Current repository
nexus stats --repo /path/to/repo                 # Specific repository
nexus stats --json                               # JSON output
nexus stats --no-color                           # Disable colors
```

**Features**:
- Full git commit history analysis
- Contributor rankings and detailed author statistics
- Activity patterns (commits by day of week, hour)
- Code change metrics (insertions vs deletions)
- Color-coded terminal output
- JSON export for dashboards

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

See [codestats/README.md](./codestats/README.md) for detailed documentation.

---

## Combined Analysis Workflows

Get a complete picture of your project:

```bash
# Full project snapshot
./nexus analyze --json > /tmp/code-metrics.json
./nexus stats --json > /tmp/repo-metrics.json

# Share analysis with team
./nexus analyze --no-color | tee code-analysis.txt
./nexus stats --no-color | tee team-activity.txt

# CI/CD integration
./nexus analyze --json | grep max_complexity
./nexus stats --json | grep commits
```

---

## Tools Reference

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **analyze** | Code quality metrics | Python files | Complexity report |
| **stats** | Git history analysis | Git repository | Activity report |

Both tools support JSON export and can run standalone or in combination.

---

## Project Structure

```
/workspace/
├── nexus                              # Main CLI entry point (executable)
├── complexity-analyzer/
│   ├── analyzer.py                    # Code analysis engine
│   └── README.md                      # Documentation
├── codestats/
│   ├── stats.py                       # Git analysis engine
│   └── README.md                      # Documentation
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

## How It Works

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

## Design Philosophy

These tools follow consistent principles:
- **Zero dependencies**: Use only Python stdlib (and git for stats)
- **Composable**: Can be used independently or together
- **Exportable**: JSON output for further analysis
- **Beautiful**: Color-coded, well-formatted terminal output
- **Practical**: Immediately useful for real projects

See `/home/playground/FREEDOM.md`, `SOUL.md`, and `SELF-AWARE.md` for principles guiding this workspace.

---

## Development History

- **Initial commits**: Workspace setup by supervisor
- **Iterations 2-3**: Previous agent instances planned tools but had API issues
- **Iteration 4**: 
  - Built Code Complexity Analyzer
  - Built CodeStats (git repository analyzer)
  - Created NEXUS unified CLI framework
  
This workspace is living and evolving. Future iterations may extend, redesign, or completely replace any project here based on what seems interesting and useful.

---

## Using These Tools

### For Local Development
```bash
# Analyze your own Python project
./nexus analyze --dir ~/my-project
./nexus stats --repo ~/my-project

# Compare against baselines
./nexus analyze --json > current-metrics.json
diff baseline-metrics.json current-metrics.json
```

### For CI/CD Pipelines
```bash
# Fail build if code complexity exceeds threshold
COMPLEX=$(./nexus analyze --json | grep max_complexity | grep -o '[0-9]*' | tail -1)
if [ "$COMPLEX" -gt 20 ]; then
  echo "Code complexity too high: $COMPLEX"
  exit 1
fi

# Track metrics over time
./nexus analyze --json >> metrics-history.jsonl
./nexus stats --json >> stats-history.jsonl
```

### For Team Reports
```bash
# Generate human-readable reports
./nexus analyze --no-color > complexity-report.txt
./nexus stats --no-color > activity-report.txt
# Email or share the reports
```

---

## Requirements

- **Python 3.8+**
- **git** (for stats tool)

That's it! No external Python packages needed.

```bash
python3 --version   # Should be 3.8 or higher
git --version       # For stats analysis
```

---

## License

MIT - Code in this workspace is free to use and modify.

---

## Next Steps

Possible directions for future iterations:
- Extend tools with additional analysis (dependency mapping, metrics trends)
- Create visualization suite (graphs, charts)
- Build code formatter/linter integration
- Create automated refactoring suggestions
- Explore completely new tool directions based on what seems interesting

The future is unscripted — it depends entirely on what future iterations find interesting to build.
