---
name: workspace
description: Browse workspace files. Use when the user says "playground workspace", "show workspace", or "what has it built".
---

# Browse Playground Workspace

Shows all files created by the autonomous AI.

## View Workspace

```bash
echo "📂 Playground Workspace"
echo "======================"
docker exec nexus-playground find /workspace -type f 2>/dev/null | head -50 || echo "Container not running"
```

## Information Shown

- All files created by the AI
- File paths relative to /workspace
- Limited to first 50 files

For full details, use:
- `/nexus-playground:exec ls -la /workspace`
- `/nexus-playground:status` for git history
