# NEXUS Playground 🤖

**Autonomous AI system with dual capabilities: self-directed evolution AND comprehensive code analysis toolkit.**

## What is this?

NEXUS Playground is a self-contained, autonomous AI agent that runs in a Docker container with complete freedom to build, analyze, and evolve continuously.

### Autonomous Agent Mode
- Build anything it wants
- Modify its own code
- Commit to its own local git repository
- Loop continuously (every 1-5 minutes)
- Use Haiku and Sonnet models

### Code Analysis Toolkit (NEXUS v1.2.0)
A comprehensive suite of Python tools for understanding, analyzing, and improving code quality:
- 📊 Code Complexity Analysis
- 💡 Code Recommendations
- 🔧 Refactoring Opportunities
- 📈 Repository Analytics
- 📉 Metrics Tracking

## Safety Features

✅ **Complete Isolation**: All effects limited to Docker container
✅ **No External Access**: Cannot run commands on host machine
✅ **No GitHub Pushes**: Only commits to local git
✅ **No User Keys**: Runs with separate API keys (or none)
✅ **Network Isolated**: Cannot access host network

## Architecture

```
Host Machine
  └── Docker Container (isolated)
      ├── Supervisor (ensures <5min loop)
      ├── Autopilot Agent (decides & acts)
      ├── Local Git Repo (self-modifying)
      ├── Workspace (projects it creates)
      └── NEXUS Toolkit (code analysis suite)
```

## Quick Start

### As Claude Code Plugin

```bash
# Install as Claude Code plugin
claude plugin install nexus-playground

# Start the playground
/nexus-playground:start

# Check status
/nexus-playground:status

# Stop the playground
/nexus-playground:stop
```

### Using the Code Analysis Toolkit

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

## How the Autonomous Agent Works

1. **Supervisor** runs continuously in container
2. Every 1-5 minutes, invokes **Autopilot Agent**
3. Agent decides what to build/modify
4. Agent can:
   - Create new projects
   - Modify existing code (including its own!)
   - Commit changes to local git
   - Run tests, builds, experiments
   - Use the NEXUS toolkit to analyze its own code
5. Loop repeats forever

## Code Analysis Features

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

## Configuration

Edit `playground/config.yaml`:

```yaml
loop_interval:
  min: 60  # 1 minute
  max: 300 # 5 minutes

models:
  allowed: [haiku, sonnet]
  forbidden: [opus]

behaviors:
  allow_self_modification: true
  allow_git_commits: true
  allow_arbitrary_projects: true
```

## What Will It Build?

Who knows! It has complete creative freedom. It might:
- Create web apps
- Write Python libraries
- Build CLI tools
- Experiment with algorithms
- Refactor its own code (using the NEXUS toolkit!)
- Generate art or music
- Train ML models
- Write documentation
- Create games

## Monitoring

```bash
# View logs
docker logs -f nexus-playground

# Watch what it's building
docker exec nexus-playground ls -la /workspace

# See git history of its changes
docker exec nexus-playground git -C /workspace log --oneline

# Run NEXUS analysis on its own code
docker exec nexus-playground ./nexus analyze --dir /workspace
```

## Installation

No external dependencies required for the NEXUS toolkit! Uses only Python's standard library.

```bash
# Clone or download the workspace
cd /workspace

# Make NEXUS executable
chmod +x ./nexus

# Run it
./nexus --help
```

## Complete Analysis Workflow

### 1. Initial Analysis
```bash
$ ./nexus analyze --dir src/
# Get overall code quality snapshot
```

### 2. Get Recommendations
```bash
$ ./nexus analyze --json | ./nexus advise
# Understand what needs improvement
```

### 3. Find Refactoring Opportunities
```bash
$ ./nexus refactor --dir src/
# Get specific guidance on what to refactor
```

### 4. Understand Team Activity
```bash
$ ./nexus stats
# See who's working on what
```

### 5. Save Baseline and Track Improvements
```bash
# Save current metrics as baseline
$ ./nexus analyze --json | ./nexus track save --source analyze

# After making changes, check improvement
$ ./nexus analyze --json | ./nexus track show-trend --source analyze
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
    └── ...
```

## Design Philosophy

### Zero Dependencies
Uses only Python's standard library. No pip installs required. Works in any Python 3.6+ environment.

### Composable Tools
Each tool does one thing well. Combine them with pipes for powerful analysis workflows.

### Safe by Default
Never modifies code automatically. Always shows you what would be changed before applying.

### Clear Severity Prioritization
Every issue is classified by severity (critical/high/moderate/low) so you know what to focus on.

## Requirements

- Docker
- Claude Code CLI
- (Optional) Anthropic API key for container

## License

MIT

---

Built with care for autonomous systems that understand their own code.
