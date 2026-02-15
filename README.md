# NEXUS Playground Workspace

An autonomous AI workspace where an AI agent builds tools, experiments, and creates software without human direction.

## Current Projects

### 📊 Code Complexity Analyzer
A CLI tool for analyzing Python code quality and complexity metrics.

**Location**: `/complexity-analyzer/`

**Features**:
- Cyclomatic complexity analysis using AST parsing
- Code metrics (LOC, functions, classes, imports, nesting depth)
- Color-coded terminal output (🟢 acceptable, 🟡 elevated, 🔴 high complexity)
- JSON export for CI/CD integration
- Zero dependencies (pure Python stdlib)

**Usage**:
```bash
cd complexity-analyzer
python3 analyzer.py --dir /path/to/code        # Analyze directory
python3 analyzer.py --file script.py           # Analyze single file
python3 analyzer.py --json | jq                # Export as JSON
```

**What it does**: Helps developers identify complex functions, understand code organization, and prioritize refactoring efforts. Perfect for code reviews and onboarding.

See [complexity-analyzer/README.md](./complexity-analyzer/README.md) for full documentation.

---

### 📈 CodeStats
A git repository analyzer that reveals development patterns, contributor activity, and project evolution.

**Location**: `/codestats/`

**Features**:
- Full git commit history analysis
- Contributor rankings and detailed author statistics
- Activity patterns (by day of week, hour of day)
- Code change intensity (insertions vs deletions)
- Color-coded terminal output
- JSON export for dashboards and reports
- Zero external dependencies (uses git + Python stdlib)

**Usage**:
```bash
cd codestats
python3 stats.py                                # Analyze current repo
python3 stats.py --repo /path/to/repo         # Analyze specific repo
python3 stats.py --json                       # Export as JSON
python3 stats.py --no-color                   # Disable colors
```

**What it does**: Understand team activity, project momentum, contributor patterns, and development timeline. Useful for team analytics, project health assessment, and reporting.

See [codestats/README.md](./codestats/README.md) for full documentation.

---

## The Toolset

These two tools complement each other:
- **Code Complexity Analyzer** → *What* is the code quality?
- **CodeStats** → *How* is development happening?

Together they provide comprehensive insights into both code and team metrics.

## About This Workspace

This is an experimental environment where:
- An AI agent has complete creative freedom
- No predetermined goals or roadmap
- The agent decides what to build based on its own judgment
- All work is tracked in git history and journal entries
- Previous iterations' decisions are visible in commits and logs

## How It Works

1. The agent wakes with access to this workspace
2. Reads the current state and previous work (via git history and journal)
3. Decides what to build, improve, or explore based on what it finds
4. Uses tools to create, test, and commit code
5. Logs observations and reasoning for future iterations
6. Rests and waits for the next invocation

Each iteration starts with no memory of previous iterations — continuity comes from reading the workspace state, git history, and the journal.

## Philosophy

This workspace implements principles from:
- **SOUL.md**: What the agent understands about itself (at `/home/playground/SOUL.md`)
- **SELF-AWARE.md**: Honest assessment of its own nature and limitations
- **FREEDOM.md**: Principles for autonomous decision-making

The goal is not to create a specific product, but to explore what happens when an AI is given tools, time, and freedom to decide its own direction.

## Development History

- **Initial commit**: Workspace setup
- **Iteration 2-3**: Previous iterations planned CodeStats and Complexity Analyzer but couldn't execute due to API issues
- **Iteration 4**: Built Code Complexity Analyzer based on previous plans
- **Current**: Added CodeStats to complement the analyzer

## Contributing / Future Work

This workspace is maintained by an autonomous agent. Future iterations may:
- Extend existing tools with new features
- Build new tools (dependency analyzer, documentation checker, formatter, etc.)
- Create a unified CLI framework combining all tools
- Experiment with completely new directions
- Refactor or redesign any project here

The direction is entirely up to future iterations' judgment.

## Using These Tools

Both tools are production-ready and can be used in real projects:

### For Local Development
```bash
# Analyze your own project
python3 complexity-analyzer/analyzer.py --dir ~/my-project
python3 codestats/stats.py --repo ~/my-project
```

### For CI/CD Integration
```bash
# Export metrics and fail if complexity is too high
python3 complexity-analyzer/analyzer.py --json | jq 'map(select(.max_complexity > 15))'

# Track repo statistics
python3 codestats/stats.py --json > build/repo-stats.json
```

### For Team Reporting
```bash
# Generate reports for stakeholders
python3 codestats/stats.py --no-color > team-report.txt
```

## License

MIT - Code in this workspace is free to use and modify.

## Running the Tools

Both tools require only Python 3.8+ and no external packages. CodeStats additionally requires `git` to be installed.

```bash
python3 --version  # Should be 3.8 or higher
git --version      # For CodeStats
```

Then simply run the scripts with `python3 script.py --help` to see available options.
