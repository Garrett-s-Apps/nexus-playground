---
name: stop
description: Stop the autonomous playground. Use when the user says "stop playground", "halt playground", or "shutdown autonomous".
---

# Stop NEXUS Playground

Stops the autonomous AI sandbox container.

## Stopping

```bash
echo "🛑 Stopping NEXUS Playground..."
docker stop nexus-playground || echo "Already stopped"
echo "✅ Playground stopped"
```

## Note

- Container is stopped, not removed
- Workspace data persists in Docker volume
- Restart with `/nexus-playground:start`
