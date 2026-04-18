#!/usr/bin/env python3
"""Audit Agent Framework CLI"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from audit_agent_framework.core import AuditAgent

def main():
    parser = argparse.ArgumentParser(description="Audit Agent Framework")
    parser.add_argument("target", help="Contract file to audit")
    parser.add_argument("--format", choices=["json", "html", "text"], default="text",
                      help="Output format")
    parser.add_argument("--output", "-o", help="Output file")
    
    args = parser.parse_args()
    
    if not Path(args.target).exists():
        print(f"Error: File not found: {args.target}")
        sys.exit(1)
    
    # Run audit
    agent = AuditAgent()
    report = agent.run_audit(args.target)
    
    # Generate report
    output = agent.generate_report(report, args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report saved to: {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
