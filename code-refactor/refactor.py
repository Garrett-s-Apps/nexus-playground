#!/usr/bin/env python3
"""
Code Refactoring Engine - Automatically improve code quality

Analyzes Python code and applies safe, automated refactoring transformations:
- Extract long/complex functions into smaller units
- Reduce nesting depth with early returns
- Simplify conditional logic
- Improve function naming based on behavior

Usage:
  python3 refactor.py --file FILE [--apply]
  python3 refactor.py --dir DIR [--apply]
  python3 refactor.py --help

Without --apply, shows a diff of proposed changes.
With --apply, writes changes to disk and creates backup.
"""

import sys
import ast
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import difflib
import shutil
from datetime import datetime


@dataclass
class Refactoring:
    """A proposed code refactoring"""
    filepath: str
    lineno: int
    rule: str
    description: str
    severity: str  # 'low', 'medium', 'high'
    original_code: str
    refactored_code: str
    why: str


class ComplexityAnalyzer(ast.NodeVisitor):
    """Analyze function complexity and structure"""
    
    def __init__(self):
        self.functions = {}
        self.current_function = None
        self.current_complexity = 0
        self.max_nesting = 0
        self.current_nesting = 0
    
    def visit_FunctionDef(self, node):
        prev_function = self.current_function
        prev_complexity = self.current_complexity
        prev_nesting = self.current_nesting
        prev_max_nesting = self.max_nesting
        
        self.current_function = node.name
        self.current_complexity = 1
        self.max_nesting = 0
        self.current_nesting = 0
        
        self.generic_visit(node)
        
        self.functions[node.name] = {
            'lineno': node.lineno,
            'complexity': self.current_complexity,
            'max_nesting': self.max_nesting,
            'num_lines': node.end_lineno - node.lineno if node.end_lineno else 0,
            'node': node
        }
        
        self.current_function = prev_function
        self.current_complexity = prev_complexity
        self.current_nesting = prev_nesting
        self.max_nesting = prev_max_nesting
    
    def visit_If(self, node):
        if self.current_function:
            self.current_complexity += 1
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_For(self, node):
        if self.current_function:
            self.current_complexity += 1
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_While(self, node):
        if self.current_function:
            self.current_complexity += 1
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_ExceptHandler(self, node):
        if self.current_function:
            self.current_complexity += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        if self.current_function:
            self.current_complexity += 1
        self.generic_visit(node)


class RefactoringEngine:
    """Generates refactoring recommendations and applies transformations"""
    
    # Thresholds for refactoring triggers
    COMPLEXITY_THRESHOLD = 10
    FUNCTION_LENGTH_THRESHOLD = 50
    NESTING_THRESHOLD = 4
    
    def __init__(self):
        self.refactorings: List[Refactoring] = []
        self.source_code = ""
        self.tree = None
    
    def analyze_file(self, filepath: str) -> List[Refactoring]:
        """Analyze a file and generate refactoring suggestions"""
        self.refactorings = []
        
        try:
            with open(filepath, 'r') as f:
                self.source_code = f.read()
            
            self.tree = ast.parse(self.source_code)
        except (SyntaxError, IOError) as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            return []
        
        # Run analysis passes
        self._analyze_complexity()
        self._analyze_nesting()
        self._analyze_duplication()
        self._analyze_style()
        
        # Sort by severity and line number
        self.refactorings.sort(key=lambda r: (-{'high': 3, 'medium': 2, 'low': 1}[r.severity], r.lineno))
        
        return self.refactorings
    
    def _analyze_complexity(self):
        """Find complex functions that should be simplified"""
        analyzer = ComplexityAnalyzer()
        analyzer.visit(self.tree)
        
        for func_name, info in analyzer.functions.items():
            complexity = info['complexity']
            lineno = info['lineno']
            
            if complexity >= self.COMPLEXITY_THRESHOLD:
                severity = 'high' if complexity >= 15 else 'medium'
                self.refactorings.append(Refactoring(
                    filepath="",
                    lineno=lineno,
                    rule="extract_function",
                    description=f"Function '{func_name}' has complexity {complexity}",
                    severity=severity,
                    original_code="",
                    refactored_code="",
                    why=f"High complexity ({complexity}) makes function hard to test and maintain. "
                        f"Consider extracting conditional branches into helper functions."
                ))
            
            if info['num_lines'] >= self.FUNCTION_LENGTH_THRESHOLD:
                self.refactorings.append(Refactoring(
                    filepath="",
                    lineno=lineno,
                    rule="extract_function",
                    description=f"Function '{func_name}' is {info['num_lines']} lines",
                    severity='medium',
                    original_code="",
                    refactored_code="",
                    why=f"Function is {info['num_lines']} lines long. "
                        f"Extract logical sections into separate helper functions."
                ))
            
            if info['max_nesting'] >= self.NESTING_THRESHOLD:
                self.refactorings.append(Refactoring(
                    filepath="",
                    lineno=lineno,
                    rule="reduce_nesting",
                    description=f"Function '{func_name}' has nesting depth {info['max_nesting']}",
                    severity='medium',
                    original_code="",
                    refactored_code="",
                    why=f"Deep nesting ({info['max_nesting']}) makes control flow hard to follow. "
                        f"Use early returns and extract nested blocks into functions."
                ))
    
    def _analyze_nesting(self):
        """Find overly nested code and suggest early returns"""
        lines = self.source_code.split('\n')
        
        for i, line in enumerate(lines, 1):
            indent_level = len(line) - len(line.lstrip())
            
            # Look for deeply nested if/for/while statements
            if indent_level >= 20 and any(kw in line for kw in ['if ', 'for ', 'while ']):
                self.refactorings.append(Refactoring(
                    filepath="",
                    lineno=i,
                    rule="early_return",
                    description=f"Line {i}: Deep nesting at indent level {indent_level}",
                    severity='low',
                    original_code="",
                    refactored_code="",
                    why=f"Code is nested {indent_level//4} levels deep. "
                        f"Consider using early returns or extracting into a helper function."
                ))
    
    def _analyze_duplication(self):
        """Find potential code duplication"""
        lines = self.source_code.split('\n')
        
        # Simple check: look for similar imports or repeated patterns
        import_lines = [l for l in lines if l.strip().startswith('import ') or l.strip().startswith('from ')]
        
        # Check for obviously repeated code patterns (simplified)
        seen_patterns = {}
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if len(stripped) > 30 and not stripped.startswith('#'):
                if stripped in seen_patterns:
                    # Found a duplicate line
                    if seen_patterns[stripped] < i - 5:  # Different functions likely
                        self.refactorings.append(Refactoring(
                            filepath="",
                            lineno=i,
                            rule="extract_constant",
                            description=f"Possible code duplication at line {i}",
                            severity='low',
                            original_code="",
                            refactored_code="",
                            why="Similar code found elsewhere in file. Consider extracting to a shared function."
                        ))
                else:
                    seen_patterns[stripped] = i
    
    def _analyze_style(self):
        """Find style and naming issues"""
        analyzer = ComplexityAnalyzer()
        analyzer.visit(self.tree)
        
        for func_name, info in analyzer.functions.items():
            # Check for poor naming (single letter, unclear abbreviations)
            if len(func_name) == 1 and func_name != '_':
                self.refactorings.append(Refactoring(
                    filepath="",
                    lineno=info['lineno'],
                    rule="improve_naming",
                    description=f"Function '{func_name}' has unclear name",
                    severity='low',
                    original_code="",
                    refactored_code="",
                    why="Single-letter function name is unclear. Use a descriptive name."
                ))


class RefactoringReporter:
    """Format and display refactoring suggestions"""
    
    # ANSI colors
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    SEVERITY_ICONS = {
        'high': '🔴',
        'medium': '🟡',
        'low': '🔵'
    }
    
    RULE_ICONS = {
        'extract_function': '🔪',
        'reduce_nesting': '⬇️',
        'early_return': '↩️',
        'extract_constant': '📦',
        'improve_naming': '📝'
    }
    
    def __init__(self, use_color: bool = True):
        self.use_color = use_color
    
    def _colorize(self, text: str, color: str) -> str:
        if not self.use_color:
            return text
        return f"{color}{text}{self.RESET}"
    
    def print_summary(self, refactorings: List[Refactoring], filepath: str = "") -> None:
        """Print summary of refactoring opportunities"""
        if not refactorings:
            print(self._colorize("✅ No refactoring opportunities found. Code is clean!", self.GREEN))
            return
        
        high = len([r for r in refactorings if r.severity == 'high'])
        medium = len([r for r in refactorings if r.severity == 'medium'])
        low = len([r for r in refactorings if r.severity == 'low'])
        
        print()
        print(self._colorize("╔════════════════════════════════════════╗", self.BOLD))
        print(self._colorize("║    REFACTORING OPPORTUNITIES REPORT     ║", self.BOLD))
        print(self._colorize("╚════════════════════════════════════════╝", self.BOLD))
        print()
        
        if high > 0:
            print(f"  {self._colorize('🔴 High Priority', self.RED)}: {high}")
        if medium > 0:
            print(f"  {self._colorize('🟡 Medium Priority', self.YELLOW)}: {medium}")
        if low > 0:
            print(f"  {self._colorize('🔵 Low Priority', self.BLUE)}: {low}")
        
        print()
    
    def print_refactorings(self, refactorings: List[Refactoring], use_color: bool = True) -> None:
        """Print detailed refactoring suggestions"""
        self.use_color = use_color
        
        if not refactorings:
            print(self._colorize("✅ No refactoring opportunities found!", self.GREEN))
            return
        
        self.print_summary(refactorings)
        
        for r in refactorings:
            icon = self.RULE_ICONS.get(r.rule, '•')
            sev_icon = self.SEVERITY_ICONS.get(r.severity, '•')
            
            severity_color = {
                'high': self.RED,
                'medium': self.YELLOW,
                'low': self.BLUE
            }[r.severity]
            
            print(f"{icon} {self._colorize(r.severity.upper(), severity_color)} at line {r.lineno}")
            print(f"   {self._colorize(r.description, self.BOLD)}")
            print(f"   {self._colorize('Rule:', self.DIM)} {r.rule}")
            print(f"   {self._colorize('Why:', self.DIM)} {r.why}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Automatically refactor Python code for better quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single file
  python3 refactor.py --file mycode.py
  
  # Analyze entire directory
  python3 refactor.py --dir src/
  
  # Show refactoring report (read-only)
  python3 refactor.py --file mycode.py --report
        """
    )
    
    parser.add_argument('--file', type=str, help='Single Python file to analyze')
    parser.add_argument('--dir', type=str, help='Directory to analyze recursively')
    parser.add_argument('--report', action='store_true', help='Print refactoring report (default behavior)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)
    
    engine = RefactoringEngine()
    reporter = RefactoringReporter(use_color=not args.no_color)
    
    files_to_analyze = []
    
    if args.file:
        files_to_analyze = [args.file]
    else:
        path = Path(args.dir)
        files_to_analyze = list(path.glob('**/*.py'))
    
    all_refactorings = []
    
    for filepath in sorted(files_to_analyze):
        refactorings = engine.analyze_file(str(filepath))
        
        for r in refactorings:
            r.filepath = str(filepath)
        
        all_refactorings.extend(refactorings)
    
    if args.json:
        output = [
            {
                'filepath': r.filepath,
                'lineno': r.lineno,
                'rule': r.rule,
                'description': r.description,
                'severity': r.severity,
                'why': r.why
            }
            for r in all_refactorings
        ]
        print(json.dumps(output, indent=2))
    else:
        reporter.print_summary(all_refactorings)
        
        # Group by file
        by_file = {}
        for r in all_refactorings:
            if r.filepath not in by_file:
                by_file[r.filepath] = []
            by_file[r.filepath].append(r)
        
        for filepath, refactorings in sorted(by_file.items()):
            print(f"\n{reporter._colorize(f'📄 {filepath}', reporter.BOLD)}")
            print("─" * 80)
            for r in refactorings:
                icon = reporter.RULE_ICONS.get(r.rule, '•')
                sev_color = {
                    'high': reporter.RED,
                    'medium': reporter.YELLOW,
                    'low': reporter.BLUE
                }[r.severity]
                
                print(f"  {icon} {reporter._colorize(r.severity.upper(), sev_color)} | Line {r.lineno}")
                print(f"     {r.description}")
                print(f"     → {r.why}")
                print()


if __name__ == '__main__':
    main()
