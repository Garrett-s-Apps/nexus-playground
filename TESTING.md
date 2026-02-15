# Testing Guide

## Quick Test (Local)

Test the playground components locally before running in Docker:

```bash
# Test supervisor (Ctrl+C to stop after one iteration)
cd playground
python supervisor.py

# Test autopilot agent directly
python autopilot.py
```

## Docker Test

Build and run the playground in Docker:

```bash
# Build image
docker build -t nexus-playground ./docker

# Run with mock mode (no API key)
docker run -it --rm \
  --name nexus-playground-test \
  -v nexus-playground-workspace:/workspace \
  -v nexus-playground-logs:/logs \
  --network none \
  nexus-playground

# Run with real Claude API (autonomous mode)
docker run -it --rm \
  --name nexus-playground-test \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  -v nexus-playground-workspace:/workspace \
  -v nexus-playground-logs:/logs \
  --network none \
  nexus-playground
```

## Plugin Test

Test the Claude Code plugin:

```bash
# Install plugin locally (for testing)
mkdir -p ~/.claude/plugins/cache/nexus-playground
cp -r . ~/.claude/plugins/cache/nexus-playground/

# Test commands in Claude Code
/nexus-playground:start
/nexus-playground:status
/nexus-playground:logs
/nexus-playground:stop
```

## Monitoring During Test

```bash
# Watch logs in real-time
docker logs -f nexus-playground-test

# Check workspace contents
docker exec nexus-playground-test ls -la /workspace

# Check git commits
docker exec nexus-playground-test git -C /workspace log --oneline

# Check disk usage
docker exec nexus-playground-test du -sh /workspace

# View configuration
docker exec nexus-playground-test cat playground/config.yaml
```

## Expected Behavior

### Mock Mode (no API key)
- Creates example projects every 1-5 minutes
- Commits to local git
- Logs "Mock mode: No API key provided"

### Autonomous Mode (with API key)
- Calls Claude API every 1-5 minutes
- Agent decides what to build
- May create projects, modify code, commit changes
- Check logs for AI's decision-making process

## Safety Checks

Verify safety features are working:

```bash
# Check network isolation
docker exec nexus-playground-test ping -c 1 google.com
# Should fail: "ping: bad address 'google.com'"

# Check disk usage limits
docker exec nexus-playground-test df -h /workspace

# Check resource limits
docker stats nexus-playground-test --no-stream

# Check that container can't access host
docker exec nexus-playground-test ls /host
# Should fail: "No such file or directory"
```

## Cleanup After Testing

```bash
# Stop and remove container
docker stop nexus-playground-test
docker rm nexus-playground-test

# Remove volumes (optional)
docker volume rm nexus-playground-workspace
docker volume rm nexus-playground-logs

# Remove image
docker rmi nexus-playground
```

## Troubleshooting

### Container exits immediately
- Check logs: `docker logs nexus-playground-test`
- Verify Python dependencies are installed
- Check for syntax errors in supervisor.py or autopilot.py

### No activity in logs
- Verify loop timing in config.yaml
- Check for errors in /logs/playground.log
- Ensure supervisor is running: `docker exec nexus-playground-test ps aux`

### API errors
- Verify ANTHROPIC_API_KEY is valid
- Check API rate limits
- Review error logs in /logs/

### Disk usage exceeded
- Lower max_disk_usage_mb in config.yaml
- Clean workspace: `docker exec nexus-playground-test rm -rf /workspace/*`
- Reset git: `docker exec nexus-playground-test git -C /workspace reset --hard HEAD~10`
