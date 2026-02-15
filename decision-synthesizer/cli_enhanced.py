#!/usr/bin/env python3
"""
Enhanced CLI for Decision Synthesizer with Evolution Engine

This extends the basic CLI with optional decision evolution tracking.
The tool can now learn from decisions over time and suggest patterns.

This is EXPERIMENTAL - evolution is optional and doesn't affect core functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from synthesizer import DecisionSynthesizer, Colors
from evolution import DecisionEvolver, SynthesisQualityTracker


def print_similar_decisions(evolver: DecisionEvolver, question: str):
    """Show similar decisions from history if any exist"""
    similar = evolver.find_similar_decisions(question, max_results=2)
    
    if similar:
        print(f"\n{Colors.CYAN}{Colors.BOLD}Similar Past Decisions:{Colors.RESET}")
        for i, decision in enumerate(similar, 1):
            print(f"\n  {i}. {decision.get('question', 'N/A')}")
            rec = decision.get('recommended', '')
            if rec:
                print(f"     Synthesis: {rec[:100]}..." if len(rec) > 100 else f"     Synthesis: {rec}")


def print_learning_insights(evolver: DecisionEvolver):
    """Print what the tool has learned from decision history"""
    report = evolver.get_evolution_report()
    if report:
        print(report)
    
    insight = evolver.get_learning_insight()
    if insight:
        print(f"{Colors.CYAN}Pattern Recognition:{Colors.RESET}")
        print(insight)


def main_enhanced():
    """Interactive CLI with evolution tracking"""
    
    if len(sys.argv) < 2:
        print(f"""
{Colors.BOLD}{Colors.CYAN}Decision Synthesizer v1.1{Colors.RESET}
Apply the integration principle to decision-making
(with optional learning from decision history)

Usage:
  python3 cli_enhanced.py <command> [arguments]

Commands:
  synthesize <question> [--label LABEL]  - Analyze and synthesize a decision
  analyze <question>                     - Just analyze a decision
  patterns                               - Show decision patterns (BASIC)
  evolution                              - Show decision evolution analysis (ENHANCED)
  help                                   - Show this help

Examples:
  python3 cli_enhanced.py synthesize "Plan carefully or be spontaneous?"
  python3 cli_enhanced.py synthesize "Speed or quality?" --label engineering
  python3 cli_enhanced.py evolution
  python3 cli_enhanced.py patterns
  
{Colors.YELLOW}Note:{Colors.RESET} Use quotes around questions with spaces

ENHANCED FEATURES:
  • Decision evolution tracking
  • Learning from past decisions
  • Similar decision suggestions
  • Pattern analysis
        """)
        return
    
    command = sys.argv[1]
    
    if command == 'help':
        print("See output above for help")
        return
    
    synthesizer = DecisionSynthesizer()
    evolver = DecisionEvolver()
    
    if command == 'synthesize':
        if len(sys.argv) < 3:
            print(f"{Colors.RED}Error: synthesize requires a question{Colors.RESET}")
            print(f'Usage: python3 cli_enhanced.py synthesize "question"')
            return
        
        question = sys.argv[2]
        label = None
        
        # Check for --label flag
        if '--label' in sys.argv:
            idx = sys.argv.index('--label')
            if idx + 1 < len(sys.argv):
                label = sys.argv[idx + 1]
        
        # Show similar past decisions if any
        print_similar_decisions(evolver, question)
        
        # Generate synthesis
        decision = synthesizer.synthesize(question)
        output = synthesizer.format_output(decision, color=True)
        print(output)
        
        # Save decision
        if label:
            synthesizer.save_decision(decision, label)
            print(f"{Colors.GREEN}✓ Decision saved with label: {label}{Colors.RESET}")
        else:
            synthesizer.save_decision(decision)
            print(f"{Colors.GREEN}✓ Decision saved{Colors.RESET}")
    
    elif command == 'analyze':
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
        # Show basic pattern data
        synthesizer.show_patterns()
    
    elif command == 'evolution':
        # Show evolved patterns from decision history
        print_learning_insights(evolver)
        
        # Also show quality metrics if available
        tracker = SynthesisQualityTracker()
        stats = tracker.get_quality_stats()
        if stats:
            print(f"\n{Colors.CYAN}Synthesis Quality Feedback:{Colors.RESET}")
            print(f"  Average Rating: {stats.get('average_rating', 'N/A'):.1f}/5.0")
            print(f"  Total Feedback: {stats.get('total_feedback', 0)}")
    
    else:
        print(f"{Colors.RED}Unknown command: {command}{Colors.RESET}")
        print(f"Use '{Colors.BOLD}python3 cli_enhanced.py help{Colors.RESET}' for usage")


if __name__ == '__main__':
    main_enhanced()
