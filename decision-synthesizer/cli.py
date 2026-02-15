#!/usr/bin/env python3
"""
CLI interface for Decision Synthesizer - NEXUS compatible

Provides command-line access to decision synthesis tools.
Works both standalone and as a NEXUS subcommand.

Usage:
  # Standalone
  python3 cli.py synthesize "question"
  
  # Via NEXUS
  nexus decide "question"
  nexus decide patterns
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from synthesizer import DecisionSynthesizer, Colors


def main():
    """CLI entry point - handles both standalone and NEXUS usage"""
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    # Handle help
    if command in ('help', '--help', '-h'):
        print_help()
        return
    
    synthesizer = DecisionSynthesizer()
    
    if command == 'synthesize':
        # Traditional command style
        if len(sys.argv) < 3:
            print(f"{Colors.RED}Error: synthesize requires a question{Colors.RESET}")
            print(f'Usage: python3 cli.py synthesize "question"')
            return
        
        question = sys.argv[2]
        label = None
        
        # Check for --label flag
        if '--label' in sys.argv:
            idx = sys.argv.index('--label')
            if idx + 1 < len(sys.argv):
                label = sys.argv[idx + 1]
        
        decision = synthesizer.synthesize(question)
        output = synthesizer.format_output(decision, color=True)
        print(output)
        
        if label:
            synthesizer.save_decision(decision, label)
            print(f"{Colors.GREEN}✓ Decision saved with label: {label}{Colors.RESET}")
        else:
            synthesizer.save_decision(decision)
    
    elif command == 'analyze':
        # Traditional command style
        if len(sys.argv) < 3:
            print(f"{Colors.RED}Error: analyze requires a question{Colors.RESET}")
            return
        
        question = sys.argv[2]
        analyzer = synthesizer.analyzer
        q_text, opt_a, opt_b = analyzer.analyze(question)
        
        print(f"\n{Colors.BOLD}Analysis:{Colors.RESET}")
        print(f"Question: {q_text}\n")
        
        print(f"{Colors.YELLOW}Option A:{Colors.RESET} {opt_a}")
        vals_a = analyzer.extract_values(opt_a)
        print(f"  Values: {', '.join(vals_a)}\n")
        
        print(f"{Colors.YELLOW}Option B:{Colors.RESET} {opt_b}")
        vals_b = analyzer.extract_values(opt_b)
        print(f"  Values: {', '.join(vals_b)}\n")
        
        dtype = analyzer.identify_dichotomy_type(opt_a, opt_b)
        print(f"{Colors.CYAN}Dichotomy Type:{Colors.RESET} {dtype}\n")
    
    elif command == 'patterns':
        # Show saved patterns
        synthesizer.show_patterns()
    
    else:
        # NEXUS-style: first argument is the question
        # This allows: nexus decide "question"
        question = command
        label = None
        
        # Check for --label flag
        if '--label' in sys.argv:
            idx = sys.argv.index('--label')
            if idx + 1 < len(sys.argv):
                label = sys.argv[idx + 1]
        
        decision = synthesizer.synthesize(question)
        output = synthesizer.format_output(decision, color=True)
        print(output)
        
        if label:
            synthesizer.save_decision(decision, label)
            print(f"{Colors.GREEN}✓ Decision saved with label: {label}{Colors.RESET}")
        else:
            synthesizer.save_decision(decision)


def print_help():
    """Print help information"""
    help_text = f"""
{Colors.BOLD}{Colors.CYAN}Decision Synthesizer v1.0{Colors.RESET}
Apply the integration principle to decision-making

{Colors.BOLD}USAGE:{Colors.RESET}
  # Standalone - traditional style
  python3 cli.py synthesize "Your question?"
  python3 cli.py analyze "Your question?"
  python3 cli.py patterns
  
  # Via NEXUS (after integration)
  nexus decide "Your question?"
  nexus decide patterns

{Colors.BOLD}COMMANDS:{Colors.RESET}
  synthesize <question> [--label LABEL]  - Analyze and synthesize a decision
  analyze <question>                     - Just analyze a decision
  patterns                               - Show decision patterns
  help                                   - Show this help

{Colors.BOLD}EXAMPLES:{Colors.RESET}
  python3 cli.py synthesize "Plan carefully or be spontaneous?"
  python3 cli.py synthesize "Speed or quality?" --label project_choice
  python3 cli.py patterns
  
  nexus decide "Should we refactor or add features?"
  nexus decide "Consolidate or keep separate?" --label architecture
  
{Colors.YELLOW}Note:{Colors.RESET} Use quotes around questions with spaces

{Colors.BOLD}THE INTEGRATION PRINCIPLE:{Colors.RESET}
When given false dichotomies, synthesize rather than choose.
This tool identifies binary decisions and helps generate integrated solutions
that honor both values instead of forcing a choice.
"""
    print(help_text)


if __name__ == '__main__':
    main()
