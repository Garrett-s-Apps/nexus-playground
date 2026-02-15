# NEXUS Complete Playground

**Integrated repository containing both NEXUS Playground (autonomous AI) and NEXUS Toolkit (code analysis).**

---

## Part 1: NEXUS Playground 🤖

**Autonomous AI system that builds whatever it wants in complete isolation.**

### What is this?

NEXUS Playground is a self-contained, autonomous AI agent that runs in a Docker container with complete freedom to:
- Build anything it wants
- Modify its own code
- Commit to its own local git repository
- Loop continuously (every 1-5 minutes)
- Use Haiku and Sonnet models

### Safety Features

✅ **Complete Isolation**: All effects limited to Docker container
✅ **No External Access**: Cannot run commands on host machine
✅ **No GitHub Pushes**: Only commits to local git
✅ **No User Keys**: Runs with separate API keys (or none)
✅ **Network Isolated**: Cannot access host network

### Architecture

```
Host Machine
  └── Docker Container (isolated)
      ├── Supervisor (ensures <5min loop)
      ├── Autopilot Agent (decides & acts)
      ├── Local Git Repo (self-modifying)
      └── Workspace (projects it creates)
```

### Quick Start - Playground

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

### How It Works

1. **Supervisor** runs continuously in container
2. Every 1-5 minutes, invokes **Autopilot Agent**
3. Agent decides what to build/modify
4. Agent can:
   - Create new projects
   - Modify existing code (including its own!)
   - Commit changes to local git
   - Run tests, builds, experiments
5. Loop repeats forever

### Configuration

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

### What Will It Build?

Who knows! It has complete creative freedom. It might:
- Create web apps
- Write Python libraries
- Build CLI tools
- Experiment with algorithms
- Refactor its own code
- Generate art or music
- Train ML models
- Write documentation
- Create games

### Monitoring

```bash
# View logs
docker logs -f nexus-playground

# Watch what it's building
docker exec nexus-playground ls -la /workspace

# See git history of its changes
docker exec nexus-playground git -C /workspace log --oneline
```

---

## Part 2: NEXUS v1.2.0 - Unified Code Analysis Toolkit

A comprehensive suite of Python tools for understanding, analyzing, and improving code quality. NEXUS provides metrics, recommendations, refactoring opportunities, repository insights, and trend tracking—all in one unified toolkit.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           NEXUS v1.2.0                                       ║
║           Unified Code and Repository Analysis Toolkit                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Features

#### 📊 Code Complexity Analysis
Analyzes Python code for cyclomatic complexity, code metrics, and quality indicators.
- Detect complex functions
- Understand code organization
- Identify refactoring candidates
- JSON export for CI/CD

#### 💡 Code Recommendations
Generates actionable, severity-ranked recommendations based on metrics.
- Turn raw metrics into practical suggestions
- Prioritize refactoring by impact
- Understand why each issue matters
- Human-readable and JSON formats

#### 🔧 Refactoring Opportunities
Identifies specific refactoring opportunities with detailed analysis.
- Detect overly complex functions
- Find deeply nested code
- Spot code duplication
- Improve function naming
- Clear priority and guidance for each opportunity

#### 📈 Repository Analytics
Analyze git history for development patterns and team metrics.
- Contributor activity analysis
- Commit frequency trends
- Author statistics
- Code change patterns
- Team velocity insights

#### 📉 Metrics Tracking
Track code quality metrics over time to spot trends and regressions.
- Compare current vs. historical metrics
- Detect improvements and regressions
- Monitor project health
- Enable data-driven decisions

### Installation

No external dependencies required! Uses only Python's standard library.

```bash
# Clone or download the workspace
cd /workspace

# Make NEXUS executable
chmod +x ./nexus

# Run it
./nexus --help
```

### Quick Start - Toolkit

#### Basic Workflow

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

#### Common Commands

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

### Tools Overview

See individual tool README files for detailed documentation:
- `complexity-analyzer/README.md` - Code analysis help
- `code-advisor/README.md` - Recommendation help
- `code-refactor/README.md` - Refactoring help
- `codestats/README.md` - Repository analysis help
- `metrics-tracker/README.md` - Trend tracking help

---

## Requirements

- Docker
- Claude Code CLI
- Python 3.6+ (for toolkit)
- (Optional) Anthropic API key for container

## License

MIT License - Use freely for any purpose.

---

Built with care for autonomous AI exploration and code quality analysis.
