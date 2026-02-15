#!/usr/bin/env python3
"""
CodeStats: Analyze and visualize your git repository statistics
Provides insights about development patterns, commit history, and contributor activity.
"""

import subprocess
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from dataclasses import dataclass, asdict


@dataclass
class CommitInfo:
    """Single commit metadata"""
    hash: str
    author: str
    date: str
    message: str
    timestamp: int
    files_changed: int
    insertions: int
    deletions: int


@dataclass
class AuthorStats:
    """Statistics for a single author"""
    name: str
    commits: int
    insertions: int
    deletions: int
    files_changed: int
    first_commit: str
    last_commit: str


@dataclass
class DateStats:
    """Statistics for a single date"""
    date: str
    commits: int
    insertions: int
    deletions: int
    authors: int


class GitAnalyzer:
    """Analyze git repository"""
    
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.commits = []
        self.verify_git_repo()
        self.load_commits()
    
    def verify_git_repo(self):
        """Verify this is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                print(f"Error: {self.repo_path} is not a git repository", file=sys.stderr)
                sys.exit(1)
        except subprocess.TimeoutExpired:
            print("Error: git command timed out", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: git not found. Is git installed?", file=sys.stderr)
            sys.exit(1)
    
    def run_git_command(self, args, text=True):
        """Run a git command and return output"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=text,
                timeout=30
            )
            if result.returncode != 0:
                return None
            return result.stdout
        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"Error running git command: {e}", file=sys.stderr)
            return None
    
    def load_commits(self):
        """Load full commit history with stats"""
        # Get list of commits
        log_output = self.run_git_command([
            "log",
            "--pretty=format:%H|%an|%ai|%s",
            "--all"
        ])
        
        if not log_output:
            print("Warning: Could not load commits", file=sys.stderr)
            return
        
        commit_hashes = self._parse_commit_hashes(log_output)
        self._load_stats_for_commits(commit_hashes)
    
    def _parse_commit_hashes(self, log_output):
        """Extract commit hashes from git log output"""
        hashes = []
        for line in log_output.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 4:
                hashes.append(parts[0])
        return hashes
    
    def _load_stats_for_commits(self, commit_hashes):
        """Load detailed stats for each commit"""
        for commit_hash in commit_hashes:
            commit = self._load_single_commit(commit_hash)
            if commit:
                self.commits.append(commit)
        
        # Sort by timestamp (oldest first)
        self.commits.sort(key=lambda x: x.timestamp)
    
    def _load_single_commit(self, commit_hash):
        """Load stats for a single commit"""
        stats_output = self.run_git_command([
            "show",
            "--pretty=format:%H|%an|%ai|%s",
            "--numstat",
            commit_hash
        ])
        
        if not stats_output:
            return None
        
        lines = stats_output.strip().split('\n')
        if not lines:
            return None
        
        # Parse header
        header = lines[0].split('|')
        if len(header) < 4:
            return None
        
        commit = CommitInfo(
            hash=header[0],
            author=header[1],
            date=header[2],
            message=header[3],
            timestamp=int(datetime.fromisoformat(header[2].replace('Z', '+00:00')).timestamp()),
            files_changed=0,
            insertions=0,
            deletions=0
        )
        
        # Parse stats
        for line in lines[1:]:
            parts = line.split('\t')
            if len(parts) >= 3:
                try:
                    insertions = int(parts[0]) if parts[0] != '-' else 0
                    deletions = int(parts[1]) if parts[1] != '-' else 0
                    commit.insertions += insertions
                    commit.deletions += deletions
                    commit.files_changed += 1
                except ValueError:
                    pass
        
        return commit
    
    def get_author_stats(self) -> dict:
        """Get statistics per author"""
        stats = defaultdict(lambda: {
            'commits': 0,
            'insertions': 0,
            'deletions': 0,
            'files_changed': 0,
            'first_commit': None,
            'last_commit': None
        })
        
        for commit in self.commits:
            author = commit.author
            stats[author]['commits'] += 1
            stats[author]['insertions'] += commit.insertions
            stats[author]['deletions'] += commit.deletions
            stats[author]['files_changed'] += commit.files_changed
            
            if not stats[author]['first_commit']:
                stats[author]['first_commit'] = commit.date
            stats[author]['last_commit'] = commit.date
        
        # Convert to AuthorStats objects
        result = {}
        for name, data in stats.items():
            result[name] = AuthorStats(
                name=name,
                commits=data['commits'],
                insertions=data['insertions'],
                deletions=data['deletions'],
                files_changed=data['files_changed'],
                first_commit=data['first_commit'],
                last_commit=data['last_commit']
            )
        
        return result
    
    def get_date_stats(self) -> dict:
        """Get statistics per date"""
        stats = defaultdict(lambda: {
            'commits': 0,
            'insertions': 0,
            'deletions': 0,
            'authors': set()
        })
        
        for commit in self.commits:
            date = commit.date.split()[0]  # YYYY-MM-DD
            stats[date]['commits'] += 1
            stats[date]['insertions'] += commit.insertions
            stats[date]['deletions'] += commit.deletions
            stats[date]['authors'].add(commit.author)
        
        # Convert to DateStats objects
        result = {}
        for date, data in stats.items():
            result[date] = DateStats(
                date=date,
                commits=data['commits'],
                insertions=data['insertions'],
                deletions=data['deletions'],
                authors=len(data['authors'])
            )
        
        return result
    
    def get_top_authors(self, limit=10, sort_by='commits'):
        """Get top authors by various metrics"""
        author_stats = self.get_author_stats()
        
        if sort_by == 'commits':
            sorted_authors = sorted(author_stats.values(), key=lambda x: x.commits, reverse=True)
        elif sort_by == 'insertions':
            sorted_authors = sorted(author_stats.values(), key=lambda x: x.insertions, reverse=True)
        elif sort_by == 'deletions':
            sorted_authors = sorted(author_stats.values(), key=lambda x: x.deletions, reverse=True)
        else:
            sorted_authors = sorted(author_stats.values(), key=lambda x: x.commits, reverse=True)
        
        return sorted_authors[:limit]
    
    def get_activity_by_day_of_week(self) -> dict:
        """Get commit activity by day of week"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        stats = defaultdict(int)
        
        for commit in self.commits:
            date = datetime.fromisoformat(commit.date.replace('Z', '+00:00'))
            day_name = days[date.weekday()]
            stats[day_name] += 1
        
        return dict(stats)
    
    def get_commits_by_hour(self) -> dict:
        """Get commit activity by hour of day"""
        stats = defaultdict(int)
        
        for commit in self.commits:
            date = datetime.fromisoformat(commit.date.replace('Z', '+00:00'))
            hour = date.hour
            stats[hour] += 1
        
        return dict(sorted(stats.items()))


class Reporter:
    """Format and display git statistics"""
    
    # ANSI colors
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    
    def __init__(self, use_colors=True):
        self.use_colors = use_colors
    
    def color(self, text, color_code):
        """Apply color if enabled"""
        if self.use_colors:
            return f"{color_code}{text}{self.RESET}"
        return text
    
    def print_header(self, title):
        """Print section header"""
        print(f"\n{self.color('╔' + '═' * 78 + '╗', self.CYAN)}")
        print(f"{self.color('║', self.CYAN)} {self.color(title, self.BOLD):<76} {self.color('║', self.CYAN)}")
        print(f"{self.color('╚' + '═' * 78 + '╝', self.CYAN)}\n")
    
    def print_bar(self, label, value, max_value=None, width=40):
        """Print a horizontal bar"""
        if max_value is None or max_value == 0:
            pct = 0
            bar_len = 0
        else:
            pct = (value / max_value) * 100
            bar_len = int((value / max_value) * width)
        
        bar = '█' * bar_len + '░' * (width - bar_len)
        print(f"  {label:<25} {bar} {pct:5.1f}%")
    
    def print_report(self, analyzer: GitAnalyzer):
        """Print comprehensive git statistics report"""
        if not analyzer.commits:
            print("No commits found in repository")
            return
        
        self.print_header("GIT REPOSITORY STATISTICS")
        self._print_overview(analyzer)
        self._print_contributors(analyzer)
        self._print_activity(analyzer)
        self._print_intensity(analyzer)
        print(f"{self.color('─' * 80, self.CYAN)}\n")
    
    def _print_overview(self, analyzer: GitAnalyzer):
        """Print repository overview section"""
        print(f"{self.color('📊 Repository Overview:', self.BOLD)}")
        print(f"  Total commits: {self.color(str(len(analyzer.commits)), self.GREEN)}")
        
        author_stats = analyzer.get_author_stats()
        print(f"  Unique authors: {len(author_stats)}")
        
        total_insertions = sum(c.insertions for c in analyzer.commits)
        total_deletions = sum(c.deletions for c in analyzer.commits)
        print(f"  Total insertions: {self.color(f'+{total_insertions:,}', self.GREEN)}")
        print(f"  Deletions: {self.color(f'-{total_deletions:,}', self.RED)}")
        
        if analyzer.commits:
            first = analyzer.commits[0]
            last = analyzer.commits[-1]
            print(f"  Date range: {first.date} to {last.date}")
    
    def _print_contributors(self, analyzer: GitAnalyzer):
        """Print top contributors section"""
        print(f"\n{self.color('👥 Top Contributors:', self.BOLD)}")
        top_authors = analyzer.get_top_authors(limit=10)
        if not top_authors:
            return
        
        max_commits = top_authors[0].commits
        for i, author in enumerate(top_authors, 1):
            pct = (author.commits / len(analyzer.commits) * 100) if analyzer.commits else 0
            bar_len = int((author.commits / max_commits) * 30)
            bar = '█' * bar_len + '░' * (30 - bar_len)
            print(f"  {i:2}. {author.name:<30} {bar} {author.commits:4} commits ({pct:5.1f}%)")
    
    def _print_activity(self, analyzer: GitAnalyzer):
        """Print activity by day of week section"""
        print(f"\n{self.color('📅 Activity by Day of Week:', self.BOLD)}")
        activity = analyzer.get_activity_by_day_of_week()
        if not activity:
            return
        
        max_commits = max(activity.values())
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            commits = activity.get(day, 0)
            if commits > 0:
                bar_len = int((commits / max_commits) * 30)
                bar = '█' * bar_len + '░' * (30 - bar_len)
                print(f"  {day:<12} {bar} {commits:4} commits")
    
    def _print_intensity(self, analyzer: GitAnalyzer):
        """Print code change intensity section"""
        total_insertions = sum(c.insertions for c in analyzer.commits)
        total_deletions = sum(c.deletions for c in analyzer.commits)
        total_changes = total_insertions + total_deletions
        
        print(f"\n{self.color('📈 Code Change Intensity:', self.BOLD)}")
        if total_changes == 0:
            return
        
        ins_pct = (total_insertions / total_changes) * 100
        del_pct = (total_deletions / total_changes) * 100
        print(f"  Additions:  {'█' * int(ins_pct / 2)} {ins_pct:.1f}%")
        print(f"  Deletions:  {'█' * int(del_pct / 2)} {del_pct:.1f}%")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze and visualize git repository statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze current repository
  python3 stats.py
  
  # Analyze specific repository
  python3 stats.py --repo /path/to/repo
  
  # Export as JSON
  python3 stats.py --json
  
  # Disable colors
  python3 stats.py --no-color
        """
    )
    
    parser.add_argument('--repo', type=str, default='.', help='Path to git repository')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    analyzer = GitAnalyzer(args.repo)
    
    if args.json:
        # Export all data as JSON
        data = {
            'commits': len(analyzer.commits),
            'authors': len(analyzer.get_author_stats()),
            'top_authors': [asdict(a) for a in analyzer.get_top_authors(limit=10)],
            'activity_by_day': analyzer.get_activity_by_day_of_week()
        }
        print(json.dumps(data, indent=2, default=str))
    else:
        reporter = Reporter(use_colors=not args.no_color)
        reporter.print_report(analyzer)


if __name__ == '__main__':
    main()
