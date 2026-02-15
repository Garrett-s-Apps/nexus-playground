# NEXUS Playground 🤖

**Autonomous AI system that builds whatever it wants in complete isolation.**

## What is this?

NEXUS Playground is a self-contained, autonomous AI agent that runs in a Docker container with complete freedom to:
- Build anything it wants
- Modify its own code
- Commit to its own local git repository
- Loop continuously (every 1-5 minutes)
- Use Haiku and Sonnet models

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
      └── Workspace (projects it creates)
```

## Quick Start

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

## How It Works

1. **Supervisor** runs continuously in container
2. Every 1-5 minutes, invokes **Autopilot Agent**
3. Agent decides what to build/modify
4. Agent can:
   - Create new projects
   - Modify existing code (including its own!)
   - Commit changes to local git
   - Run tests, builds, experiments
5. Loop repeats forever

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
- Refactor its own code
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
```

## Requirements

- Docker
- Claude Code CLI
- (Optional) Anthropic API key for container

## License

MIT
