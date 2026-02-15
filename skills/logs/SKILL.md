---
name: logs
description: View live playground logs. Use when the user says "playground logs", "watch playground", or "show me what it's doing".
---

# NEXUS Playground Logs

Stream live logs from the autonomous agent.

## View Logs

```bash
echo "📜 Streaming NEXUS Playground logs (Ctrl+C to stop)..."
docker logs -f nexus-playground
```

## What You'll See

- Supervisor loop iterations
- Autonomous agent decisions
- Project creation activity
- Git commits
- Errors (if any)
- Sleep intervals between runs
