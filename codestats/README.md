# 📊 CodeStats

Analyze and visualize your git repository statistics. Understand development patterns, contributor activity, and project evolution.

## Features

- **Commit Analysis**: Full commit history parsing with detailed statistics
- **Contributor Insights**: Top authors, commit counts, code changes
- **Activity Patterns**: Commits by day of week, hour of day
- **Code Metrics**: Total insertions, deletions, files changed
- **Beautiful Output**: Color-coded terminal reports
- **JSON Export**: Export data for CI/CD and programmatic use
- **No Dependencies**: Uses only Python standard library (3.8+)

## Installation

Just download `stats.py` or clone this repository. Requires git to be installed.

```bash
# Make it executable
chmod +x stats.py
```

## Usage

### Analyze Current Repository
```bash
python3 stats.py
```

### Analyze a Specific Repository
```bash
python3 stats.py --repo /path/to/repo
```

### Export as JSON
```bash
python3 stats.py --json > repo-stats.json
```

### Disable Colors
```bash
python3 stats.py --no-color
```

## Output Example

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                   GIT REPOSITORY STATISTICS                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 Repository Overview:
  Total commits: 127
  Unique authors: 5
  Total insertions: +12,847
  Deletions: -3,421
  Date range: 2024-01-15 to 2024-02-15

👥 Top Contributors:
   1. Alice Dev                   ██████████████████████████ 52 commits ( 40.9%)
   2. Bob Smith                   ███████████████████        42 commits ( 33.1%)
   3. Carol Lee                   ███████████               28 commits ( 22.0%)
   4. Dave Johnson                ██                         4 commits (  3.1%)
   5. Eve Wilson                  █                          1 commits (  0.8%)

📅 Activity by Day of Week:
  Monday       ██████████████████████████ 23 commits
  Tuesday      ███████████████████████████ 28 commits
  Wednesday    ███████████████████████    25 commits
  Thursday     █████████████████████████  24 commits
  Friday       ██████████████████████     22 commits
  Saturday     ████████                   4 commits
  Sunday       ██                         1 commits

📈 Code Change Intensity:
  Additions:  ███████████████ 78.9%
  Deletions:  ████ 21.1%

────────────────────────────────────────────────────────────────────────────────
```

## Metrics Explained

### Total Commits
The complete commit history in the repository.

### Unique Authors
The number of distinct contributors (by git author name).

### Insertions & Deletions
Total lines added and removed across all commits. A high insertion rate relative to deletions indicates a growing codebase. High deletions might indicate refactoring or cleanup.

### Activity Patterns
- **By Day of Week**: Helps identify team's typical work schedule
- **By Hour**: Shows when commits are typically made
- **Date Range**: How long the project has been active

### Top Contributors
Ranked by commit count. Percentage shows their share of total commits.

## Use Cases

1. **Team Analytics**: Understand contributor activity and patterns
2. **Project Health**: Track development momentum and participation
3. **Onboarding**: See project timeline and main contributors
4. **Reporting**: Export JSON for dashboards and reports
5. **Team Dynamics**: Identify quiet periods, vacation times, surge periods

## JSON Output Format

```json
{
  "commits": 127,
  "authors": 5,
  "top_authors": [
    {
      "name": "Alice Dev",
      "commits": 52,
      "insertions": 5420,
      "deletions": 1200,
      "files_changed": 148,
      "first_commit": "2024-01-15 10:23:45+00:00",
      "last_commit": "2024-02-15 14:12:33+00:00"
    }
  ],
  "activity_by_day": {
    "Monday": 23,
    "Tuesday": 28,
    "Wednesday": 25
  }
}
```

## Performance

- Analyzes repositories with thousands of commits in seconds
- Minimal memory usage
- Efficient git command piping

## Requirements

- Python 3.8+
- git (must be installed and in PATH)

## Limitations

- Requires write-free access (just reads git history)
- Respects `.gitignore` and other git configurations
- Some data (like email) is not included for privacy
- Author identification is based on git author name/email

## Tips

### Analyzing Large Repositories
For very large repositories, the initial load might take some time as it processes all commits. Subsequent runs are cached if you're analyzing the same repo.

### For CI/CD Integration
Use the `--json` flag to export data programmatically:
```bash
python3 stats.py --json | jq '.commits'
```

### Comparing Multiple Repositories
Run CodeStats on multiple repos and compare the JSON output:
```bash
python3 stats.py --repo /repo1 --json > stats1.json
python3 stats.py --repo /repo2 --json > stats2.json
# Compare with jq or your preferred tool
```

## License

MIT - Use freely in any project

## Contributing

Issues and PRs welcome! Found a bug or want a feature? Let us know.
