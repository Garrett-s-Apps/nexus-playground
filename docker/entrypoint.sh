#!/bin/bash
# NEXUS Playground Entrypoint

set -e

echo "🤖 NEXUS Playground Starting..."
echo "================================"
echo "Container: $(hostname)"
echo "Workspace: /workspace"
echo "Logs: /logs"
echo "================================"

# Display configuration
if [ -f playground/config.yaml ]; then
    echo "Configuration loaded ✓"
fi

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  No ANTHROPIC_API_KEY set - running in MOCK mode"
    echo "   The agent will create example projects instead of using real AI"
else
    echo "✅ ANTHROPIC_API_KEY configured - running in AUTONOMOUS mode"
fi

echo "================================"
echo ""

# Start supervisor
exec python -u playground/supervisor.py
