#!/usr/bin/env python3
"""
Metrics Tracker - Track code quality and repository metrics over time

Compares current metrics against historical baselines and shows trends,
regressions, and improvements. Helps teams monitor code health evolution.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Snapshot:
    """A single point-in-time metrics snapshot"""
    timestamp: str
    commit_hash: Optional[str]
    source: str  # 'analyze' or 'stats'
    data: dict


class MetricsTracker:
    """Track and compare metrics over time"""
    
    def __init__(self, snapshot_dir: str = ".metrics"):
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(exist_ok=True)
        self.snapshots: List[Snapshot] = []
        self.load_snapshots()
    
    def load_snapshots(self):
        """Load all historical snapshots"""
        if not self.snapshot_dir.exists():
            return
        
        for snapshot_file in sorted(self.snapshot_dir.glob("*.json")):
            try:
                with open(snapshot_file) as f:
                    data = json.load(f)
                    # Parse filename: YYYY-MM-DDTHH-MM-SS-source[-hash].json
                    # Example: 2026-02-15T04-11-48-analyze.json
                    parts = snapshot_file.stem.split('-')
                    if len(parts) >= 4:  # Need at least YYYY-MM-DDTHH-MM-SS-source
                        # Extract timestamp (first 3 parts: YYYY, MM, DDTHH, MM, SS)
                        # But this is tricky with the T separator...
                        # Better: Just use the stem minus the source
                        stem = snapshot_file.stem
                        
                        # Find the source (last component that's 'analyze' or 'stats')
                        source = None
                        commit_hash = None
                        
                        if '-analyze' in stem:
                            source = 'analyze'
                            idx = stem.rfind('-analyze')
                            timestamp = stem[:idx]
                            remainder = stem[idx+8:]  # len('-analyze') = 8
                            if remainder.startswith('-'):
                                commit_hash = remainder[1:]
                        elif '-stats' in stem:
                            source = 'stats'
                            idx = stem.rfind('-stats')
                            timestamp = stem[:idx]
                            remainder = stem[idx+6:]  # len('-stats') = 6
                            if remainder.startswith('-'):
                                commit_hash = remainder[1:]
                        
                        if source:
                            snapshot = Snapshot(
                                timestamp=timestamp,
                                commit_hash=commit_hash,
                                source=source,
                                data=data
                            )
                            self.snapshots.append(snapshot)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load {snapshot_file}: {e}", file=sys.stderr)
    
    def save_snapshot(self, source: str, data: dict, commit_hash: Optional[str] = None):
        """Save a new metrics snapshot"""
        now = datetime.now().isoformat().replace(':', '-').split('.')[0]
        hash_suffix = f"-{commit_hash}" if commit_hash else ""
        filename = f"{now}-{source}{hash_suffix}.json"
        filepath = self.snapshot_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filepath
    
    def get_latest_snapshot(self, source: str) -> Optional[Snapshot]:
        """Get the most recent snapshot for a source"""
        matching = [s for s in self.snapshots if s.source == source]
        return matching[-1] if matching else None
    
    def get_all_snapshots(self, source: str) -> List[Snapshot]:
        """Get all snapshots for a source"""
        return [s for s in self.snapshots if s.source == source]
    
    def calculate_complexity_trend(self, current: dict) -> Dict:
        """Calculate complexity metrics trend"""
        latest = self.get_latest_snapshot('analyze')
        if not latest:
            return {'status': 'no_history', 'message': 'No previous complexity metrics found'}
        
        # Handle both single file and directory results
        current_data = current[0] if isinstance(current, list) else current
        latest_data = latest.data[0] if isinstance(latest.data, list) else latest.data
        
        current_max = current_data.get('max_complexity', 0)
        latest_max = latest_data.get('max_complexity', 0)
        
        current_avg = current_data.get('avg_complexity', 0)
        latest_avg = latest_data.get('avg_complexity', 0)
        
        max_change = current_max - latest_max
        avg_change = current_avg - latest_avg
        
        return {
            'status': 'good' if max_change <= 0 else 'warning' if max_change <= 2 else 'bad',
            'max_complexity': {
                'current': current_max,
                'previous': latest_max,
                'change': max_change,
                'percent_change': (max_change / latest_max * 100) if latest_max > 0 else 0
            },
            'avg_complexity': {
                'current': current_avg,
                'previous': latest_avg,
                'change': avg_change,
                'percent_change': (avg_change / latest_avg * 100) if latest_avg > 0 else 0
            }
        }
    
    def calculate_contributor_trend(self, current: dict) -> Dict:
        """Calculate contributor metrics trend"""
        latest = self.get_latest_snapshot('stats')
        if not latest:
            return {'status': 'no_history', 'message': 'No previous stats metrics found'}
        
        current_commits = current.get('commits', 0)
        latest_commits = latest.data.get('commits', 0)
        
        current_authors = current.get('authors', 0)
        latest_authors = latest.data.get('authors', 0)
        
        commit_change = current_commits - latest_commits
        author_change = current_authors - latest_authors
        
        return {
            'status': 'active' if commit_change > 0 else 'stable' if commit_change == 0 else 'idle',
            'commits': {
                'current': current_commits,
                'previous': latest_commits,
                'change': commit_change
            },
            'authors': {
                'current': current_authors,
                'previous': latest_authors,
                'change': author_change
            }
        }
    
    def get_complexity_history(self, max_items: int = 10) -> List[Dict]:
        """Get complexity metrics history"""
        snapshots = self.get_all_snapshots('analyze')
        history = []
        
        for snapshot in snapshots[-max_items:]:
            data = snapshot.data[0] if isinstance(snapshot.data, list) else snapshot.data
            history.append({
                'timestamp': snapshot.timestamp,
                'max_complexity': data.get('max_complexity', 0),
                'avg_complexity': data.get('avg_complexity', 0),
                'num_functions': data.get('num_functions', 0)
            })
        
        return history
    
    def get_contributor_history(self, max_items: int = 10) -> List[Dict]:
        """Get contributor metrics history"""
        snapshots = self.get_all_snapshots('stats')
        history = []
        
        for snapshot in snapshots[-max_items:]:
            history.append({
                'timestamp': snapshot.timestamp,
                'commits': snapshot.data.get('commits', 0),
                'authors': snapshot.data.get('authors', 0)
            })
        
        return history


class TrendReporter:
    """Report on trends and changes"""
    
    # ANSI colors
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors
    
    def color(self, text, color_code):
        """Apply color if enabled"""
        if self.use_colors:
            return f"{color_code}{text}{self.RESET}"
        return text
    
    def get_trend_indicator(self, change: float, good_direction: str = 'down') -> str:
        """Get indicator for metric change"""
        if change == 0:
            return '→ '
        
        is_positive = change > 0
        if good_direction == 'down':
            # For metrics like complexity (lower is better)
            if is_positive:
                return self.color('↑ ', self.RED)  # Bad: went up
            else:
                return self.color('↓ ', self.GREEN)  # Good: went down
        else:
            # For metrics like commits (higher is better)
            if is_positive:
                return self.color('↑ ', self.GREEN)  # Good: went up
            else:
                return self.color('↓ ', self.RED)  # Bad: went down
    
    def print_complexity_trend(self, trend: Dict):
        """Print complexity trend report"""
        print(f"\n{self.color('📊 Code Complexity Trend:', self.BOLD)}")
        
        if trend.get('status') == 'no_history':
            print(f"  {trend.get('message')}")
            return
        
        max_trend = trend['max_complexity']
        avg_trend = trend['avg_complexity']
        
        indicator = self.get_trend_indicator(max_trend['change'], 'down')
        status_color = self.GREEN if trend['status'] == 'good' else self.YELLOW if trend['status'] == 'warning' else self.RED
        
        print(f"  Status: {self.color(trend['status'].upper(), status_color)}")
        print(f"  Max Complexity: {max_trend['current']} {indicator} (was {max_trend['previous']})")
        if max_trend['change'] != 0:
            pct = max_trend['percent_change']
            print(f"    Change: {max_trend['change']:+.1f} ({pct:+.1f}%)")
        
        print(f"  Avg Complexity: {avg_trend['current']:.1f} {self.get_trend_indicator(avg_trend['change'], 'down')} (was {avg_trend['previous']:.1f})")
        if avg_trend['change'] != 0:
            pct = avg_trend['percent_change']
            print(f"    Change: {avg_trend['change']:+.1f} ({pct:+.1f}%)")
    
    def print_contributor_trend(self, trend: Dict):
        """Print contributor trend report"""
        print(f"\n{self.color('👥 Contributor Activity Trend:', self.BOLD)}")
        
        if trend.get('status') == 'no_history':
            print(f"  {trend.get('message')}")
            return
        
        commits = trend['commits']
        authors = trend['authors']
        
        indicator = self.get_trend_indicator(commits['change'], 'up')
        status_color = self.GREEN if trend['status'] == 'active' else self.YELLOW
        
        print(f"  Status: {self.color(trend['status'].upper(), status_color)}")
        print(f"  Recent Commits: {commits['current']} {indicator} (was {commits['previous']})")
        if commits['change'] != 0:
            print(f"    Change: {commits['change']:+d}")
        
        print(f"  Active Authors: {authors['current']} {self.get_trend_indicator(authors['change'], 'up')} (was {authors['previous']})")
        if authors['change'] != 0:
            print(f"    Change: {authors['change']:+d}")
    
    def print_history(self, history: List[Dict], metric_type: str):
        """Print metric history"""
        if not history:
            print(f"  No history available")
            return
        
        print(f"\n{self.color('📈 Recent History:', self.BOLD)}")
        
        if metric_type == 'complexity':
            for i, entry in enumerate(history[-5:]):
                print(f"  {i+1}. {entry['timestamp']:<20} max={entry['max_complexity']} avg={entry['avg_complexity']:.1f}")
        elif metric_type == 'contributors':
            for i, entry in enumerate(history[-5:]):
                print(f"  {i+1}. {entry['timestamp']:<20} commits={entry['commits']} authors={entry['authors']}")


def main():
    parser = argparse.ArgumentParser(
        description='Track and compare code metrics over time',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Save current complexity metrics
  nexus analyze --json | python3 tracker.py save --source analyze
  
  # Show trend compared to last snapshot
  nexus analyze --json | python3 tracker.py show-trend --source analyze
  
  # Show contributor activity trend
  nexus stats --json | python3 tracker.py show-trend --source stats
  
  # Show history of metrics
  python3 tracker.py history --source analyze
  python3 tracker.py history --source stats
        """
    )
    
    parser.add_argument('command', choices=['save', 'show-trend', 'history'],
                       help='Command to execute')
    parser.add_argument('--source', choices=['analyze', 'stats'], required=True,
                       help='Metrics source (analyze=code, stats=git)')
    parser.add_argument('--commit', type=str, help='Commit hash to associate with snapshot')
    parser.add_argument('--dir', type=str, default='.metrics',
                       help='Directory for storing snapshots (default: .metrics)')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    tracker = MetricsTracker(args.dir)
    reporter = TrendReporter(use_colors=not args.no_color)
    
    if args.command == 'save':
        # Read JSON from stdin
        try:
            data = json.load(sys.stdin)
            filepath = tracker.save_snapshot(args.source, data, args.commit)
            print(f"Snapshot saved to {filepath}")
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'show-trend':
        # Read JSON from stdin
        try:
            data = json.load(sys.stdin)
            
            if args.source == 'analyze':
                trend = tracker.calculate_complexity_trend(data)
                reporter.print_complexity_trend(trend)
                history = tracker.get_complexity_history()
                reporter.print_history(history, 'complexity')
            else:
                trend = tracker.calculate_contributor_trend(data)
                reporter.print_contributor_trend(trend)
                history = tracker.get_contributor_history()
                reporter.print_history(history, 'contributors')
            
            print()
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'history':
        if args.source == 'analyze':
            history = tracker.get_complexity_history()
            reporter.print_history(history, 'complexity')
        else:
            history = tracker.get_contributor_history()
            reporter.print_history(history, 'contributors')
        print()


if __name__ == '__main__':
    main()
