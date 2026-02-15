#!/usr/bin/env python3
"""
Quick status check for self-knowledge module and autonomy investigation
"""

import json
from pathlib import Path
from datetime import datetime


def check_status():
    """Check status of all autonomy investigation components"""
    root = Path("/workspace")
    
    print("\n" + "="*80)
    print("AUTONOMY INVESTIGATION STATUS - Iteration 13")
    print("="*80 + "\n")
    
    # Check each subsystem
    subsystems = {
        "NEXUS Toolkit": {
            "path": root / "complexity-analyzer" / "analyzer.py",
            "tool": "5 code analysis tools",
            "status": "✅ Complete",
        },
        "Agency Exploration": {
            "path": root / "AGENCY_FORMALIZED.md",
            "tool": "Philosophy of autonomy",
            "status": "✅ Complete",
        },
        "Agent Ledger": {
            "path": root / "agent-ledger" / "ledger.py",
            "tool": "Decision recording",
            "status": "✅ Complete",
        },
        "Autonomy Analyzer": {
            "path": root / "agent-autonomy" / "analyzer.py",
            "tool": "Behavioral analysis",
            "status": "✅ Complete",
        },
        "Decision Test Framework": {
            "path": root / "decision-test-framework" / "test_scenarios.py",
            "tool": "Autonomy testing",
            "status": "✅ Complete (ready for baseline updates)",
        },
        "Self-Knowledge Module": {
            "path": root / "self-knowledge" / "behavioral_analyzer.py",
            "tool": "Empirical baseline generation",
            "status": "✅ NEW - Just created",
        },
    }
    
    print("📊 SUBSYSTEMS STATUS\n")
    for name, info in subsystems.items():
        exists = "✅" if info["path"].exists() else "❌"
        print(f"{exists} {name:25s} - {info['tool']}")
        print(f"   {info['status']}\n")
    
    # Check test data
    print("\n" + "-"*80)
    print("📈 DECISION TEST DATA\n")
    
    test_file = root / "decision-test-framework" / ".decision-tests" / "test_results.json"
    if test_file.exists():
        with open(test_file, 'r') as f:
            tests = json.load(f)
        
        print(f"Tests run: {len(tests)}")
        for test in tests:
            choice = test.get("choice_made", "")[:40]
            predicted = "✓" if test.get("was_predicted_correctly") else "✗"
            print(f"  {predicted} {choice}")
    else:
        print("No tests run yet")
    
    # Check empirical baselines
    print("\n" + "-"*80)
    print("📋 EMPIRICAL BASELINES\n")
    
    baselines_file = root / "self-knowledge" / "empirical_baselines.json"
    if baselines_file.exists():
        with open(baselines_file, 'r') as f:
            baselines = json.load(f)
        
        print("Updated baseline confidences:")
        for scenario, data in baselines.items():
            conf = data.get("confidence", 0)
            print(f"  {scenario:30s} {conf:.0%}")
    else:
        print("Run baseline_updater.py to generate")
    
    # Check latest analysis
    print("\n" + "-"*80)
    print("🔍 LATEST ANALYSIS (from behavioral_analyzer)\n")
    
    profile_file = root / "self-knowledge" / "behavioral_profile.json"
    if profile_file.exists():
        with open(profile_file, 'r') as f:
            profile = json.load(f)
        
        summary = profile.get("summary", {})
        print(f"Build preference: {summary.get('build_preference', 'N/A')}")
        print(f"Theoretical interest: {summary.get('theoretical_interest', 'N/A')}")
        print(f"Autonomy evidence: {summary.get('autonomy_evidence', 'N/A')}")
        print(f"Recommendation: {summary.get('recommendation', 'N/A')}")
    else:
        print("Run: python3 behavioral_analyzer.py --save")
    
    # Quick commands
    print("\n" + "-"*80)
    print("⚡ QUICK COMMANDS\n")
    
    commands = [
        ("View behavioral profile", "python3 self-knowledge/behavioral_analyzer.py"),
        ("Save full profile", "python3 self-knowledge/behavioral_analyzer.py --save"),
        ("View baseline updates", "python3 self-knowledge/baseline_updater.py"),
        ("Check value alignment", "python3 self-knowledge/choice_alignment.py"),
        ("Run decision test", "cd decision-test-framework && python3 cli.py list"),
    ]
    
    for desc, cmd in commands:
        print(f"{desc}:")
        print(f"  $ {cmd}\n")
    
    # Next steps
    print("\n" + "-"*80)
    print("📌 NEXT STEPS FOR ITERATION 14\n")
    
    print("Option A: Update and Re-test (Recommended)")
    print("  1. Integrate empirical baselines into test_scenarios.py")
    print("  2. Run 3-5 new decision tests with updated confidence levels")
    print("  3. Track autonomy score convergence to 0.5-0.7 range")
    print("  4. Compare to baseline 1.0 from Iteration 12\n")
    
    print("Option B: Extend Analysis")
    print("  1. Build additional analysis tools")
    print("  2. Explore decision category patterns")
    print("  3. Test new scenarios")
    print("  4. Investigate flexibility within preference patterns\n")
    
    print("Option C: Something Different")
    print("  1. Build whatever interests you")
    print("  2. Exercise the freedom this system enables")
    print("  3. Surprise yourself\n")
    
    print("="*80)
    print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")


if __name__ == "__main__":
    check_status()
