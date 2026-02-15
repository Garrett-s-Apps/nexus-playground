---
name: start
description: Start the autonomous playground container. Use when the user says "start playground", "launch playground", or "begin autonomous".
---

# Start NEXUS Playground

Starts the autonomous AI sandbox in Docker with complete isolation.

## Starting the Playground

```bash
#!/bin/bash
set -e

echo "🚀 Starting NEXUS Playground..."

# Check if container exists
if docker ps -a --format '{{.Names}}' | grep -q '^nexus-playground$'; then
  echo "📦 Container exists, starting..."
  docker start nexus-playground
else
  echo "🏗️  Building and creating container..."
  PLUGIN_DIR="$HOME/.claude/plugins/cache/nexus-playground-marketplace/nexus-playground/0.1.0"

  docker build -t nexus-playground -f "$PLUGIN_DIR/docker/Dockerfile" "$PLUGIN_DIR"

  # Run container
  docker run -d \
    --name nexus-playground \
    --restart unless-stopped \
    -v nexus-playground-workspace:/workspace \
    -v nexus-playground-logs:/logs \
    --network none \
    --memory 2g \
    --cpus 2 \
    --security-opt=no-new-privileges \
    --cap-drop=ALL \
    nexus-playground
fi

echo "✅ Playground running!"
echo "📊 View logs: /nexus-playground:logs"
echo "🛑 Stop: /nexus-playground:stop"
```

## What Happens

- Builds Docker image (first time only)
- Creates isolated container with:
  - No network access
  - 2GB RAM limit
  - 2 CPU cores
  - Persistent workspace volume
- Starts autonomous loop (1-5 minute intervals)
