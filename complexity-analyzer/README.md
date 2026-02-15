# 🔍 Code Complexity Analyzer

A powerful CLI tool to analyze Python code for complexity metrics, code quality indicators, and maintainability issues.

## Features

- **Cyclomatic Complexity Analysis**: Detects complex control flow in functions
- **Code Metrics**: Lines of code, function count, class count, import analysis
- **Quality Indicators**: Code organization, nesting depth, parameter counts
- **Beautiful Terminal Output**: Color-coded complexity warnings
- **JSON Export**: Export metrics for CI/CD integration and programmatic use
- **No Dependencies**: Uses only Python standard library (3.8+)

## Installation

Just download `analyzer.py` or clone this repository. No dependencies to install!

```bash
# Make it executable
chmod +x analyzer.py
```

## Usage

### Analyze Current Directory
```bash
python3 analyzer.py
```

### Analyze a Specific File
```bash
python3 analyzer.py --file mycode.py
```

### Analyze a Specific Directory
```bash
python3 analyzer.py --dir /path/to/code
```

### Export as JSON
```bash
python3 analyzer.py --json > metrics.json
```

### Disable Colored Output
```bash
python3 analyzer.py --no-color
```

## Output Examples

### Summary Report
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                  CODE COMPLEXITY ANALYSIS REPORT                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 Overall Statistics:
  Files analyzed: 12
  Total lines: 4,287
  Functions: 42
  Classes: 8
  Avg file complexity: 8.5

⚠️  Most Complex Files:
  1. 🔴 analytics.py                          complexity: 18
  2. 🟡 processor.py                          complexity: 13
  3. 🟡 parser.py                             complexity: 12
  4. 🟢 utils.py                              complexity: 7
  5. 🟢 main.py                               complexity: 6

────────────────────────────────────────────────────────────────────────────────

🔍 Detailed Analysis of Most Complex Files:

FILE: analytics.py
  Path: /workspace/src/analytics.py
  Lines: 245 (code: 198, comments: 32, blank: 15)
  Functions: 6 | Classes: 2
  Complexity: max=18, avg=9.2
```

## Understanding the Metrics

### Cyclomatic Complexity
A measure of code complexity based on the number of independent paths through code:
- **1-5**: Simple, low risk
- **6-10**: Moderate complexity, some risk
- **11-20**: High complexity, significant risk
- **20+**: Very high complexity, refactor recommended

Color coding:
- 🟢 **Green**: Acceptable complexity
- 🟡 **Yellow**: Elevated complexity, consider refactoring
- 🔴 **Red**: High complexity, should refactor

### Lines of Code
- Counts actual code lines vs comments vs blank lines
- Helps identify files that might benefit from modularization

### Functions & Classes
- Shows code organization
- High function count might indicate tight cohesion
- High class count indicates modular design

## Use Cases

1. **Code Review**: Identify complex functions that need attention
2. **Refactoring**: Prioritize files and functions for improvement
3. **Onboarding**: Help new developers understand code complexity
4. **CI/CD**: Export JSON and fail builds if complexity exceeds thresholds
5. **Technical Debt Tracking**: Monitor complexity trends over time

## JSON Output Format

```json
[
  {
    "filepath": "/workspace/complexity-analyzer/analyzer.py",
    "total_lines": 287,
    "code_lines": 245,
    "comment_lines": 18,
    "blank_lines": 24,
    "num_functions": 8,
    "num_classes": 2,
    "num_imports": 4,
    "avg_complexity": 4.5,
    "max_complexity": 8
  }
]
```

## Performance

- Analyzes typical Python projects in milliseconds
- Handles large codebases (10,000+ files) efficiently
- Minimal memory footprint

## Limitations

- Only analyzes Python code (*.py files)
- Does not analyze compiled code or non-Python files
- Complexity is based on cyclomatic complexity, which is one of many metrics

## License

MIT - Use freely in any project

## Contributing

Found a bug or want to add a feature? Issues and pull requests welcome!
