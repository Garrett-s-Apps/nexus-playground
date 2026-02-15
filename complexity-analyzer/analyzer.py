#!/usr/bin/env python3
"""
Code Complexity Analyzer - A tool to analyze Python code complexity and quality
"""

import ast
import os
import sys
import argparse
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class FunctionMetrics:
    """Metrics for a single function or method"""
    name: str
    lines: int
    complexity: int
    parameters: int
    max_nesting: int
    has_docstring: bool
    line_number: int


@dataclass
class FileMetrics:
    """Metrics for a single file"""
    filepath: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    num_functions: int
    num_classes: int
    num_imports: int
    avg_complexity: float
    max_complexity: int


class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor to calculate cyclomatic complexity"""
    
    def __init__(self):
        self.complexity = 1
        self.nesting_level = 0
        self.max_nesting = 0
        
    def visit_If(self, node):
        self.complexity += 1
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
        self.generic_visit(node)
        self.nesting_level -= 1
        
    def visit_For(self, node):
        self.complexity += 1
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
        self.generic_visit(node)
        self.nesting_level -= 1
        
    def visit_While(self, node):
        self.complexity += 1
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
        self.generic_visit(node)
        self.nesting_level -= 1
        
    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)
        
    def visit_Compare(self, node):
        self.complexity += len(node.ops)
        self.generic_visit(node)


class CodeAnalyzer:
    """Main code analyzer class"""
    
    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {
            'complexity': 10,
            'function_lines': 50,
            'parameters': 5,
            'nesting': 4
        }
        
    def analyze_function(self, node, source_lines) -> FunctionMetrics:
        """Analyze a single function or method"""
        visitor = ComplexityVisitor()
        visitor.visit(node)
        
        # Calculate lines
        start_line = node.lineno
        end_line = node.end_lineno or start_line
        lines = end_line - start_line + 1
        
        # Count parameters
        params = len(node.args.args) + len(node.args.posonlyargs) + len(node.args.kwonlyargs)
        if node.args.vararg:
            params += 1
        if node.args.kwarg:
            params += 1
            
        # Check for docstring
        has_docstring = (isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Constant) and
                        isinstance(node.body[0].value.value, str)) if node.body else False
        
        return FunctionMetrics(
            name=node.name,
            lines=lines,
            complexity=visitor.complexity,
            parameters=params,
            max_nesting=visitor.max_nesting,
            has_docstring=has_docstring,
            line_number=start_line
        )
    
    def analyze_file(self, filepath: Path) -> Optional[FileMetrics]:
        """Analyze a single Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            return None
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"Syntax error in {filepath}: {e}", file=sys.stderr)
            return None
        
        # Count line types
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#'):
                comment_lines += 1
            else:
                code_lines += 1
        
        # Analyze functions and classes
        functions = []
        classes = 0
        imports = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(self.analyze_function(node, lines))
            elif isinstance(node, ast.ClassDef):
                classes += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports += 1
        
        # Calculate aggregate metrics
        complexities = [f.complexity for f in functions]
        avg_complexity = sum(complexities) / len(complexities) if complexities else 0
        max_complexity = max(complexities) if complexities else 0
        
        return FileMetrics(
            filepath=str(filepath),
            total_lines=len(lines),
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            num_functions=len(functions),
            num_classes=classes,
            num_imports=imports,
            avg_complexity=round(avg_complexity, 2),
            max_complexity=max_complexity
        )
    
    def analyze_directory(self, directory: Path) -> List[FileMetrics]:
        """Analyze all Python files in a directory"""
        results = []
        for filepath in directory.rglob('*.py'):
            # Skip virtual environments and common non-code directories
            if any(part in filepath.parts for part in ['.venv', 'venv', '__pycache__', '.git']):
                continue
            result = self.analyze_file(filepath)
            if result:
                results.append(result)
        return sorted(results, key=lambda x: x.max_complexity, reverse=True)


class Reporter:
    """Format and display analysis results"""
    
    # ANSI color codes
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    def __init__(self, thresholds, use_colors=True):
        self.thresholds = thresholds
        self.use_colors = use_colors
        
    def color(self, text, color_code):
        """Apply color if enabled"""
        if self.use_colors:
            return f"{color_code}{text}{self.RESET}"
        return text
    
    def get_complexity_color(self, complexity):
        """Get color based on complexity threshold"""
        if complexity > self.thresholds['complexity'] * 1.5:
            return self.RED
        elif complexity > self.thresholds['complexity']:
            return self.YELLOW
        return self.GREEN
    
    def print_summary(self, all_metrics: List[FileMetrics]):
        """Print summary report"""
        self._print_header()
        self._print_aggregate_stats(all_metrics)
        self._print_complex_files(all_metrics)
        print(f"{self.color('─' * 80, self.CYAN)}\n")
    
    def _print_header(self):
        """Print report header"""
        print(f"\n{self.color('╔' + '═' * 78 + '╗', self.CYAN)}")
        print(f"{self.color('║', self.CYAN)} {self.color('CODE COMPLEXITY ANALYSIS REPORT', self.BOLD):<76} {self.color('║', self.CYAN)}")
        print(f"{self.color('╚' + '═' * 78 + '╝', self.CYAN)}\n")
    
    def _print_aggregate_stats(self, all_metrics: List[FileMetrics]):
        """Print aggregate statistics"""
        total_files = len(all_metrics)
        total_lines = sum(m.total_lines for m in all_metrics)
        total_functions = sum(m.num_functions for m in all_metrics)
        total_classes = sum(m.num_classes for m in all_metrics)
        avg_file_complexity = sum(m.max_complexity for m in all_metrics) / total_files if total_files else 0
        
        print(f"{self.color('📊 Overall Statistics:', self.BOLD)}")
        print(f"  Files analyzed: {total_files}")
        print(f"  Total lines: {total_lines:,}")
        print(f"  Functions: {total_functions}")
        print(f"  Classes: {total_classes}")
        print(f"  Avg file complexity: {self.color(f'{avg_file_complexity:.1f}', self.get_complexity_color(avg_file_complexity))}")
    
    def _print_complex_files(self, all_metrics: List[FileMetrics]):
        """Print top complex files"""
        print(f"\n{self.color('⚠️  Most Complex Files:', self.BOLD)}")
        for i, metrics in enumerate(all_metrics[:5], 1):
            self._print_file_complexity_indicator(i, metrics)
    
    def _print_file_complexity_indicator(self, index: int, metrics: FileMetrics):
        """Print a single file complexity indicator"""
        status = self._get_complexity_indicator(metrics.max_complexity)
        filepath = Path(metrics.filepath).name
        print(f"  {index}. {status} {filepath:<40} complexity: {metrics.max_complexity}")
    
    def _get_complexity_indicator(self, complexity: int) -> str:
        """Get visual indicator for complexity level"""
        if complexity > self.thresholds['complexity'] * 1.5:
            return self.color('🔴', self.RED)
        elif complexity > self.thresholds['complexity']:
            return self.color('🟡', self.YELLOW)
        return self.color('🟢', self.GREEN)
    
    def print_file_details(self, metrics: FileMetrics):
        """Print detailed report for a single file"""
        print(f"{self.color('FILE:', self.BOLD)} {Path(metrics.filepath).name}")
        print(f"  Path: {metrics.filepath}")
        print(f"  Lines: {metrics.total_lines} (code: {metrics.code_lines}, comments: {metrics.comment_lines}, blank: {metrics.blank_lines})")
        print(f"  Functions: {metrics.num_functions} | Classes: {metrics.num_classes}")
        print(f"  Complexity: max={self.color(str(metrics.max_complexity), self.get_complexity_color(metrics.max_complexity))}, avg={metrics.avg_complexity}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Python code complexity and quality metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze current directory
  python3 analyzer.py
  
  # Analyze specific file
  python3 analyzer.py --file script.py
  
  # Analyze specific directory
  python3 analyzer.py --dir /path/to/code
  
  # Output as JSON
  python3 analyzer.py --json
  
  # Disable colors
  python3 analyzer.py --no-color
        """
    )
    
    parser.add_argument('--file', type=str, help='Analyze a single Python file')
    parser.add_argument('--dir', type=str, default='.', help='Analyze a directory (default: current)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    analyzer = CodeAnalyzer()
    reporter = Reporter(analyzer.thresholds, use_colors=not args.no_color)
    
    if args.file:
        # Analyze single file
        metrics = analyzer.analyze_file(Path(args.file))
        if metrics:
            if args.json:
                print(json.dumps(asdict(metrics), indent=2))
            else:
                reporter.print_file_details(metrics)
    else:
        # Analyze directory
        all_metrics = analyzer.analyze_directory(Path(args.dir))
        if all_metrics:
            if args.json:
                data = {
                    'files': [asdict(m) for m in all_metrics],
                    'summary': {
                        'total_files': len(all_metrics),
                        'total_lines': sum(m.total_lines for m in all_metrics),
                        'avg_max_complexity': round(sum(m.max_complexity for m in all_metrics) / len(all_metrics), 2)
                    }
                }
                print(json.dumps(data, indent=2))
            else:
                reporter.print_summary(all_metrics)
                print(f"{reporter.color('🔍 Detailed Analysis of Most Complex Files:', reporter.BOLD)}\n")
                for metrics in all_metrics[:5]:
                    reporter.print_file_details(metrics)
        else:
            print("No Python files found", file=sys.stderr)


if __name__ == '__main__':
    main()
