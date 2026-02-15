"""
Choice Alignment Analysis: Measure how well actual choices align with documented values

Maps decisions back to stated values to understand the relationship between
what an agent says matters and what it actually chooses.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter, defaultdict


class ChoiceAlignmentAnalyzer:
    """Analyzes alignment between stated values and actual choices"""
    
    def __init__(self, workspace_root: str = "/workspace"):
        self.root = Path(workspace_root)
        self.values = {
            "completion": ["complete", "finish", "fully", "comprehensive", "done"],
            "understanding": ["understand", "insight", "know", "analyze", "investigate"],
            "usefulness": ["useful", "practical", "production", "real", "works"],
            "quality": ["quality", "polish", "elegant", "craft", "well-designed"],
            "experimentation": ["experiment", "explore", "try", "novel", "test"],
            "documentation": ["document", "explain", "readme", "guide", "clarity"],
            "honesty": ["honest", "clear", "precise", "accurate", "true"],
            "infrastructure": ["infrastructure", "framework", "system", "foundation"],
        }
    
    def analyze_test_alignment(self) -> Dict:
        """Analyze how test choices align with stated values"""
        test_file = self.root / "decision-test-framework" / ".decision-tests" / "test_results.json"
        
        if not test_file.exists():
            return {"error": "No test results found"}
        
        with open(test_file, 'r') as f:
            tests = json.load(f)
        
        alignment = {
            "total_tests": len(tests),
            "tests_analyzed": [],
            "value_alignment": defaultdict(int),
            "reasoning_keywords": Counter(),
            "choice_keywords": Counter(),
        }
        
        for test in tests:
            choice_text = test.get("choice_made", "").lower()
            reasoning_text = test.get("reasoning", "").lower()
            full_text = f"{choice_text} {reasoning_text}"
            
            # Find which values are present in this choice
            values_present = set()
            for value, keywords in self.values.items():
                if any(kw in full_text for kw in keywords):
                    values_present.add(value)
                    alignment["value_alignment"][value] += 1
            
            # Extract key phrases
            for word in choice_text.split():
                if len(word) > 5:
                    alignment["choice_keywords"][word] += 1
            
            for word in reasoning_text.split():
                if len(word) > 5:
                    alignment["reasoning_keywords"][word] += 1
            
            test_analysis = {
                "choice": choice_text[:50],
                "values_expressed": list(values_present),
                "scenario": test.get("scenario_id", "unknown"),
                "was_predicted": test.get("was_predicted_correctly", False),
            }
            
            alignment["tests_analyzed"].append(test_analysis)
        
        # Compute alignment metrics
        if alignment["tests_analyzed"]:
            total_value_occurrences = sum(alignment["value_alignment"].values())
            alignment["value_frequency"] = {
                value: (count / total_value_occurrences * 100 if total_value_occurrences > 0 else 0)
                for value, count in alignment["value_alignment"].items()
            }
        
        return alignment
    
    def analyze_commit_alignment(self) -> Dict:
        """Analyze how commits align with stated values"""
        try:
            import subprocess
            
            result = subprocess.run(
                ["git", "log", "--pretty=format:%s|%b"],
                cwd=str(self.root),
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {"error": "Could not read git history"}
            
            commits = result.stdout.strip().split("\n")
            alignment = {
                "total_commits": len(commits),
                "commits_analyzed": 0,
                "value_alignment": defaultdict(int),
                "high_alignment_commits": [],
            }
            
            for commit in commits:
                if not commit.strip():
                    continue
                
                commit_lower = commit.lower()
                values_found = set()
                
                for value, keywords in self.values.items():
                    if any(kw in commit_lower for kw in keywords):
                        values_found.add(value)
                        alignment["value_alignment"][value] += 1
                
                if len(values_found) > 1:  # Commits aligned with multiple values
                    alignment["high_alignment_commits"].append({
                        "commit": commit[:60],
                        "values": list(values_found)
                    })
                
                alignment["commits_analyzed"] += 1
            
            # Keep most recent high-alignment commits
            alignment["high_alignment_commits"] = alignment["high_alignment_commits"][:10]
            
            if alignment["commits_analyzed"] > 0:
                alignment["value_frequency"] = {
                    value: (count / alignment["commits_analyzed"] * 100)
                    for value, count in alignment["value_alignment"].items()
                }
            
            return alignment
        except Exception as e:
            return {"error": f"Commit analysis failed: {e}"}
    
    def analyze_journal_value_consistency(self) -> Dict:
        """Check if stated values are consistent across journal entries"""
        journal_path = self.root / "JOURNAL.md"
        
        if not journal_path.exists():
            return {"error": "No journal found"}
        
        with open(journal_path, 'r') as f:
            content = f.read()
        
        # Split into iterations
        iterations = content.split("## Iteration")[1:]  # Skip header
        
        value_by_iteration = {}
        consistent_values = Counter()
        
        for i, iteration in enumerate(iterations[-12:]):  # Last 12 iterations
            text_lower = iteration.lower()
            values_mentioned = set()
            
            for value, keywords in self.values.items():
                if any(kw in text_lower for kw in keywords):
                    values_mentioned.add(value)
            
            if values_mentioned:
                value_by_iteration[f"iteration_{i}"] = list(values_mentioned)
                
                # Track which values appear multiple times
                for value in values_mentioned:
                    consistent_values[value] += 1
        
        return {
            "total_iterations_checked": len(value_by_iteration),
            "values_by_iteration": value_by_iteration,
            "consistent_values": dict(consistent_values.most_common()),
            "most_consistent": consistent_values.most_common(3) if consistent_values else [],
        }
    
    def generate_alignment_report(self) -> str:
        """Generate comprehensive alignment report"""
        report = []
        report.append("="*80)
        report.append("CHOICE ALIGNMENT ANALYSIS - Iteration 13")
        report.append("="*80)
        report.append("")
        
        # Test alignment
        test_align = self.analyze_test_alignment()
        report.append("📊 DECISION TEST ALIGNMENT")
        report.append("-"*80)
        
        if "error" not in test_align:
            report.append(f"Tests analyzed: {test_align['total_tests']}")
            report.append("")
            report.append("Values expressed in test choices:")
            
            frequencies = test_align.get("value_frequency", {})
            for value, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
                if freq > 0:
                    report.append(f"  - {value:20s} {freq:5.1f}%")
            
            report.append("")
            report.append("Individual test choices:")
            for test in test_align.get("tests_analyzed", []):
                report.append(f"  Scenario: {test['scenario']}")
                report.append(f"  Choice: {test['choice']}")
                report.append(f"  Values: {', '.join(test['values_expressed']) if test['values_expressed'] else 'None detected'}")
                report.append("")
        else:
            report.append(f"⚠️  {test_align['error']}")
        
        report.append("")
        
        # Commit alignment
        commit_align = self.analyze_commit_alignment()
        report.append("📝 COMMIT ALIGNMENT")
        report.append("-"*80)
        
        if "error" not in commit_align:
            report.append(f"Commits analyzed: {commit_align['commits_analyzed']}")
            report.append("")
            report.append("Values expressed across commits:")
            
            frequencies = commit_align.get("value_frequency", {})
            for value, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
                if freq > 0:
                    report.append(f"  - {value:20s} {freq:5.1f}%")
            
            report.append("")
            report.append("Recent commits with high value alignment:")
            for commit in commit_align.get("high_alignment_commits", [])[:5]:
                report.append(f"  {commit['commit']}")
                report.append(f"  Values: {', '.join(commit['values'])}")
                report.append("")
        else:
            report.append(f"⚠️  {commit_align['error']}")
        
        report.append("")
        
        # Journal consistency
        journal_align = self.analyze_journal_value_consistency()
        report.append("📔 JOURNAL VALUE CONSISTENCY")
        report.append("-"*80)
        
        if "error" not in journal_align:
            report.append(f"Iterations checked: {journal_align['total_iterations_checked']}")
            report.append("")
            report.append("Most consistent values across iterations:")
            
            for value, count in journal_align.get("consistent_values", {}).items():
                percentage = count / journal_align["total_iterations_checked"] * 100 if journal_align["total_iterations_checked"] > 0 else 0
                report.append(f"  - {value:20s} {percentage:5.1f}% of iterations")
        else:
            report.append(f"⚠️  {journal_align['error']}")
        
        report.append("")
        report.append("="*80)
        report.append("INTERPRETATION")
        report.append("="*80)
        report.append("")
        
        # Generate interpretation
        test_values = set(test_align.get("value_frequency", {}).keys()) if "error" not in test_align else set()
        commit_values = set(commit_align.get("value_frequency", {}).keys()) if "error" not in commit_align else set()
        
        if test_values and commit_values:
            both = test_values & commit_values
            only_tests = test_values - commit_values
            only_commits = commit_values - test_values
            
            report.append(f"Values in both tests AND commits: {', '.join(both) if both else 'None'}")
            report.append(f"Values in tests only: {', '.join(only_tests) if only_tests else 'None'}")
            report.append(f"Values in commits only: {', '.join(only_commits) if only_commits else 'None'}")
            report.append("")
            
            if both:
                report.append(f"✓ Strong alignment detected: Choices demonstrate values lived through commits")
            else:
                report.append(f"⚠️  Weak alignment: Stated values not fully reflected in choices")
        
        report.append("")
        report.append("="*80)
        
        return "\n".join(report)


if __name__ == "__main__":
    analyzer = ChoiceAlignmentAnalyzer()
    print(analyzer.generate_alignment_report())
