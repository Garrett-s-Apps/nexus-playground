#!/usr/bin/env python3
"""
Test Generator - Creates test stubs for complex functions

Analyzes code metrics to identify complex functions that need testing,
then generates pytest test stubs with appropriate test cases based on
the function's complexity.

Usage:
  python3 generator.py [--source FILE] [--target DIR] [--no-color]
  python3 generator.py --help

Takes output from nexus analyze or from a JSON metrics file.
Generates test file stubs for functions with high complexity.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast


class TestGeneratorEngine:
    """Generates test stubs for complex functions"""
    
    # Complexity threshold for generating tests
    MIN_COMPLEXITY_FOR_TESTS = 5
    
    def __init__(self):
        self.test_files = {}
    
    def generate_test_stub(self, file_path: str, metrics: Dict[str, Any]) -> Optional[str]:
        """Generate test file content for a Python file"""
        filepath = Path(file_path)
        
        if not filepath.suffix == '.py':
            return None
        
        max_complexity = metrics.get('max_complexity', 0)
        
        # Only generate tests for sufficiently complex files
        if max_complexity < self.MIN_COMPLEXITY_FOR_TESTS:
            return None
        
        # Read the source file to extract function names
        try:
            with open(filepath) as f:
                source_code = f.read()
            tree = ast.parse(source_code)
        except:
            return None
        
        # Extract function and class information
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip magic methods and private methods for now
                if not node.name.startswith('_'):
                    functions.append(node.name)
        
        if not functions:
            return None
        
        # Generate test file
        test_module = filepath.stem
        test_content = self._generate_test_content(test_module, functions, max_complexity)
        
        return test_content
    
    def _generate_test_content(self, module_name: str, functions: List[str], complexity: int) -> str:
        """Generate test file content"""
        # Determine number of test cases based on complexity
        num_test_cases = min(complexity // 2 + 1, 10)  # 1-10 test cases
        
        imports = f"""\"\"\"
Tests for {module_name} module.

This test file was automatically generated based on code complexity analysis.
Add more specific test cases based on your module's actual behavior.
\"\"\"

import pytest
from {module_name} import {', '.join(functions[:5] if len(functions) > 5 else functions)}
"""
        
        test_cases = []
        for func_name in functions[:5]:  # Generate tests for first 5 functions
            test_cases.append(self._generate_function_tests(func_name, num_test_cases))
        
        return imports + "\n\n" + "\n\n".join(test_cases)
    
    def _generate_function_tests(self, func_name: str, num_cases: int) -> str:
        """Generate test cases for a specific function"""
        test_stubs = []
        
        for i in range(num_cases):
            test_stub = f"""def test_{func_name}_case_{i + 1}():
    \"\"\"
    Test {func_name} with test case {i + 1}.
    
    TODO: Add specific test inputs and assertions.
    \"\"\"
    # Arrange
    # TODO: Set up test data
    
    # Act
    # result = {func_name}(...)
    
    # Assert
    # assert result == expected_value
    pytest.skip("Implement test case {i + 1}")"""
            test_stubs.append(test_stub)
        
        return "\n\n".join(test_stubs)
    
    def analyze_metrics(self, metrics: List[Dict[str, Any]]) -> Dict[str, str]:
        """Analyze all files and generate test stubs"""
        test_files = {}
        
        for file_data in metrics:
            filepath = file_data.get('filepath', '')
            test_content = self.generate_test_stub(filepath, file_data)
            
            if test_content:
                # Generate test file path
                source_path = Path(filepath)
                test_path = f"tests/test_{source_path.stem}.py"
                test_files[test_path] = test_content
        
        return test_files


class TestGeneratorReporter:
    """Formats and displays test generation results"""
    
    # ANSI colors
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def __init__(self, use_color: bool = True):
        self.use_color = use_color
    
    def _colorize(self, text: str, color: str) -> str:
        """Add color to text if enabled"""
        if not self.use_color:
            return text
        return f"{color}{text}{self.RESET}"
    
    def print_summary(self, test_files: Dict[str, str]) -> None:
        """Print summary of generated test files"""
        if not test_files:
            print(self._colorize("ℹ️  No test files generated (no complex functions found)", self.BLUE))
            return
        
        print()
        print(self._colorize("╔═══════════════════════════════════════╗", self.BOLD))
        print(self._colorize("║       TEST GENERATION SUMMARY         ║", self.BOLD))
        print(self._colorize("╚═══════════════════════════════════════╝", self.BOLD))
        print()
        
        print(f"  📝 Test files to create: {len(test_files)}")
        print()
        
        for test_path in sorted(test_files.keys()):
            lines = test_files[test_path].count('\n')
            print(f"    ✓ {self._colorize(test_path, self.GREEN)}")
            print(f"      {lines} lines of test stubs")
        
        print()
        print("  Next steps:")
        print("    1. Review the generated test files")
        print("    2. Replace pytest.skip() with actual test implementations")
        print("    3. Add assertions based on function behavior")
        print("    4. Run: pytest tests/")
        print()
    
    def print_json(self, test_files: Dict[str, str]) -> None:
        """Print test files as JSON"""
        output = {
            'total': len(test_files),
            'test_files': test_files
        }
        print(json.dumps(output, indent=2))
    
    def print_files(self, test_files: Dict[str, str]) -> None:
        """Print detailed file contents"""
        if not test_files:
            print(self._colorize("ℹ️  No test files generated", self.BLUE))
            return
        
        self.print_summary(test_files)
        
        for test_path in sorted(test_files.keys()):
            print(f"\n{'='*78}")
            print(f"📄 {self._colorize(test_path, self.BOLD)}")
            print('='*78)
            print(test_files[test_path])
            print()


class TestGenerator:
    """Main test generator class"""
    
    def __init__(self, use_color: bool = True, target_dir: Optional[str] = None):
        self.engine = TestGeneratorEngine()
        self.reporter = TestGeneratorReporter(use_color=use_color)
        self.target_dir = Path(target_dir) if target_dir else None
    
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
    
    def write_test_files(self, test_files: Dict[str, str]) -> None:
        """Write test files to disk"""
        if not test_files:
            return
        
        target_dir = self.target_dir or Path.cwd()
        
        for test_path, content in test_files.items():
            file_path = target_dir / test_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Don't overwrite existing files
            if file_path.exists():
                print(f"⚠️  Skipped {test_path} (file already exists)", file=sys.stderr)
                continue
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"✓ Created {test_path}")
    
    def run(self, args: argparse.Namespace) -> None:
        """Main execution"""
        # Read metrics
        if args.source:
            metrics = self.analyze_file(args.source)
        else:
            metrics = self.analyze_json_input()
        
        # Generate test files
        test_files = self.engine.analyze_metrics(metrics)
        
        # Output
        if args.json:
            self.reporter.print_json(test_files)
        elif args.write:
            self.write_test_files(test_files)
        else:
            self.reporter.print_files(test_files)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        prog='test-generator',
        description='Generate test stubs for complex functions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate test stubs from current metrics
  nexus analyze --json | python3 generator.py
  
  # From a saved metrics file
  python3 generator.py --source metrics.json
  
  # Write test files to disk
  nexus analyze --json | python3 generator.py --write
  
  # Export test files as JSON
  nexus analyze --json | python3 generator.py --json > test-files.json
  
  # Without colors
  nexus analyze --json | python3 generator.py --no-color
        """.strip()
    )
    
    parser.add_argument(
        '--source',
        help='Read metrics from JSON file instead of stdin'
    )
    parser.add_argument(
        '--write',
        action='store_true',
        help='Write test files to disk (in tests/ directory)'
    )
    parser.add_argument(
        '--target',
        default='.',
        help='Target directory for test files (default: current directory)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output test files as JSON'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    args = parser.parse_args()
    
    generator = TestGenerator(use_color=not args.no_color, target_dir=args.target)
    generator.run(args)


if __name__ == '__main__':
    main()
