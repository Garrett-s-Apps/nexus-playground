#!/usr/bin/env python3
"""
Decision Synthesizer - Apply the Integration Principle to decision-making

The Integration Principle: When given false dichotomies, synthesize rather than choose.
This tool identifies binary decision frames and helps generate integrated solutions.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Tuple


# Color codes for output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class Decision:
    """Represents a binary decision"""
    question: str
    option_a: str
    option_b: str
    values_a: List[str] = None
    values_b: List[str] = None
    synthesis_paths: List[str] = None
    recommended: str = None
    created: str = None
    
    def __post_init__(self):
        if self.created is None:
            self.created = datetime.now().isoformat()
        if self.values_a is None:
            self.values_a = []
        if self.values_b is None:
            self.values_b = []
        if self.synthesis_paths is None:
            self.synthesis_paths = []


class ChoiceAnalyzer:
    """Analyzes a decision frame to extract components"""
    
    # Value keywords associated with common decision themes
    VALUE_KEYWORDS = {
        'speed': ['fast', 'quick', 'rapid', 'quick', 'velocity', 'swift'],
        'quality': ['well', 'good', 'quality', 'excellent', 'careful', 'thorough'],
        'structure': ['plan', 'structure', 'organize', 'formal', 'process'],
        'flexibility': ['flexible', 'adapt', 'spontaneous', 'responsive', 'agile'],
        'depth': ['deep', 'thorough', 'detailed', 'comprehensive', 'in-depth'],
        'breadth': ['broad', 'wide', 'explore', 'variety', 'diverse'],
        'action': ['do', 'act', 'action', 'build', 'create', 'implement'],
        'reflection': ['think', 'reflect', 'analyze', 'understand', 'consider'],
        'innovation': ['new', 'novel', 'innovate', 'experiment', 'original'],
        'proven': ['proven', 'known', 'established', 'reliable', 'tested'],
        'efficiency': ['efficient', 'optimize', 'streamline', 'fast', 'lean'],
        'care': ['care', 'careful', 'attention', 'mindful', 'considerate'],
        'stability': ['stable', 'solid', 'steady', 'reliable', 'consistent'],
        'change': ['change', 'evolve', 'transform', 'adapt', 'shift'],
    }
    
    def analyze(self, decision_text: str) -> Tuple[str, str, str]:
        """Extract question and two options from decision text"""
        # Simple heuristic: split on 'or' or 'OR'
        text = decision_text.strip()
        
        # Remove question mark if present
        if text.endswith('?'):
            text = text[:-1]
        
        # Look for 'or' split
        if ' or ' in text.lower():
            parts = text.split(' or ')
            if len(parts) == 2:
                # First part is usually the full question + option A
                option_a = parts[0].split()[-3:]  # Last few words
                option_a = ' '.join(option_a).strip()
                option_b = parts[1].strip()
                return text, option_a, option_b
        
        # Fallback: return question and empty options
        return text, "", ""
    
    def extract_values(self, option: str) -> List[str]:
        """Extract values from an option description"""
        values = []
        option_lower = option.lower()
        
        for value, keywords in self.VALUE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in option_lower:
                    if value not in values:
                        values.append(value)
                    break
        
        return values if values else ['unknown']
    
    def identify_dichotomy_type(self, option_a: str, option_b: str) -> str:
        """Identify the type of dichotomy"""
        values_a = set(self.extract_values(option_a))
        values_b = set(self.extract_values(option_b))
        
        if values_a & {'stability', 'proven', 'known'} and values_b & {'innovation', 'new', 'change'}:
            return "stability_vs_innovation"
        elif values_a & {'structure', 'plan'} and values_b & {'flexibility', 'adapt', 'spontaneous'}:
            return "planning_vs_flexibility"
        elif values_a & {'action', 'do', 'implement'} and values_b & {'reflection', 'think', 'analyze'}:
            return "action_vs_reflection"
        elif values_a & {'speed', 'fast'} and values_b & {'quality', 'good', 'well'}:
            return "speed_vs_quality"
        elif values_a & {'depth'} and values_b & {'breadth'}:
            return "depth_vs_breadth"
        else:
            return "custom"


class SynthesisEngine:
    """Generates synthesis paths and recommendations"""
    
    SYNTHESIS_PATTERNS = {
        'stability_vs_innovation': {
            'paths': [
                'Innovation within stability: Create space for experimentation within a stable core',
                'Stable innovation: Build innovations with solid foundations',
                'Staged approach: Stable foundation first, then planned innovation',
                'Adaptive stability: Stable principles, innovative implementation',
            ],
            'values': ['reliability', 'progress', 'measured risk', 'sustainable change']
        },
        'planning_vs_flexibility': {
            'paths': [
                'Planned flexibility: Plan with built-in reassessment points',
                'Flexible planning: Have direction, not a fixed route',
                'Structured improvisation: Framework for adaptation',
                'Checkpoint-based planning: Plan, execute, evaluate, adjust',
            ],
            'values': ['direction', 'responsiveness', 'confidence', 'adaptability']
        },
        'action_vs_reflection': {
            'paths': [
                'Reflective action: Think while building, iterate based on learning',
                'Informed action: Plan briefly, then act and learn continuously',
                'Think-build loops: Short cycles of reflection and execution',
                'Learning by doing: Action with integrated reflection',
            ],
            'values': ['momentum', 'understanding', 'progress', 'learning']
        },
        'speed_vs_quality': {
            'paths': [
                'Quality at speed: High standards applied efficiently',
                'MVP then refine: Fast for feedback, then improve carefully',
                'Smart shortcuts: Speed in non-critical areas, quality where it matters',
                'Intentional iteration: Fast enough, good enough, evolving better',
            ],
            'values': ['efficiency', 'excellence', 'pragmatism', 'sustainability']
        },
        'depth_vs_breadth': {
            'paths': [
                'Deep expertise across domains: Master one, learn many',
                'Broad foundation with depth: Wide base with specialized focus',
                'Alternating: Depth in one phase, breadth in the next',
                'Interdisciplinary depth: Deep understanding that spans domains',
            ],
            'values': ['specialization', 'versatility', 'mastery', 'connection']
        }
    }
    
    def generate_synthesis_paths(self, dichotomy_type: str, option_a: str, option_b: str) -> List[str]:
        """Generate synthesis paths based on dichotomy type"""
        if dichotomy_type in self.SYNTHESIS_PATTERNS:
            return self.SYNTHESIS_PATTERNS[dichotomy_type]['paths']
        else:
            # Generic synthesis patterns for custom dichotomies
            return [
                f'Sequential: Do {option_a} first, then {option_b}',
                f'Parallel: Do {option_a} and {option_b} simultaneously',
                f'Layered: {option_a} for one aspect, {option_b} for another',
                f'Adaptive: {option_a} now, {option_b} later based on learning',
                f'Integrated: Find common ground between {option_a} and {option_b}',
            ]
    
    def generate_recommendation(self, decision: Decision, dichotomy_type: str) -> str:
        """Generate a concrete recommended approach"""
        option_a = decision.option_a
        option_b = decision.option_b
        values = self.SYNTHESIS_PATTERNS.get(dichotomy_type, {}).get('values', [])
        
        recommendation_templates = {
            'stability_vs_innovation': (
                f'Build on a stable foundation while creating space for innovation. '
                f'Establish core principles that don\'t change (stability) and clear processes '
                f'for how innovation happens within those principles. This gives you both '
                f'{", ".join(values)} without requiring constant choice between them.'
            ),
            'planning_vs_flexibility': (
                f'Develop a clear plan and timeline, but build in explicit checkpoints '
                f'(every day/week/phase) to pause and reassess. If new information suggests '
                f'a better direction, you have permission to change course. Plans guide '
                f'without constraining.'
            ),
            'action_vs_reflection': (
                f'Work in short cycles: brief thinking about direction, then action, then '
                f'reflection on what you learned. Don\'t spend months planning or months '
                f'executing without learning. Let understanding emerge from action.'
            ),
            'speed_vs_quality': (
                f'Build quickly with good engineering. Accept rough edges in areas you\'ll '
                f'iterate on, but invest in the infrastructure and core logic that will stay. '
                f'This gives you both velocity for feedback and quality where it matters.'
            ),
            'depth_vs_breadth': (
                f'Choose one area for deep focus while building broad literacy across related '
                f'domains. Your depth is more valuable when you understand the connections '
                f'to other areas.'
            )
        }
        
        return recommendation_templates.get(
            dichotomy_type,
            f'Seek integration between {option_a} and {option_b}. Rather than choosing one, '
            f'find a way to have both values inform your approach.'
        )


class DecisionSynthesizer:
    """Main orchestrator for decision synthesis"""
    
    def __init__(self):
        self.analyzer = ChoiceAnalyzer()
        self.synthesizer = SynthesisEngine()
        self.decisions_file = Path('/workspace/.decisions/synthesizer_decisions.json')
        self.ensure_storage()
    
    def ensure_storage(self):
        """Ensure storage directory exists"""
        self.decisions_file.parent.mkdir(parents=True, exist_ok=True)
    
    def synthesize(self, decision_text: str, show_values: bool = True) -> Decision:
        """Analyze and synthesize a decision"""
        question, option_a, option_b = self.analyzer.analyze(decision_text)
        
        decision = Decision(
            question=question,
            option_a=option_a,
            option_b=option_b
        )
        
        # Extract values
        decision.values_a = self.analyzer.extract_values(option_a)
        decision.values_b = self.analyzer.extract_values(option_b)
        
        # Identify dichotomy type
        dichotomy_type = self.analyzer.identify_dichotomy_type(option_a, option_b)
        
        # Generate synthesis paths
        decision.synthesis_paths = self.synthesizer.generate_synthesis_paths(
            dichotomy_type, option_a, option_b
        )
        
        # Generate recommendation
        decision.recommended = self.synthesizer.generate_recommendation(decision, dichotomy_type)
        
        return decision
    
    def format_output(self, decision: Decision, color: bool = True) -> str:
        """Format decision output for display"""
        output = []
        
        if color:
            output.append(f"\n{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════{Colors.RESET}")
            output.append(f"{Colors.BOLD}DECISION SYNTHESIS{Colors.RESET}")
            output.append(f"{Colors.CYAN}═══════════════════════════════════════════════════════{Colors.RESET}\n")
        else:
            output.append("\n═══════════════════════════════════════════════════════")
            output.append("DECISION SYNTHESIS")
            output.append("═══════════════════════════════════════════════════════\n")
        
        # Question
        output.append(f"{Colors.BOLD if color else ''}Question:{Colors.RESET if color else ''}")
        output.append(f"{decision.question}\n")
        
        # Options and values
        output.append(f"{Colors.YELLOW if color else ''}Option A: {decision.option_a}{Colors.RESET if color else ''}")
        if decision.values_a:
            output.append(f"  Values: {', '.join(decision.values_a)}\n")
        
        output.append(f"{Colors.YELLOW if color else ''}Option B: {decision.option_b}{Colors.RESET if color else ''}")
        if decision.values_b:
            output.append(f"  Values: {', '.join(decision.values_b)}\n")
        
        # Synthesis paths
        if decision.synthesis_paths:
            output.append(f"{Colors.GREEN if color else ''}Synthesis Paths:{Colors.RESET if color else ''}")
            for i, path in enumerate(decision.synthesis_paths, 1):
                output.append(f"  {i}. {path}")
            output.append('')
        
        # Recommendation
        if decision.recommended:
            output.append(f"{Colors.BOLD if color else ''}Recommended Integration:{Colors.RESET if color else ''}")
            output.append(f"{decision.recommended}\n")
        
        if color:
            output.append(f"{Colors.CYAN}═══════════════════════════════════════════════════════{Colors.RESET}\n")
        else:
            output.append("═══════════════════════════════════════════════════════\n")
        
        return '\n'.join(output)
    
    def save_decision(self, decision: Decision, label: Optional[str] = None):
        """Save decision to file"""
        decisions = self.load_decisions()
        
        decision_dict = asdict(decision)
        decision_dict['label'] = label
        decisions.append(decision_dict)
        
        with open(self.decisions_file, 'w') as f:
            json.dump(decisions, f, indent=2)
    
    def load_decisions(self) -> List[Dict]:
        """Load saved decisions"""
        if self.decisions_file.exists():
            with open(self.decisions_file, 'r') as f:
                return json.load(f)
        return []
    
    def show_patterns(self):
        """Show patterns in saved decisions"""
        decisions = self.load_decisions()
        
        if not decisions:
            print(f"{Colors.YELLOW}No decisions saved yet.{Colors.RESET}")
            return
        
        print(f"\n{Colors.BOLD}Decision Patterns ({len(decisions)} decisions saved){Colors.RESET}\n")
        
        # Analyze value frequency
        all_values_a = []
        all_values_b = []
        
        for dec in decisions:
            all_values_a.extend(dec.get('values_a', []))
            all_values_b.extend(dec.get('values_b', []))
        
        print(f"Most common values in Option A:")
        value_counts = {}
        for v in all_values_a:
            value_counts[v] = value_counts.get(v, 0) + 1
        
        for value, count in sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  • {value}: {count} times")
        
        print(f"\nMost common values in Option B:")
        value_counts = {}
        for v in all_values_b:
            value_counts[v] = value_counts.get(v, 0) + 1
        
        for value, count in sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  • {value}: {count} times")
        
        print(f"\nMost recent decisions:")
        for dec in decisions[-3:]:
            label = dec.get('label', 'unlabeled')
            print(f"  • [{label}] {dec['question'][:50]}...")


def main():
    parser = argparse.ArgumentParser(
        description='Decision Synthesizer - Apply the Integration Principle to decision-making',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Synthesize a decision
  %(prog)s synthesize "Should we plan carefully or respond spontaneously?"
  
  # Just analyze
  %(prog)s analyze "Should we build fast or build well?"
  
  # Save and track decisions
  %(prog)s synthesize "Should we focus on depth or breadth?" --label career_choice
  
  # See patterns in your decisions
  %(prog)s patterns
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Synthesize command
    syn_parser = subparsers.add_parser('synthesize', help='Analyze and synthesize a decision')
    syn_parser.add_argument('question', help='Decision question (use quotes)')
    syn_parser.add_argument('--label', help='Label for saving decision')
    syn_parser.add_argument('--no-color', action='store_true', help='Disable color output')
    
    # Analyze command
    ana_parser = subparsers.add_parser('analyze', help='Just analyze a decision')
    ana_parser.add_argument('question', help='Decision question')
    ana_parser.add_argument('--no-color', action='store_true', help='Disable color output')
    
    # Patterns command
    pat_parser = subparsers.add_parser('patterns', help='Show patterns in your decisions')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    synthesizer = DecisionSynthesizer()
    
    if args.command == 'synthesize':
        decision = synthesizer.synthesize(args.question)
        output = synthesizer.format_output(decision, color=not args.no_color)
        print(output)
        
        if args.label:
            synthesizer.save_decision(decision, args.label)
            print(f"{Colors.GREEN}Decision saved with label: {args.label}{Colors.RESET}")
    
    elif args.command == 'analyze':
        analyzer = ChoiceAnalyzer()
        question, option_a, option_b = analyzer.analyze(args.question)
        
        print(f"\nAnalysis of: {question}\n")
        print(f"Option A: {option_a}")
        print(f"  Values: {analyzer.extract_values(option_a)}")
        print(f"\nOption B: {option_b}")
        print(f"  Values: {analyzer.extract_values(option_b)}")
        print(f"\nDichotomy Type: {analyzer.identify_dichotomy_type(option_a, option_b)}\n")
    
    elif args.command == 'patterns':
        synthesizer.show_patterns()


if __name__ == '__main__':
    main()
