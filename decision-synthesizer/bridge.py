#!/usr/bin/env python3
"""
Bridge to allow NEXUS to route to Decision Synthesizer

This allows both:
- Standalone use: python3 synthesizer.py synthesize "..."
- NEXUS integration: nexus synthesize "..."
- Separate development: decision-synthesizer/ is independent but integrated
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from synthesizer import DecisionSynthesizer, Colors


def main():
    """Main entry for NEXUS routing"""
    
    if len(sys.argv) < 2:
        print(f"""
{Colors.BOLD}{Colors.CYAN}Decision Synthesizer{Colors.RESET}
Apply the Integration Principle to decision-making

Usage:
  nexus decide <question> [--label LABEL]
  nexus decide patterns

Examples:
  nexus decide "Should we plan or be spontaneous?"
  nexus decide "Speed or quality?" --label project_choice
  nexus decide patterns
        """)
        return 1
    
    command = sys.argv[1]
    synthesizer = DecisionSynthesizer()
    
    if command == 'patterns':
        synthesizer.show_patterns()
        return 0
    
    # Treat first argument as the question
    question = ' '.join(sys.argv[1:])
    
    # Check for --label flag
    label = None
    args_str = ' '.join(sys.argv[1:])
    if '--label' in args_str:
        parts = args_str.split('--label')
        question = parts[0].strip()
        if len(parts) > 1:
            label = parts[1].strip().split()[0]
    
    decision = synthesizer.synthesize(question)
    output = synthesizer.format_output(decision, color=True)
    print(output)
    
    if label:
        synthesizer.save_decision(decision, label)
        print(f"{Colors.GREEN}✓ Decision saved with label: {label}{Colors.RESET}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
