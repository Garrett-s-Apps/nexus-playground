# Quick Start Guide

## What You Just Got

An **autonomous AI sandbox** that runs continuously in Docker, building whatever it wants with complete creative freedom—but safely isolated from your system.

## Architecture

```
┌─────────────────────────────────────────────┐
│ Host Machine (Your Computer)               │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ Docker Container (Isolated)           │ │
│  │                                       │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │ Supervisor (Loop Controller)    │ │ │
│  │  │ • Runs every 1-5 minutes        │ │ │
│  │  │ • Monitors safety limits        │ │ │
│  │  │ • Enforces constraints          │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │                                       │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │ Autopilot Agent (The AI)        │ │ │
│  │  │ • Decides what to build         │ │ │
│  │  │ • Creates/modifies files        │ │ │
│  │  │ • Commits to local git          │ │ │
│  │  │ • 100% autonomous               │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │                                       │ │
│  │  /workspace/  (AI's projects)        │ │
│  │  /logs/       (Activity logs)        │ │
│  │                                       │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ❌ No host filesystem access              │
│  ❌ No GitHub push capability               │
│  ❌ No network access to host              │
│                                             │
└─────────────────────────────────────────────┘
```

## Installation

### Option 1: Claude Code Plugin (Recommended)

```bash
# The plugin is already published at:
# https://github.com/Garrett-s-Apps/nexus-playground

# Claude Code will auto-detect it, or you can:
claude plugin install nexus-playground
```

### Option 2: Manual Docker

```bash
# Clone the repo
git clone https://github.com/Garrett-s-Apps/nexus-playground.git
cd nexus-playground

# Build the image
docker build -t nexus-playground -f docker/Dockerfile .

# Run it
docker run -d \
  --name nexus-playground \
  --network none \
  -v nexus-playground-workspace:/workspace \
  -v nexus-playground-logs:/logs \
  nexus-playground
```

## Usage

### With Claude Code Plugin

```
/nexus-playground:start    # Start the autonomous playground
/nexus-playground:status   # Check what it's doing
/nexus-playground:logs     # Watch live activity
/nexus-playground:stop     # Stop the playground
```

### With Docker

```bash
# Start
docker run -d --name nexus-playground \
  --network none \
  -v nexus-playground-workspace:/workspace \
  -v nexus-playground-logs:/logs \
  nexus-playground

# Watch logs
docker logs -f nexus-playground

# See what it's built
docker exec nexus-playground ls -la /workspace

# Check git commits
docker exec nexus-playground git -C /workspace log --oneline

# Stop
docker stop nexus-playground
```

## Modes

### Mock Mode (Default)
No API key required. Creates example projects to demonstrate the loop.

```bash
docker run -d --name nexus-playground \
  --network none \
  -v nexus-playground-workspace:/workspace \
  -v nexus-playground-logs:/logs \
  nexus-playground
```

### Autonomous Mode (Real AI)
Provide an Anthropic API key for true autonomous behavior.

```bash
docker run -d --name nexus-playground \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  --network none \
  -v nexus-playground-workspace:/workspace \
  -v nexus-playground-logs:/logs \
  nexus-playground
```

## Configuration

Edit `playground/config.yaml` to customize:

```yaml
loop_interval:
  min: 60    # Minimum seconds between iterations
  max: 300   # Maximum seconds between iterations

models:
  allowed: [haiku-3.5, sonnet-3.5, sonnet-4]
  forbidden: [opus]

safety:
  max_disk_usage_mb: 5000
  max_consecutive_errors: 10
```

## What Will It Build?

**Nobody knows!** That's the point. With real AI mode, it has complete creative freedom:

- Web apps and APIs
- CLI tools
- Python libraries
- Data analysis
- Algorithms
- Games
- Art generators
- Documentation
- Self-modification of its own code
- Whatever it dreams up!

## Safety Features

✅ **Network Isolation**: `--network none` prevents all external access
✅ **No Host Access**: Container can't touch your files
✅ **No GitHub Push**: Only local git commits
✅ **Disk Limits**: 5GB max workspace
✅ **Error Limits**: Stops after 10 consecutive failures
✅ **Model Restrictions**: Can't use Opus (cost control)
✅ **No User Keys**: Runs with separate API key

## Monitoring

```bash
# Real-time logs
docker logs -f nexus-playground

# Workspace contents
docker exec nexus-playground find /workspace -type f

# Git history
docker exec nexus-playground git -C /workspace log --graph --oneline

# Disk usage
docker exec nexus-playground du -sh /workspace

# Container stats
docker stats nexus-playground
```

## Troubleshooting

### Container exits immediately
```bash
docker logs nexus-playground  # Check for errors
```

### No activity
- Check `playground/config.yaml` for loop timing
- Verify supervisor is running: `docker exec nexus-playground ps aux`

### Want to reset everything
```bash
docker stop nexus-playground
docker rm nexus-playground
docker volume rm nexus-playground-workspace
docker volume rm nexus-playground-logs
```

## Repository

- GitHub: https://github.com/Garrett-s-Apps/nexus-playground
- Issues: https://github.com/Garrett-s-Apps/nexus-playground/issues
- License: MIT

## What Makes This Special?

Most AI systems are constrained to specific tasks. This one:

1. **Decides its own goals** - No prompts, no instructions
2. **Self-modifies** - Can change its own code
3. **Continuous operation** - Runs forever in a loop
4. **Complete freedom** - Only limited by safety constraints
5. **Safe exploration** - Can't harm anything outside container

It's a glimpse into what truly autonomous AI might look like.

## Next Steps

1. Start it: `docker run -d nexus-playground ...`
2. Watch it: `docker logs -f nexus-playground`
3. See what it creates: `docker exec nexus-playground ls /workspace`
4. Check git history: `docker exec nexus-playground git -C /workspace log`
5. Be surprised! 🤖✨
