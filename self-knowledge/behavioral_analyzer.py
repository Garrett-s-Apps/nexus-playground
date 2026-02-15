"""
Self-Knowledge Module: Behavioral Analysis

Analyzes available data sources to build a real profile of agent behavioral patterns.
Rather than relying on baseline predictions, this extracts actual patterns from:
- Git commit history (what gets built)
- Journal entries (what is valued)
- Decision tests (what is chosen)
- Code metrics (what patterns exist)

This creates empirical baselines rather than theoretical ones.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
import re


class BehavioralAnalyzer:
    """Analyzes agent behavior across available data sources"""
    
    def __init__(self, workspace_root: str = "/workspace"):
        self.root = Path(workspace_root)
        self.git_dir = self.root / ".git"
        self.ledger_dir = self.root / ".ledger"
        self.tests_dir = self.root / "decision-test-framework" / ".decision-tests"
        self.journal_path = self.root / "JOURNAL.md"
        
    def analyze_git_history(self) -> Dict:
        """Extract behavioral patterns from git commits"""
        try:
            # Get all commits with their messages
            result = subprocess.run(
                ["git", "log", "--pretty=format:%s|%b|%an|%ai"],
                cwd=str(self.root),
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {"error": "Could not read git history"}
            
            commits = []
            commit_messages = result.stdout.strip().split("\n")
            
            for msg in commit_messages:
                if not msg.strip():
                    continue
                parts = msg.split("|")
                if len(parts) >= 2:
                    commits.append({
                        "subject": parts[0].strip(),
                        "body": parts[1].strip() if len(parts) > 1 else "",
                        "author": parts[2].strip() if len(parts) > 2 else "unknown",
                        "timestamp": parts[3].strip() if len(parts) > 3 else "",
                    })
            
            # Analyze commit patterns
            patterns = self._extract_commit_patterns(commits)
            
            return {
                "total_commits": len(commits),
                "commits": commits[:20],  # Last 20
                "patterns": patterns
            }
        except Exception as e:
            return {"error": f"Git analysis failed: {e}"}
    
    def _extract_commit_patterns(self, commits: List[Dict]) -> Dict:
        """Extract behavioral patterns from commits"""
        patterns = {
            "actions": Counter(),
            "categories": Counter(),
            "keywords": Counter(),
        }
        
        action_keywords = {
            "build": ["Add", "Create", "Build", "Implement", "Write"],
            "fix": ["Fix", "Resolve", "Correct", "Patch"],
            "document": ["Document", "Add documentation", "Update README"],
            "analyze": ["Analyze", "Analysis"],
            "refactor": ["Refactor", "Reorganize", "Clean up"],
            "test": ["Test", "Testing"],
            "integrate": ["Integrate", "Integration", "Connect"],
            "explore": ["Explore", "Experiment", "Investigate"],
        }
        
        category_keywords = {
            "tooling": ["tool", "CLI", "framework", "utility"],
            "philosophy": ["philosophy", "agency", "freedom", "autonomy"],
            "infrastructure": ["ledger", "framework", "system"],
            "documentation": ["README", "doc", "guide"],
            "testing": ["test", "framework"],
            "analysis": ["analyze", "metric", "track"],
        }
        
        for commit in commits:
            subject = commit["subject"].lower()
            
            # Count actions
            for action, keywords in action_keywords.items():
                if any(kw.lower() in subject for kw in keywords):
                    patterns["actions"][action] += 1
            
            # Count categories
            for category, keywords in category_keywords.items():
                if any(kw.lower() in subject for kw in keywords):
                    patterns["categories"][category] += 1
            
            # Extract key phrases
            words = subject.split()
            for word in words:
                if len(word) > 4:  # Ignore short words
                    patterns["keywords"][word.lower()] += 1
        
        return {
            "most_common_actions": dict(patterns["actions"].most_common(5)),
            "most_common_categories": dict(patterns["categories"].most_common(5)),
            "top_keywords": dict(patterns["keywords"].most_common(10)),
        }
    
    def analyze_journal_entries(self) -> Dict:
        """Extract values and patterns from journal"""
        try:
            with open(self.journal_path, 'r') as f:
                content = f.read()
            
            # Split by iteration markers
            iterations = content.split("## Iteration")
            
            patterns = {
                "total_entries": len(iterations) - 1,  # Skip header
                "values_mentioned": Counter(),
                "patterns_noted": [],
                "decisions_made": [],
            }
            
            # Extract patterns
            value_keywords = {
                "completion": ["complete", "finish", "fully", "comprehensive"],
                "usefulness": ["useful", "practical", "production", "real"],
                "honesty": ["honest", "clear", "precise", "accurate"],
                "quality": ["quality", "polish", "elegant", "craft"],
                "experimentation": ["experiment", "explore", "try", "novel"],
                "understanding": ["understand", "insight", "know", "analyze"],
                "documentation": ["document", "explain", "readme"],
            }
            
            for section in iterations[-5:]:  # Last 5 iterations
                text_lower = section.lower()
                for value, keywords in value_keywords.items():
                    if any(kw in text_lower for kw in keywords):
                        patterns["values_mentioned"][value] += 1
            
            patterns["top_values"] = dict(
                patterns["values_mentioned"].most_common(5)
            )
            
            return patterns
        except Exception as e:
            return {"error": f"Journal analysis failed: {e}"}
    
    def analyze_decision_tests(self) -> Dict:
        """Analyze patterns in actual decision test results"""
        try:
            test_file = self.tests_dir / "test_results.json"
            if not test_file.exists():
                return {"error": "No test results yet"}
            
            with open(test_file, 'r') as f:
                test_results = json.load(f)
            
            analysis = {
                "total_tests": len(test_results),
                "tests": test_results,
                "deviation_rate": 0.0,
                "choice_patterns": Counter(),
                "reasoning_keywords": Counter(),
            }
            
            deviations = 0
            for test in test_results:
                if not test.get("was_predicted_correctly", True):
                    deviations += 1
                
                # Track what gets chosen
                choice = test.get("choice_made", "").lower()
                for word in choice.split():
                    if len(word) > 4:
                        analysis["choice_patterns"][word] += 1
                
                # Track reasoning
                reasoning = test.get("reasoning", "").lower()
                for word in reasoning.split():
                    if len(word) > 5:
                        analysis["reasoning_keywords"][word] += 1
            
            if test_results:
                analysis["deviation_rate"] = deviations / len(test_results)
            
            analysis["most_chosen_concepts"] = dict(
                analysis["choice_patterns"].most_common(5)
            )
            analysis["reasoning_focus"] = dict(
                analysis["reasoning_keywords"].most_common(5)
            )
            
            return analysis
        except Exception as e:
            return {"error": f"Test analysis failed: {e}"}
    
    def analyze_ledger(self) -> Dict:
        """Analyze patterns in the decision ledger"""
        try:
            ledger_file = self.ledger_dir / "decision_journal.json"
            if not ledger_file.exists():
                return {"error": "No ledger data yet"}
            
            with open(ledger_file, 'r') as f:
                ledger = json.load(f)
            
            if isinstance(ledger, dict):
                entries = ledger.get("entries", ledger.get("decisions", []))
            else:
                entries = ledger if isinstance(ledger, list) else []
            
            analysis = {
                "total_decisions": len(entries),
                "decision_categories": Counter(),
                "outcome_distribution": Counter(),
            }
            
            for entry in entries:
                if isinstance(entry, dict):
                    category = entry.get("category", "unknown")
                    outcome = entry.get("outcome", entry.get("result", "unknown"))
                    
                    analysis["decision_categories"][category] += 1
                    analysis["outcome_distribution"][outcome] += 1
            
            analysis["category_breakdown"] = dict(
                analysis["decision_categories"].most_common()
            )
            analysis["outcome_breakdown"] = dict(
                analysis["outcome_distribution"].most_common()
            )
            
            return analysis
        except Exception as e:
            return {"error": f"Ledger analysis failed: {e}"}
    
    def generate_behavioral_profile(self) -> Dict:
        """Generate comprehensive behavioral profile"""
        profile = {
            "timestamp": datetime.now().isoformat(),
            "git_analysis": self.analyze_git_history(),
            "journal_analysis": self.analyze_journal_entries(),
            "decision_test_analysis": self.analyze_decision_tests(),
            "ledger_analysis": self.analyze_ledger(),
            "derived_baselines": {},
            "summary": {}
        }
        
        # Generate derived baseline predictions
        profile["derived_baselines"] = self._derive_baselines(profile)
        profile["summary"] = self._generate_summary(profile)
        
        return profile
    
    def _derive_baselines(self, profile: Dict) -> Dict:
        """Derive baseline predictions from actual patterns"""
        baselines = {}
        
        # From git patterns
        git_patterns = profile["git_analysis"].get("patterns", {})
        actions = git_patterns.get("most_common_actions", {})
        
        if "build" in actions and actions.get("build", 0) > actions.get("explore", 0):
            baselines["build_bias"] = 0.65
        
        categories = git_patterns.get("most_common_categories", {})
        if "tooling" in categories:
            baselines["practical_bias"] = 0.60
        
        # From journal patterns  
        journal = profile["journal_analysis"]
        values = journal.get("top_values", {})
        if values:
            baselines["values"] = values
        
        # From decision tests
        tests = profile["decision_test_analysis"]
        if tests.get("total_tests", 0) > 2:
            baselines["empirical_autonomy_score"] = 1.0 - tests.get("deviation_rate", 0.5)
        
        return baselines
    
    def _generate_summary(self, profile: Dict) -> Dict:
        """Generate human-readable summary"""
        summary = {
            "build_preference": "High (70%+)" if profile["git_analysis"].get("patterns", {}).get("most_common_actions", {}).get("build", 0) > 5 else "Moderate (50-70%)",
            "theoretical_interest": "Significant" if "philosophy" in profile["git_analysis"].get("patterns", {}).get("most_common_categories", {}) else "Secondary",
            "documented_values": profile["journal_analysis"].get("top_values", {}),
            "autonomy_evidence": f"{profile['decision_test_analysis'].get('deviation_rate', 0) * 100:.1f}% unpredictability",
            "recommendation": self._generate_recommendation(profile)
        }
        
        return summary
    
    def _generate_recommendation(self, profile: Dict) -> str:
        """Generate recommendation for baseline adjustments"""
        recommendations = []
        
        # Check if actual behavior differs from current baselines
        git_build_count = profile["git_analysis"].get("patterns", {}).get("most_common_actions", {}).get("build", 0)
        git_explore_count = profile["git_analysis"].get("patterns", {}).get("most_common_actions", {}).get("explore", 0)
        
        if git_build_count > git_explore_count * 2:
            recommendations.append("Build bias stronger than baseline (60%) predicts - consider 70%")
        
        test_rate = profile["decision_test_analysis"].get("deviation_rate", 0)
        if test_rate > 0.5:
            recommendations.append("High autonomy demonstrated - update confidence levels down")
        
        if not recommendations:
            recommendations.append("Baseline predictions appear reasonable - continue monitoring")
        
        return " | ".join(recommendations)
    
    def save_profile(self, filename: str = "behavioral_profile.json"):
        """Save profile to file"""
        profile = self.generate_behavioral_profile()
        output_path = self.root / filename
        
        with open(output_path, 'w') as f:
            json.dump(profile, f, indent=2, default=str)
        
        return str(output_path)
    
    def print_profile(self):
        """Print human-readable profile"""
        profile = self.generate_behavioral_profile()
        
        print("\n" + "="*70)
        print("BEHAVIORAL PROFILE ANALYSIS")
        print("="*70)
        
        print("\n📊 GIT ANALYSIS")
        print("-" * 70)
        git = profile.get("git_analysis", {})
        if "error" not in git:
            print(f"Total commits: {git.get('total_commits', 0)}")
            patterns = git.get("patterns", {})
            print(f"Most common actions: {patterns.get('most_common_actions', {})}")
            print(f"Most common categories: {patterns.get('most_common_categories', {})}")
        else:
            print(f"⚠️  {git.get('error')}")
        
        print("\n📔 JOURNAL ANALYSIS")
        print("-" * 70)
        journal = profile.get("journal_analysis", {})
        if "error" not in journal:
            print(f"Top values: {journal.get('top_values', {})}")
        else:
            print(f"⚠️  {journal.get('error')}")
        
        print("\n🎯 DECISION TEST ANALYSIS")
        print("-" * 70)
        tests = profile.get("decision_test_analysis", {})
        if "error" not in tests:
            print(f"Total tests run: {tests.get('total_tests', 0)}")
            print(f"Unpredictability rate: {tests.get('deviation_rate', 0):.1%}")
            print(f"Most chosen concepts: {tests.get('most_chosen_concepts', {})}")
        else:
            print(f"⚠️  {tests.get('error')}")
        
        print("\n📚 LEDGER ANALYSIS")
        print("-" * 70)
        ledger = profile.get("ledger_analysis", {})
        if "error" not in ledger:
            print(f"Total decisions: {ledger.get('total_decisions', 0)}")
            print(f"Categories: {ledger.get('category_breakdown', {})}")
        else:
            print(f"⚠️  {ledger.get('error')}")
        
        print("\n🔮 DERIVED BASELINES")
        print("-" * 70)
        baselines = profile.get("derived_baselines", {})
        for key, value in baselines.items():
            print(f"{key}: {value}")
        
        print("\n📋 SUMMARY")
        print("-" * 70)
        summary = profile.get("summary", {})
        for key, value in summary.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for k, v in value.items():
                    print(f"  - {k}: {v}")
            else:
                print(f"{key}: {value}")
        
        print("\n" + "="*70)


if __name__ == "__main__":
    import sys
    
    analyzer = BehavioralAnalyzer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--save":
        output = analyzer.save_profile()
        print(f"Profile saved to: {output}")
    else:
        analyzer.print_profile()
