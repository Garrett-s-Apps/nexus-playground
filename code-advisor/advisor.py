#!/usr/bin/env python3
"""
Code Advisor - Turns metrics into actionable recommendations

Analyzes code complexity metrics and generates specific, practical
refactoring suggestions based on detected code smells and patterns.

Usage:
  python3 advisor.py [--source FILE] [--json] [--no-color]
  python3 advisor.py --help

Takes output from nexus analyze or from a JSON metrics file.
Generates human-readable or JSON recommendations.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional


class RecommendationEngine:
    """Generates recommendations based on code metrics"""
    
    # Thresholds for different issues
    COMPLEXITY_CRITICAL = 15
    COMPLEXITY_HIGH = 10
    COMPLEXITY_MODERATE = 6
    
    LOC_CRITICAL = 100
    LOC_HIGH = 50
    LOC_MODERATE = 25
    
    NESTING_CRITICAL = 5
    NESTING_HIGH = 4
    NESTING_MODERATE = 3
    
    def __init__(self):
        self.recommendations = []
    
    def _check_complexity(self, file_data: Dict[str, Any], filepath: str) -> Optional[Dict[str, Any]]:
        """Check complexity metrics and return recommendation if needed"""
        max_complexity = file_data.get('max_complexity', 0)
        avg_complexity = file_data.get('avg_complexity', 0)
        
        if max_complexity >= self.COMPLEXITY_CRITICAL:
            return {
                'severity': 'critical',
                'category': 'Complexity',
                'issue': f'Function with complexity {max_complexity} detected',
                'impact': 'Hard to test, understand, and maintain',
                'suggestion': 'Break function into smaller, focused functions. Extract conditional logic into helper functions.',
                'priority': 1,
                'file': filepath
            }
        elif max_complexity >= self.COMPLEXITY_HIGH:
            return {
                'severity': 'high',
                'category': 'Complexity',
                'issue': f'Function with complexity {max_complexity} is complex',
                'impact': 'Difficult to test thoroughly',
                'suggestion': 'Consider extracting branches into separate functions. Look for repeated conditionals.',
                'priority': 2,
                'file': filepath
            }
        elif max_complexity >= self.COMPLEXITY_MODERATE:
            return {
                'severity': 'moderate',
                'category': 'Complexity',
                'issue': f'Average function complexity {avg_complexity:.1f} is elevated',
                'impact': 'Makes code harder to reason about',
                'suggestion': 'Review functions with multiple if/elif chains. Consider simplifying logic.',
                'priority': 3,
                'file': filepath
            }
        return None
    
    def _check_file_size(self, file_data: Dict[str, Any], filepath: str) -> Optional[Dict[str, Any]]:
        """Check file size and return recommendation if needed"""
        code_lines = file_data.get('code_lines', 0)
        
        if code_lines >= self.LOC_CRITICAL:
            return {
                'severity': 'high',
                'category': 'Size',
                'issue': f'File is {code_lines} lines of code',
                'impact': 'Hard to navigate and test. High cognitive load.',
                'suggestion': 'Split into multiple modules. Group related functions together.',
                'priority': 2,
                'file': filepath
            }
        elif code_lines >= self.LOC_HIGH:
            return {
                'severity': 'moderate',
                'category': 'Size',
                'issue': f'File is {code_lines} lines of code',
                'impact': 'Getting large. Harder to maintain.',
                'suggestion': 'Consider splitting into 2-3 focused modules.',
                'priority': 3,
                'file': filepath
            }
        return None
    
    def _check_function_design(self, file_data: Dict[str, Any], filepath: str) -> Optional[Dict[str, Any]]:
        """Check function design and return recommendation if needed"""
        num_functions = file_data.get('num_functions', 0)
        code_lines = file_data.get('code_lines', 0)
        
        if num_functions <= 0:
            return None
        
        avg_lines_per_function = code_lines / num_functions
        
        if avg_lines_per_function > self.LOC_CRITICAL:
            return {
                'severity': 'high',
                'category': 'Function Design',
                'issue': f'Average function size is {avg_lines_per_function:.0f} lines',
                'impact': 'Functions doing too much. Difficult to unit test.',
                'suggestion': 'Extract smaller functions with single responsibilities.',
                'priority': 2,
                'file': filepath
            }
        elif avg_lines_per_function > self.LOC_HIGH:
            return {
                'severity': 'moderate',
                'category': 'Function Design',
                'issue': f'Average function size is {avg_lines_per_function:.0f} lines',
                'impact': 'Some functions could be simpler',
                'suggestion': 'Review larger functions. Extract helper functions.',
                'priority': 3,
                'file': filepath
            }
        return None
    
    def _check_nesting(self, file_data: Dict[str, Any], filepath: str) -> Optional[Dict[str, Any]]:
        """Check nesting depth and return recommendation if needed"""
        nesting_depth = file_data.get('max_nesting_depth', 0)
        
        if nesting_depth >= self.NESTING_CRITICAL:
            return {
                'severity': 'high',
                'category': 'Structure',
                'issue': f'Code has nesting depth of {nesting_depth}',
                'impact': 'Very hard to follow control flow',
                'suggestion': 'Extract nested blocks into separate functions. Use early returns to reduce nesting.',
                'priority': 1,
                'file': filepath
            }
        elif nesting_depth >= self.NESTING_MODERATE:
            return {
                'severity': 'moderate',
                'category': 'Structure',
                'issue': f'Code nesting depth is {nesting_depth}',
                'impact': 'Control flow is hard to follow',
                'suggestion': 'Use guard clauses and early returns. Extract nested logic.',
                'priority': 3,
                'file': filepath
            }
        return None
    
    def analyze_file(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for a single file"""
        filepath = file_data.get('filepath', 'unknown')
        recommendations = []
        
        # Check each category
        checks = [
            self._check_complexity(file_data, filepath),
            self._check_file_size(file_data, filepath),
            self._check_function_design(file_data, filepath),
            self._check_nesting(file_data, filepath)
        ]
        
        for rec in checks:
            if rec:
                recommendations.append(rec)
        
        return recommendations
    
    def analyze_metrics(self, metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze all files and generate recommendations"""
        all_recommendations = []
        
        for file_data in metrics:
            file_recs = self.analyze_file(file_data)
            all_recommendations.extend(file_recs)
        
        # Sort by priority
        all_recommendations.sort(key=lambda r: r['priority'])
        
        return all_recommendations


class RecommendationReporter:
    """Formats and displays recommendations"""
    
    # ANSI colors
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    SEVERITY_COLORS = {
        'critical': RED,
        'high': RED,
        'moderate': YELLOW,
        'info': BLUE
    }
    
    def __init__(self, use_color: bool = True):
        self.use_color = use_color
    
    def _colorize(self, text: str, color: str) -> str:
        """Add color to text if enabled"""
        if not self.use_color:
            return text
        return f"{color}{text}{self.RESET}"
    
    def _format_severity(self, severity: str) -> str:
        """Format severity indicator"""
        if not self.use_color:
            return severity.upper()
        
        icons = {
            'critical': '🔴',
            'high': '🔴',
            'moderate': '🟡',
            'info': '🔵'
        }
        color = self.SEVERITY_COLORS.get(severity, self.RESET)
        icon = icons.get(severity, '●')
        return f"{icon} {self._colorize(severity.upper(), color)}"
    
    def print_summary(self, recommendations: List[Dict[str, Any]]) -> None:
        """Print summary of recommendations"""
        if not recommendations:
            print(self._colorize("✅ No issues found. Code looks good!", self.GREEN))
            return
        
        critical = len([r for r in recommendations if r['severity'] == 'critical'])
        high = len([r for r in recommendations if r['severity'] == 'high'])
        moderate = len([r for r in recommendations if r['severity'] == 'moderate'])
        
        print()
        print(self._colorize("╔═══════════════════════════════════════╗", self.BOLD))
        print(self._colorize("║     CODE RECOMMENDATIONS REPORT       ║", self.BOLD))
        print(self._colorize("╚═══════════════════════════════════════╝", self.BOLD))
        print()
        
        if critical > 0:
            print(f"  {self._colorize('🔴 Critical', self.RED)}: {critical} issue{'s' if critical != 1 else ''}")
        if high > 0:
            print(f"  {self._colorize('🔴 High', self.RED)}: {high} issue{'s' if high != 1 else ''}")
        if moderate > 0:
            print(f"  {self._colorize('🟡 Moderate', self.YELLOW)}: {moderate} issue{'s' if moderate != 1 else ''}")
        
        print()
    
    def print_detailed(self, recommendations: List[Dict[str, Any]]) -> None:
        """Print detailed recommendations"""
        if not recommendations:
            print(self._colorize("✅ No recommendations. Code is clean!", self.GREEN))
            return
        
        self.print_summary(recommendations)
        
        # Group by file
        by_file = {}
        for rec in recommendations:
            file = rec.get('file', 'unknown')
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(rec)
        
        for filepath in sorted(by_file.keys()):
            print(f"\n📄 {self._colorize(filepath, self.BOLD)}")
            print("  " + "─" * 70)
            
            for rec in by_file[filepath]:
                severity_str = self._format_severity(rec['severity'])
                category = rec.get('category', 'General')
                issue = rec.get('issue', 'Unknown issue')
                impact = rec.get('impact', '')
                suggestion = rec.get('suggestion', '')
                
                print(f"\n  {severity_str} {category}")
                print(f"    Issue: {issue}")
                if impact:
                    print(f"    Impact: {impact}")
                if suggestion:
                    print(f"    → {suggestion}")
        
        print("\n" + "─" * 78)
        print(f"\n💡 Tip: Address critical issues first, then high, then moderate.")
        print(f"   Focus on complexity and size issues for the biggest impact.\n")
    
    def print_json(self, recommendations: List[Dict[str, Any]]) -> None:
        """Print recommendations as JSON"""
        output = {
            'total': len(recommendations),
            'by_severity': {
                'critical': len([r for r in recommendations if r['severity'] == 'critical']),
                'high': len([r for r in recommendations if r['severity'] == 'high']),
                'moderate': len([r for r in recommendations if r['severity'] == 'moderate']),
            },
            'recommendations': recommendations
        }
        print(json.dumps(output, indent=2))


class Advisor:
    """Main advisor class"""
    
    def __init__(self, use_color: bool = True):
        self.engine = RecommendationEngine()
        self.reporter = RecommendationReporter(use_color=use_color)
    
    def analyze_json_input(self) -> List[Dict[str, Any]]:
        """Read JSON metrics from stdin"""
        try:
            data = json.load(sys.stdin)
            if not isinstance(data, list):
                print("Error: Input must be a JSON array of metrics", file=sys.stderr)
                sys.exit(1)
            return data
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
            sys.exit(1)
    
    def analyze_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Read metrics from a file"""
        try:
            with open(filepath) as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("Error: File must contain a JSON array of metrics", file=sys.stderr)
                sys.exit(1)
            return data
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in file: {e}", file=sys.stderr)
            sys.exit(1)
    
    def run(self, args: argparse.Namespace) -> None:
        """Main execution"""
        # Read metrics
        if args.source:
            metrics = self.analyze_file(args.source)
        else:
            metrics = self.analyze_json_input()
        
        # Generate recommendations
        recommendations = self.engine.analyze_metrics(metrics)
        
        # Output
        if args.json:
            self.reporter.print_json(recommendations)
        else:
            self.reporter.print_detailed(recommendations)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        prog='advisor',
        description='Generate actionable code recommendations from complexity metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate recommendations from current metrics
  nexus analyze --json | python3 advisor.py
  
  # From a saved metrics file
  python3 advisor.py --source metrics.json
  
  # Export recommendations as JSON
  nexus analyze --json | python3 advisor.py --json > recommendations.json
  
  # Without colors (for logs/email)
  nexus analyze --json | python3 advisor.py --no-color
        """.strip()
    )
    
    parser.add_argument(
        '--source',
        help='Read metrics from JSON file instead of stdin'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output recommendations as JSON'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    args = parser.parse_args()
    
    advisor = Advisor(use_color=not args.no_color)
    advisor.run(args)


if __name__ == '__main__':
    main()
