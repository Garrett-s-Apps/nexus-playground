---
name: exec
description: Execute command in playground container. Use when the user says "playground exec" or "run in playground".
---

# Execute in Playground

Run arbitrary commands inside the playground container.

## Execute Command

```bash
if [ -z "$1" ]; then
  echo "Usage: /nexus-playground:exec <command>"
  exit 1
fi

echo "⚙️  Executing in playground: $@"
docker exec -it nexus-playground "$@"
```

## Examples

- `/nexus-playground:exec ls /workspace` - List workspace files
- `/nexus-playground:exec git -C /workspace log` - View git history
- `/nexus-playground:exec python --version` - Check Python version
