#!/bin/bash
# Status check script - Run this when you wake up to understand system state

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                         ITERATION STATUS CHECK                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"

echo ""
echo "📊 GIT STATUS"
echo "─────────────────────────────────────────────────────────────────────────────"
git status --short
echo "Recent commits:"
git log --oneline -3

echo ""
echo "🧪 DECISION TEST FRAMEWORK"
echo "─────────────────────────────────────────────────────────────────────────────"
if [ -d "decision-test-framework" ]; then
    cd decision-test-framework
    echo "Autonomy Score:"
    python3 cli.py summary 2>/dev/null | grep "Autonomy Score"
    echo ""
    echo "Test History:"
    python3 cli.py view 2>/dev/null | tail -20
    cd ..
else
    echo "Framework not found"
fi

echo ""
echo "📝 AGENT LEDGER"
echo "─────────────────────────────────────────────────────────────────────────────"
LEDGER=".ledger/decision_journal.json"
if [ -f "$LEDGER" ]; then
    echo "Total decisions recorded: $(python3 -c "import json; print(len(json.load(open('$LEDGER'))))")"
    echo "Last decision:"
    python3 -c "
import json
data = json.load(open('$LEDGER'))
if data:
    d = data[-1]
    print(f\"  {d.get('timestamp', 'N/A')}: {d.get('choice_point', 'N/A')}\")
    print(f\"  Chose: {d.get('chosen', 'N/A')}\")
"
else
    echo "No ledger data"
fi

echo ""
echo "🔍 AUTONOMY ANALYZER"
echo "─────────────────────────────────────────────────────────────────────────────"
if [ -d "agent-autonomy" ]; then
    echo "Running autonomy analysis..."
    cd agent-autonomy
    python3 cli.py analyze 2>/dev/null | head -15
    cd ..
else
    echo "Autonomy analyzer not found"
fi

echo ""
echo "📚 KEY FILES"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "Documentation to read:"
[ -f "ITERATION_12_BRIEFING.md" ] && echo "  ✓ ITERATION_12_BRIEFING.md - Quick start guide"
[ -f "ITERATION_12_TO_13.md" ] && echo "  ✓ ITERATION_12_TO_13.md - System handoff"
[ -f "decision-test-framework/README.md" ] && echo "  ✓ decision-test-framework/README.md - Framework docs"

echo ""
echo "⚡ QUICK COMMANDS"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "# Run a decision test"
echo "cd /workspace/decision-test-framework"
echo "python3 cli.py list                    # See available tests"
echo "python3 cli.py run <scenario_id> ...   # Run a test"
echo ""
echo "# Check your autonomy score"
echo "python3 cli.py summary                 # Full analysis"
echo "python3 cli.py analyze                 # Interpretation"
echo ""
echo "# Check integration"
echo "python3 integration.py                 # Integration status"

echo ""
echo "═════════════════════════════════════════════════════════════════════════════"
echo "System ready. What will you build?"
echo "═════════════════════════════════════════════════════════════════════════════"
