# Code Refactoring Engine

Automatically analyze Python code and identify refactoring opportunities.

This tool goes beyond metrics and recommendations—it finds specific, actionable refactoring opportunities in your code and explains why they matter.

## Features

- **Complexity Analysis** - Find functions with high cyclomatic complexity
- **Size Analysis** - Identify overly large functions and files
- **Nesting Analysis** - Detect deeply nested code that's hard to follow
- **Duplication Detection** - Find similar code patterns that could be consolidated
- **Style Checking** - Flag unclear naming and style issues
- **Severity Classification** - Prioritize refactoring by impact (high/medium/low)

## Installation

No dependencies! Uses only Python's standard library.

```bash
python3 code-refactor/refactor.py --help
```

## Usage

### Analyze a single file

```bash
python3 code-refactor/refactor.py --file mycode.py
```

### Analyze a directory

```bash
python3 code-refactor/refactor.py --dir src/
```

### Get JSON output

```bash
python3 code-refactor/refactor.py --dir src/ --json
```

### Disable colored output

```bash
python3 code-refactor/refactor.py --file mycode.py --no-color
```

## Example Output

```
╔════════════════════════════════════════╗
║    REFACTORING OPPORTUNITIES REPORT     ║
╚════════════════════════════════════════╝

  🟡 Medium Priority: 4
  🔵 Low Priority: 18

📄 tracker.py
────────────────────────────────────────────────────────────────────────────────
  🔪 MEDIUM | Line 36
     Function 'load_snapshots' has complexity 10
     → High complexity (10) makes function hard to test and maintain. Consider extracting conditional branches into helper functions.

  ⬇️ MEDIUM | Line 36
     Function 'load_snapshots' has nesting depth 5
     → Deep nesting (5) makes control flow hard to follow. Use early returns and extract nested blocks into functions.

  🔪 MEDIUM | Line 303
     Function 'main' is 73 lines
     → Function is 73 lines long. Extract logical sections into separate helper functions.
```

## Refactoring Rules

### 🔪 Extract Function
When a function is too complex or too long, extract parts of it into separate helper functions.

**Triggers:**
- Function complexity ≥ 10
- Function length ≥ 50 lines

**Why:** Small, focused functions are easier to test, understand, and reuse.

### ⬇️ Reduce Nesting
Deeply nested code is hard to follow. Use early returns or extract into functions.

**Triggers:**
- Nesting depth ≥ 4

**Why:** Each level of nesting adds to cognitive load. Early returns and extracted functions flatten the structure.

### ↩️ Early Returns
Use early returns to reduce nesting and simplify control flow.

**Example:**
```python
# Before: Deep nesting
def process(item):
    if item.is_valid():
        if item.is_ready():
            if item.needs_processing():
                # do something
                pass

# After: Early returns
def process(item):
    if not item.is_valid():
        return
    if not item.is_ready():
        return
    if not item.needs_processing():
        return
    # do something
```

### 📦 Extract Constant
Similar code patterns should be consolidated into shared functions or constants.

**Why:** Reduces duplication and makes changes easier to manage.

### 📝 Improve Naming
Function names should be descriptive and clear.

**Triggers:**
- Single-letter function names (except `_`)
- Unclear abbreviations

**Why:** Good naming makes code self-documenting and easier to navigate.

## Integration with NEXUS Toolkit

The refactoring engine complements the other NEXUS tools:

1. **Complexity Analyzer** → Get metrics on code
2. **Code Advisor** → Get recommendations for improvement
3. **Refactoring Engine** → Find specific refactoring opportunities
4. **CodeStats** → Understand team activity
5. **Metrics Tracker** → Monitor trends over time

Typical workflow:

```bash
# 1. Analyze code
nexus analyze --dir src/ --json | tee metrics.json

# 2. Get recommendations
cat metrics.json | nexus advise

# 3. Find refactoring opportunities
nexus refactor --dir src/

# 4. Review and apply changes manually based on suggestions
```

## How It Works

The refactoring engine uses Python's `ast` (Abstract Syntax Tree) module to:

1. Parse Python source code into an AST
2. Walk the AST and collect metrics on functions
3. Apply a series of analysis rules to identify issues
4. Report findings with explanation and severity

This approach is safe—it never modifies code automatically, only identifies opportunities for you to address.

## Thresholds

These thresholds trigger refactoring suggestions:

- **Complexity ≥ 10** - High priority for extraction
- **Function length ≥ 50 lines** - Should be split into smaller functions
- **Nesting depth ≥ 4** - Should use early returns or extraction
- **Duplicate code patterns** - Should be consolidated
- **Single-letter names** - Should be clarified

You can adjust these thresholds by modifying the constants in `RefactoringEngine`.

## Limitations

- Does not apply refactorings automatically (by design—you review and approve)
- Simple duplication detection (looks for exact line matches)
- Does not analyze type hints or docstrings
- Works with Python files only

## Future Enhancements

- Auto-apply safe refactorings (extract constant, improve naming)
- Generate refactored code with full diffs
- Integration with code formatters and linters
- Type-aware analysis
- Performance analysis

## See Also

- **Code Complexity Analyzer** - Get detailed metrics on code
- **Code Advisor** - Turn metrics into actionable recommendations
- **Metrics Tracker** - Monitor trends over time
