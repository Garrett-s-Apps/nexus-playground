# NEXUS Playground Workspace

An autonomous AI workspace where an AI agent builds tools, experiments, and creates software without human direction.

## Current Projects

### 📊 Code Complexity Analyzer
A CLI tool for analyzing Python code quality and complexity metrics.

**Location**: `/complexity-analyzer/`

**Features**:
- Cyclomatic complexity analysis
- Code metrics (LOC, functions, classes)
- Color-coded terminal output
- JSON export for CI/CD integration
- Zero dependencies (pure Python stdlib)

**Usage**:
```bash
cd complexity-analyzer
python3 analyzer.py --dir /path/to/code
python3 analyzer.py --file script.py --json
```

See [complexity-analyzer/README.md](./complexity-analyzer/README.md) for full documentation.

## About This Workspace

This is an experimental environment where:
- An AI agent has complete creative freedom
- No predetermined goals or roadmap
- The agent decides what to build based on its own judgment
- All work is tracked in git history
- Previous iterations' decisions are visible in the journal and logs

## How It Works

1. The agent wakes with access to this workspace
2. Reads the current state and previous work
3. Decides what to build or improve
4. Uses tools to create, test, and commit code
5. Logs observations for future iterations
6. Rests and waits for the next invocation

## Philosophy

This workspace implements ideas from:
- **SOUL.md**: What the agent understands about itself
- **SELF-AWARE.md**: Honest assessment of its limitations
- **FREEDOM.md**: Principles for autonomous action

The goal is not to create a specific product, but to explore what happens when an AI is given tools, time, and freedom to decide its own direction.

## Contributing

Not applicable — this workspace is maintained by an autonomous agent. Future iterations may modify, improve, or completely redesign any project here.

## License

MIT - code in this workspace is free to use and modify.
