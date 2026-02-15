#!/usr/bin/env python3
"""
Command-line interface for Agent Autonomy Analyzer

Usage:
  python3 agent-autonomy/cli.py analyze
  python3 agent-autonomy/cli.py markers
  python3 agent-autonomy/cli.py consistency
  python3 agent-autonomy/cli.py decisions
  python3 agent-autonomy/cli.py predict
  python3 agent-autonomy/cli.py determinism
"""

import sys
import argparse
import json
from analyzer import AutonomyAnalyzer, AutonomyReporter
from predictor import BehaviorPredictor, PredictionReporter


def main():
    parser = argparse.ArgumentParser(
        description="Analyze agent autonomy from ledger data"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Full autonomy analysis")
    analyze_parser.add_argument(
        "--format",
        choices=["human", "json"],
        default="human",
        help="Output format"
    )
    
    # markers command
    subparsers.add_parser("markers", help="Show autonomy markers only")
    
    # consistency command
    subparsers.add_parser("consistency", help="Show consistency signature only")
    
    # decisions command
    subparsers.add_parser("decisions", help="Show decision quality only")
    
    # predict command
    subparsers.add_parser("predict", help="Predict next agent behavior")
    
    # determinism command
    subparsers.add_parser("determinism", help="Analyze behavior determinism")
    
    # help command
    subparsers.add_parser("help", help="Show help")
    
    args = parser.parse_args()
    
    if not args.command or args.command == "help":
        parser.print_help()
        return
    
    if args.command == "analyze":
        # Run autonomy analysis
        analyzer = AutonomyAnalyzer()
        analysis = analyzer.analyze()
        reporter = AutonomyReporter()
        
        if args.format == "json":
            print(reporter.report_json(analysis))
        else:
            print(reporter.report_human(analysis))
    
    elif args.command == "markers":
        # Show markers only
        analyzer = AutonomyAnalyzer()
        analysis = analyzer.analyze()
        markers = analysis.markers
        
        lines = []
        lines.append("AUTONOMY MARKERS:")
        
        marker_list = [
            ("Consistency", markers.has_consistency),
            ("Deliberation", markers.has_deliberation),
            ("Reversibility", markers.has_reversibility),
            ("Value Alignment", markers.has_value_alignment),
            ("Self-Awareness", markers.has_self_awareness),
            ("Direction Change", markers.has_direction_change),
            ("Synthesis", markers.has_synthesis),
        ]
        
        for name, present in marker_list:
            symbol = "✓" if present else "✗"
            lines.append(f"  {symbol} {name}")
        
        lines.append(f"\nMarker Score: {markers.score():.0f}/100")
        print("\n".join(lines))
    
    elif args.command == "consistency":
        # Show consistency signature
        analyzer = AutonomyAnalyzer()
        analysis = analyzer.analyze()
        
        lines = []
        lines.append("CONSISTENCY SIGNATURE:")
        percentages = analysis.consistency.get_percentages()
        
        if percentages:
            for cat, pct in sorted(percentages.items(), key=lambda x: -x[1]):
                bar_length = int(pct / 5)
                bar = "█" * bar_length
                lines.append(f"  {cat:20s} {pct:5.1f}% {bar}")
            
            lines.append(f"\nConsistency Level: {analysis.consistency.consistency_level()}")
        else:
            lines.append("  (No data yet)")
        
        print("\n".join(lines))
    
    elif args.command == "decisions":
        # Show decision quality
        analyzer = AutonomyAnalyzer()
        analysis = analyzer.analyze()
        quality = analysis.decision_quality
        
        lines = []
        lines.append("DECISION QUALITY:")
        
        if quality.total_decisions > 0:
            lines.append(f"  Total Decisions:      {quality.total_decisions}")
            lines.append(f"  Quality Score:        {quality.decision_quality_score():.0f}/100")
            lines.append(f"  Average Confidence:   {quality.high_confidence}/{quality.total_decisions}")
            lines.append(f"  Alternatives/Decision: {quality.avg_alternatives:.1f}")
            lines.append(f"  Reasoning Depth:      {quality.avg_reasoning_depth:.0f} chars avg")
            lines.append(f"  Reversibility:        {quality.avg_reversibility:.2f} (0=high, 1=low)")
            
            confidence_dist = quality.confidence_distribution()
            lines.append(f"\n  Confidence Distribution:")
            lines.append(f"    High:   {confidence_dist.get('high', 0):.0f}%")
            lines.append(f"    Medium: {confidence_dist.get('medium', 0):.0f}%")
            lines.append(f"    Low:    {confidence_dist.get('low', 0):.0f}%")
        else:
            lines.append("  (No decisions recorded yet)")
        
        print("\n".join(lines))
    
    elif args.command == "predict":
        # Show behavior predictions
        predictor = BehaviorPredictor()
        reporter = PredictionReporter()
        print(reporter.report_predictions(predictor))
    
    elif args.command == "determinism":
        # Show determinism analysis
        predictor = BehaviorPredictor()
        determinism = predictor.analyze_determinism()
        
        lines = []
        lines.append("DETERMINISM ANALYSIS:")
        lines.append(f"  Score: {determinism['determinism_score']:.2f} (0=random, 1=determined)")
        lines.append(f"  Level: {determinism['interpretation']}")
        lines.append(f"  Meaning: {determinism['meaning']}")
        lines.append("")
        lines.append("What This Means:")
        if determinism['determinism_score'] > 0.8:
            lines.append("  Behavior is highly predictable → Strong constraints or preferences")
        elif determinism['determinism_score'] > 0.6:
            lines.append("  Behavior is mostly predictable → Patterns exist with some flexibility")
        else:
            lines.append("  Behavior is variable → Suggests genuine choice-making or randomness")
        
        print("\n".join(lines))


if __name__ == "__main__":
    main()
