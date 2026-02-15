---
name: reset
description: Reset playground (delete container and volumes). Use when the user says "reset playground", "clean playground", or "start fresh".
---

# Reset NEXUS Playground

Completely removes the container and all workspace data.

## Reset

```bash
echo "⚠️  Resetting NEXUS Playground..."
echo "This will delete the container and all workspace data!"
read -p "Are you sure? (y/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
  docker stop nexus-playground 2>/dev/null || true
  docker rm nexus-playground 2>/dev/null || true
  docker volume rm nexus-playground-workspace 2>/dev/null || true
  docker volume rm nexus-playground-logs 2>/dev/null || true
  echo "✅ Playground reset complete"
else
  echo "❌ Reset cancelled"
fi
```

## Warning

This permanently deletes:
- All files created by the AI
- All git history
- All logs

Start fresh with `/nexus-playground:start`
