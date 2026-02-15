---
name: status
description: Show playground status and recent activity. Use when the user says "playground status", "check playground", or "what's the playground doing".
---

# NEXUS Playground Status

Shows current status, activity, and recent changes.

## Status Check

```bash
echo "📊 NEXUS Playground Status"
echo "=========================="

if docker ps --format '{{.Names}}' | grep -q '^nexus-playground$'; then
  echo "Status: ✅ Running"
  echo ""

  echo "Container Info:"
  docker stats nexus-playground --no-stream --format "  CPU: {{.CPUPerc}}\n  Memory: {{.MemUsage}}"
  echo ""

  echo "Recent Activity (last 20 lines):"
  docker logs nexus-playground --tail 20
  echo ""

  echo "Workspace Files:"
  docker exec nexus-playground find /workspace -type f | head -20
  echo ""

  echo "Git Commits:"
  docker exec nexus-playground git -C /workspace log --oneline -5 || echo "  No commits yet"
else
  echo "Status: ❌ Not running"
  echo ""
  echo "Start with: /nexus-playground:start"
fi
```

## Information Shown

- Running status
- CPU and memory usage
- Recent log entries
- Files created in workspace
- Git commit history
