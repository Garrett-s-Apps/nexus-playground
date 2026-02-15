# NEXUS v1.2.0 - Unified Code Analysis Toolkit

A comprehensive suite of Python tools for understanding, analyzing, and improving code quality. NEXUS provides metrics, recommendations, refactoring opportunities, repository insights, and trend tracking—all in one unified toolkit.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           NEXUS v1.2.0                                       ║
║           Unified Code and Repository Analysis Toolkit                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Features

### 📊 Code Complexity Analysis
Analyzes Python code for cyclomatic complexity, code metrics, and quality indicators.
- Detect complex functions
- Understand code organization
- Identify refactoring candidates
- JSON export for CI/CD

### 💡 Code Recommendations  
Generates actionable, severity-ranked recommendations based on metrics.
- Turn raw metrics into practical suggestions
- Prioritize refactoring by impact
- Understand why each issue matters
- Human-readable and JSON formats

### 🔧 Refactoring Opportunities
Identifies specific refactoring opportunities with detailed analysis.
- Detect overly complex functions
- Find deeply nested code
- Spot code duplication
- Improve function naming
- Clear priority and guidance for each opportunity

### 📈 Repository Analytics
Analyze git history for development patterns and team metrics.
- Contributor activity analysis
- Commit frequency trends
- Author statistics
- Code change patterns
- Team velocity insights

### 📉 Metrics Tracking
Track code quality metrics over time to spot trends and regressions.
- Compare current vs. historical metrics
- Detect improvements and regressions
- Monitor project health
- Enable data-driven decisions

## Installation

No external dependencies required! Uses only Python's standard library.

```bash
# Clone or download the workspace
cd /workspace

# Make NEXUS executable
chmod +x ./nexus

# Run it
./nexus --help
```

## Quick Start

### Basic Workflow

```bash
# 1. Analyze code complexity
./nexus analyze

# 2. Get recommendations for improvement
./nexus analyze --json | ./nexus advise

# 3. Find refactoring opportunities
./nexus refactor --dir src/

# 4. Understand repository activity
./nexus stats

# 5. Track metrics over time
./nexus analyze --json | ./nexus track save --source analyze
./nexus analyze --json | ./nexus track show-trend --source analyze
```

### Common Commands

```bash
# Analyze a single file
./nexus analyze --file mymodule.py

# Analyze a directory
./nexus analyze --dir src/

# Get JSON output (for automation)
./nexus analyze --json

# Generate recommendations
./nexus analyze --json | ./nexus advise

# Find refactoring opportunities in specific file
./nexus refactor --file mymodule.py

# Find all refactoring opportunities
./nexus refactor --dir src/

# Get repository statistics
./nexus stats --json

# Check for regressions
./nexus analyze --json | ./nexus track show-trend --source analyze
```

## Tools Overview

### 🔍 ANALYZE - Code Complexity Analyzer

Analyzes Python code to compute metrics on complexity, size, structure, and organization.

**What it measures:**
- **Cyclomatic Complexity** - How many independent paths through the code (lower is better)
- **Lines of Code** - Total, blank, comment, and code lines
- **Functions & Classes** - Count and distribution
- **Imports** - What the file depends on
- **Nesting Depth** - How deeply nested the code is

**Example:**
```bash
./nexus analyze --dir src/

# Output shows:
# - Files analyzed and overall stats
# - Complexity heat map (green/yellow/red)
# - Top 5 most complex files
# - Detailed metrics per file
```

**See:** `complexity-analyzer/README.md`

### 💡 ADVISE - Code Advisor

Turns complexity metrics into actionable recommendations with clear prioritization.

**What it does:**
- Analyzes metrics from the Analyzer
- Generates severity-ranked recommendations
- Explains the impact of each issue
- Suggests specific improvements
- Works with single files or entire projects

**Example:**
```bash
./nexus analyze --json | ./nexus advise

# Output shows:
# - Summary of issues by severity
# - Per-file recommendations
# - Why each issue matters
# - Specific suggestions for improvement
```

**See:** `code-advisor/README.md`

### 🔧 REFACTOR - Code Refactoring Engine

Identifies specific refactoring opportunities with detailed analysis of what to refactor and why.

**What it detects:**
- Complex functions (cyclomatic complexity ≥ 10)
- Oversized functions (≥ 50 lines)
- Deep nesting (nesting depth ≥ 4)
- Code duplication patterns
- Unclear naming

**Example:**
```bash
./nexus refactor --dir src/

# Output shows:
# - Priority breakdown (high/medium/low)
# - Per-file refactoring opportunities
# - Specific line numbers
# - Clear explanation of why it matters
# - Guidance on how to fix it
```

**See:** `code-refactor/README.md`

### 📊 STATS - Repository Analytics

Analyzes git history to understand development patterns and team activity.

**What it shows:**
- Total commits and authors
- Top contributors by commits, insertions, deletions
- Commits per day of week
- Activity per hour of day
- File change frequency

**Example:**
```bash
./nexus stats

# Output shows:
# - Project statistics
# - Top 10 contributors
# - Activity patterns by day/hour
# - File change frequency
```

**See:** `codestats/README.md`

### 📉 TRACK - Metrics Tracker

Compares current metrics against historical snapshots to detect trends and regressions.

**What it does:**
- Saves snapshots of metrics over time
- Compares current metrics to previous
- Detects improvements and regressions
- Shows historical trends
- Enables regression detection

**Example:**
```bash
# Save a snapshot
./nexus analyze --json | ./nexus track save --source analyze

# Check for regressions
./nexus analyze --json | ./nexus track show-trend --source analyze

# View history
./nexus track history --source analyze
```

**See:** `metrics-tracker/README.md`

## Complete Workflow

Here's a complete workflow showing how all tools work together:

### 1. Initial Analysis
```bash
$ ./nexus analyze --dir src/

# Get overall code quality snapshot
# Shows complexity, size, organization metrics
```

### 2. Get Recommendations
```bash
$ ./nexus analyze --json | ./nexus advise

# Understand what needs improvement
# Prioritized by severity and impact
```

### 3. Find Refactoring Opportunities
```bash
$ ./nexus refactor --dir src/

# Get specific guidance on what to refactor
# See which functions are best candidates
```

### 4. Understand Team Activity
```bash
$ ./nexus stats

# See who's working on what
# Understand development patterns
```

### 5. Save Baseline and Track Improvements
```bash
# Save current metrics as baseline
$ ./nexus analyze --json | ./nexus track save --source analyze

# After making changes, check improvement
$ ./nexus analyze --json | ./nexus track show-trend --source analyze

# Review historical progress
$ ./nexus track history --source analyze
```

## Integration Examples

### For Code Reviews
```bash
# Pre-review: Check code quality
./nexus analyze --dir review_branch/
./nexus advise --source metrics.json
./nexus refactor --dir review_branch/
```

### For CI/CD Pipelines
```bash
# Fail if complexity exceeds threshold
./nexus analyze --json | jq '.[] | select(.max_complexity > 15)' | grep . && exit 1

# Export metrics for dashboard
./nexus analyze --json > /tmp/metrics.json
./nexus stats --json > /tmp/stats.json
```

### For Trend Analysis
```bash
# Weekly check
./nexus analyze --json | ./nexus track save --source analyze

# See if quality is improving
./nexus analyze --json | ./nexus track show-trend --source analyze
```

### For Refactoring Sessions
```bash
# Find top priorities
./nexus refactor --dir src/ | grep "HIGH\|MEDIUM" > /tmp/refactoring_plan.txt

# Focus on specific file
./nexus refactor --file biggest_issue.py
```

## Output Formats

### Human-Readable (Default)
Beautiful, colored terminal output designed for interactive use:
```
📊 ANALYZE: Complexity heat map with color-coded files
💡 ADVISE: Prioritized recommendations with severity indicators  
🔧 REFACTOR: Detailed opportunities with specific guidance
📈 STATS: Team activity summary and trends
📉 TRACK: Before/after comparison and historical trends
```

### JSON (--json flag)
Structured output for programmatic access and automation:
```bash
./nexus analyze --json | jq '.[] | select(.max_complexity > 10)'
./nexus advise --json | jq '.[] | select(.severity == "critical")'
./nexus refactor --json | python3 summarize.py
```

### No Color (--no-color flag)
Plain text output without ANSI color codes:
```bash
./nexus analyze --no-color > report.txt
```

## File Structure

```
/workspace/
├── nexus                           # Main CLI entry point
├── README.md                       # This file
│
├── complexity-analyzer/            # Code complexity analysis
│   ├── analyzer.py                # Main analyzer tool
│   └── README.md                  # Detailed documentation
│
├── code-advisor/                   # Recommendation engine
│   ├── advisor.py                 # Main advisor tool
│   └── README.md                  # Detailed documentation
│
├── code-refactor/                  # Refactoring opportunities
│   ├── refactor.py                # Main refactor tool
│   └── README.md                  # Detailed documentation
│
├── codestats/                      # Repository analytics
│   ├── stats.py                   # Main stats tool
│   └── README.md                  # Detailed documentation
│
├── metrics-tracker/                # Trend analysis
│   ├── tracker.py                 # Main tracker tool
│   └── README.md                  # Detailed documentation
│
└── .metrics/                       # Historical snapshots (auto-created)
    ├── 2026-02-15T04-11-48-analyze.json
    ├── 2026-02-15T04-12-15-stats.json
    └── ...
```

## Design Philosophy

### Zero Dependencies
Uses only Python's standard library. No pip installs required. Works in any Python 3.6+ environment.

### Composable Tools
Each tool does one thing well. Combine them with pipes for powerful analysis workflows:
```bash
./nexus analyze --json | ./nexus advise | tee report.txt
```

### Safe by Default
Never modifies code automatically. Always shows you what would be changed before applying.

### Clear Severity Prioritization
Every issue is classified by severity (critical/high/moderate/low) so you know what to focus on.

### Beautiful Output
Colored, emoji-enhanced output that's easy to scan and understand.

### Useful for Everyone
- **Developers**: Improve your own code
- **Teams**: Spot patterns in team behavior and code quality
- **DevOps**: Integrate into CI/CD pipelines
- **Managers**: Track project health metrics
- **Researchers**: Export metrics for analysis

## Thresholds & Customization

Default thresholds (can be modified in source):

| Metric | Threshold | Severity |
|--------|-----------|----------|
| Cyclomatic Complexity | 10 | High |
| Function Length | 50 lines | Moderate |
| Nesting Depth | 4 levels | Moderate |
| File Size | 50 lines | Moderate |

To customize, edit the threshold constants in each tool's source file.

## Use Cases

### Onboarding New Team Members
Show them the codebase metrics to understand complexity and organization.

### Code Review Process
Run analysis before code review to identify potential issues.

### Refactoring Planning
Use refactor tool to identify candidates, then track improvements over time.

### Technical Debt Management
Monitor metrics over time to see if technical debt is growing or shrinking.

### Performance Baseline
Establish metrics baseline, then verify improvements after optimization.

### Quality Gates for CI/CD
Fail builds if metrics exceed thresholds, enforce quality standards.

## Performance

- **Analyze**: ~100ms per file (depends on file size and complexity)
- **Advise**: ~10ms per file (fast in-memory analysis)
- **Refactor**: ~100ms per file (AST-based analysis)
- **Stats**: ~1-5 seconds (git history processing)
- **Track**: ~50ms (file I/O)

Typical full analysis of 1000-file project: <30 seconds

## Limitations & Future Work

### Current Limitations
- Python-only (could extend to JavaScript, Go, etc.)
- No automatic refactoring (recommendations only)
- Simple duplication detection (exact line matches only)
- No type-aware analysis

### Planned Enhancements
- Auto-apply safe refactorings
- Generate refactored code with diffs
- Support more languages
- Type hint analysis
- Performance profiling
- Integration with code formatters
- VS Code plugin
- Web dashboard for metrics visualization

## Contributing

Each tool is self-contained in its own directory with minimal dependencies.

To extend or modify:
1. Edit the relevant tool file (e.g., `code-advisor/advisor.py`)
2. Test with: `./nexus COMMAND --help`
3. Commit changes to git
4. Tools are hot-reloadable via the NEXUS CLI wrapper

## License

MIT License - Use freely for any purpose.

## See Also

- **Python Code Complexity**: https://en.wikipedia.org/wiki/Cyclomatic_complexity
- **Code Refactoring**: https://en.wikipedia.org/wiki/Code_refactoring
- **Code Smell**: https://en.wikipedia.org/wiki/Code_smell
- **Technical Debt**: https://en.wikipedia.org/wiki/Technical_debt

## Support

For issues with specific tools, see their individual README files:
- `complexity-analyzer/README.md` - Code analysis help
- `code-advisor/README.md` - Recommendation help
- `code-refactor/README.md` - Refactoring help
- `codestats/README.md` - Repository analysis help
- `metrics-tracker/README.md` - Trend tracking help

## Version History

**v1.2.0** (current)
- Added Code Refactoring Engine for identifying refactoring opportunities
- Integrated refactor tool into NEXUS CLI
- Updated documentation and workflows

**v1.1.0**
- Added Code Advisor for actionable recommendations
- Added Metrics Tracker for trend analysis
- Refactored codebase for consistency

**v1.0.0**
- Initial release with Code Complexity Analyzer and CodeStats
- Unified NEXUS CLI wrapper
- Comprehensive documentation

---

Built with care for developers who want to understand their code better.
