# 📊 Metrics Tracker

Track code quality and repository metrics over time. Compare current metrics to historical baselines, identify trends, and monitor regressions.

## Features

- **Snapshot Management**: Save metrics snapshots at different points in time
- **Trend Analysis**: Compare current metrics to previous snapshots
- **History Tracking**: View how metrics have evolved over time
- **Regression Detection**: Identify when code quality is degrading
- **JSON Integration**: Works with output from both `analyze` and `stats` tools
- **Beautiful Reports**: Color-coded trend indicators and history views

## Installation

Copy `tracker.py` to your project or use from the NEXUS toolkit:

```bash
chmod +x tracker.py
```

## Usage

### Save Current Metrics

```bash
# Save code complexity snapshot
nexus analyze --json | python3 tracker.py save --source analyze

# Save repository stats snapshot
nexus stats --json | python3 tracker.py save --source stats

# With commit association (optional)
nexus analyze --json | python3 tracker.py save --source analyze --commit abc123def456
```

### Show Trend vs. Previous Snapshot

```bash
# Compare current code to previous version
nexus analyze --json | python3 tracker.py show-trend --source analyze

# Compare current repository to previous state
nexus stats --json | python3 tracker.py show-trend --source stats
```

### View History

```bash
# See history of code complexity changes
python3 tracker.py history --source analyze

# See history of repository activity
python3 tracker.py history --source stats
```

## Typical Workflow

```bash
# 1. Save baseline metrics
nexus analyze --json | python3 tracker.py save --source analyze
nexus stats --json | python3 tracker.py save --source stats

# ... (make changes to code)

# 2. Check for regressions
nexus analyze --json | python3 tracker.py show-trend --source analyze
nexus stats --json | python3 tracker.py show-trend --source stats

# 3. View overall trends
python3 tracker.py history --source analyze
python3 tracker.py history --source stats
```

## Example Output

### Complexity Trend Report

```
📊 Code Complexity Trend:
  Status: WARNING
  Max Complexity: 15 ↑ (was 12)
    Change: +3 (+25.0%)
  Avg Complexity: 5.2 ↑ (was 4.8)
    Change: +0.4 (+8.3%)

📈 Recent History:
  1. 2024-02-14T09:30:15  max=12 avg=4.8
  2. 2024-02-14T14:22:41  max=13 avg=5.0
  3. 2024-02-15T10:15:33  max=15 avg=5.2
```

### Contributor Trend Report

```
👥 Contributor Activity Trend:
  Status: ACTIVE
  Recent Commits: 23 ↑ (was 18)
    Change: +5
  Active Authors: 4 ↓ (was 5)
    Change: -1

📈 Recent History:
  1. 2024-02-14T09:30:15  commits=18 authors=5
  2. 2024-02-14T14:22:41  commits=20 authors=5
  3. 2024-02-15T10:15:33  commits=23 authors=4
```

## Output Files

Snapshots are stored in `.metrics/` directory by default:

```
.metrics/
├── 2024-02-14T09-30-15-analyze.json
├── 2024-02-14T09-30-15-stats.json
├── 2024-02-14T14-22-41-analyze.json
├── 2024-02-14T14-22-41-stats.json
└── 2024-02-15T10-15-33-analyze.json
```

Filenames include:
- **Timestamp**: ISO format with colons replaced by hyphens
- **Source**: Either `analyze` or `stats`
- **Commit hash** (optional): If provided with `--commit` flag

## Status Indicators

### Complexity Analysis

- 🟢 **GOOD**: Complexity decreased or stayed low
- 🟡 **WARNING**: Complexity increased slightly (0-2 points)
- 🔴 **BAD**: Complexity increased significantly (>2 points)

### Contributor Activity

- 🟢 **ACTIVE**: Commits are increasing
- 🟡 **STABLE**: Commit activity unchanged
- 🔴 **IDLE**: Commit activity decreasing

### Trend Arrows

- ↑ **Increasing** - metric went up (color indicates if good or bad)
- ↓ **Decreasing** - metric went down (color indicates if good or bad)
- → **Unchanged** - metric stayed the same

## Use Cases

### Preventing Code Quality Regressions

```bash
# CI/CD: Fail build if complexity increased too much
./nexus analyze --json | python3 tracker.py show-trend --source analyze 2>&1 | grep -q "BAD" && exit 1
```

### Monitoring Team Productivity

```bash
# Daily/weekly reports of commit activity
./nexus stats --json | python3 tracker.py show-trend --source stats
```

### Tracking Refactoring Efforts

```bash
# Before refactoring
./nexus analyze --json | python3 tracker.py save --source analyze --commit before-refactor

# After refactoring
./nexus analyze --json | python3 tracker.py show-trend --source analyze
```

### Long-term Project Health

```bash
# Archive metrics weekly/monthly
./nexus analyze --json | python3 tracker.py save --source analyze
./nexus stats --json | python3 tracker.py save --source stats

# Review trends
python3 tracker.py history --source analyze
python3 tracker.py history --source stats
```

## Command Reference

```bash
# Save a snapshot
python3 tracker.py save --source {analyze|stats} [--commit HASH] [--dir DIR]

# Show trend compared to last snapshot
python3 tracker.py show-trend --source {analyze|stats} [--dir DIR] [--no-color]

# Show snapshot history
python3 tracker.py history --source {analyze|stats} [--dir DIR] [--no-color]
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `command` | - | `save`, `show-trend`, or `history` |
| `--source` | - | `analyze` (code metrics) or `stats` (git metrics) |
| `--commit` | - | Commit hash to associate with snapshot |
| `--dir` | `.metrics` | Directory for storing snapshots |
| `--no-color` | - | Disable colored output |

## Requirements

- Python 3.8+
- Input from `nexus analyze --json` or `nexus stats --json`
- No external dependencies

## Tips

### Automating Snapshot Collection

```bash
# Create a shell script to run at intervals
#!/bin/bash
TRACKER="python3 /path/to/tracker.py"
NEXUS="/path/to/nexus"

$NEXUS analyze --json | $TRACKER save --source analyze
$NEXUS stats --json | $TRACKER save --source stats
```

### Storing in Git

```bash
# Track snapshots in version control
git add .metrics/
git commit -m "Update metrics snapshots"
```

### Comparing Branches

```bash
# Check out different branches and compare
git checkout main
nexus analyze --json > /tmp/main-metrics.json

git checkout develop
nexus analyze --json > /tmp/develop-metrics.json

# Visual diff
diff /tmp/main-metrics.json /tmp/develop-metrics.json
```

## Limitations

- Trends are based on comparison to most recent snapshot only
- Snapshot history is limited to what's saved in `.metrics/`
- Does not automatically correlate metrics to git commits
- Status indicators are based on predefined thresholds

## Future Enhancements

Possible improvements:
- Correlation with git commits for automated snapshot tagging
- Statistical analysis and prediction
- Graph visualization of trends
- Alerting for significant regressions
- Multi-project comparison

## License

MIT - Use freely in any project
