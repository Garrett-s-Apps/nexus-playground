---
name: releases
description: View released artifacts from the autonomous agents
user_invocable: true
trigger: playground releases
---

# NEXUS Playground Releases

View artifacts that agents have promoted to the releases branch.

## View Releases

```bash
echo "📦 Agent Releases"
echo "================="

if ! docker ps --format '{{.Names}}' | grep -q '^nexus-playground$'; then
  echo "❌ Playground container is not running."
  echo "   Start it with: /nexus-playground:start"
  exit 1
fi

# Check if releases branch exists
if docker exec nexus-playground git -C /workspace branch --list releases | grep -q releases; then
  echo ""
  echo "📋 Release history:"
  docker exec nexus-playground git -C /workspace log releases --oneline -20
  echo ""
  echo "📁 Released files:"
  docker exec nexus-playground git -C /workspace ls-tree -r --name-only releases
else
  echo ""
  echo "No releases yet. Agents can mark files for release by including"
  echo "[RELEASE:path/to/file] in their output."
fi
```
