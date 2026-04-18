"""
Audit Agent Framework - Modular Smart Contract Audit Framework
"""
import importlib
import pkgutil
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Type, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json

@dataclass
class Finding:
    scanner: str
    severity: str
    title: str
    description: str
    line: int
    file: str
    code: str
    recommendation: str
    confidence: float = 0.8

@dataclass
class AuditReport:
    target: str
    findings: List[Finding] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self):
        return {
            "target": self.target,
            "summary": {
                "total": len(self.findings),
                "critical": len([f for f in self.findings if f.severity == "critical"]),
                "high": len([f for f in self.findings if f.severity == "high"]),
                "medium": len([f for f in self.findings if f.severity == "medium"]),
                "low": len([f for f in self.findings if f.severity == "low"]),
            },
            "findings": [
                {
                    "scanner": f.scanner,
                    "severity": f.severity,
                    "title": f.title,
                    "line": f.line,
                    "description": f.description,
                    "recommendation": f.recommendation,
                    "confidence": f.confidence
                }
                for f in self.findings
            ]
        }

class BaseScanner(ABC):
    """Abstract base class for all scanners"""
    
    name: str = "base"
    description: str = "Base scanner"
    
    @abstractmethod
    def scan(self, target: str) -> List[Finding]:
        """Scan target and return findings"""
        pass
    
    def supports(self, target: str) -> bool:
        """Check if this scanner supports the target"""
        return True

class ReentrancyScanner(BaseScanner):
    """Scanner for reentrancy vulnerabilities"""
    
    name = "reentrancy"
    description = "Detects reentrancy vulnerabilities"
    
    def scan(self, target: str) -> List[Finding]:
        findings = []
        
        if not Path(target).exists():
            return findings
        
        with open(target, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # Detect external calls
            if any(keyword in line for keyword in [".call{value:", ".call{", "delegatecall"]):
                # Check if state update comes after
                findings.append(Finding(
                    scanner=self.name,
                    severity="critical",
                    title="Potential Reentrancy",
                    description="External call detected. Verify state updates happen before external calls.",
                    line=i,
                    file=target,
                    code=line.strip(),
                    recommendation="Follow Checks-Effects-Interactions pattern"
                ))
        
        return findings
    
    def supports(self, target: str) -> bool:
        return target.endswith('.sol')

class AccessControlScanner(BaseScanner):
    """Scanner for access control issues"""
    
    name = "access_control"
    description = "Detects access control vulnerabilities"
    
    def scan(self, target: str) -> List[Finding]:
        findings = []
        
        if not Path(target).exists():
            return findings
        
        with open(target, 'r') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for tx.origin usage
        for i, line in enumerate(lines, 1):
            if 'tx.origin' in line:
                findings.append(Finding(
                    scanner=self.name,
                    severity="critical",
                    title="Tx.Origin Authentication",
                    description="Using tx.origin for authentication is vulnerable to phishing attacks.",
                    line=i,
                    file=target,
                    code=line.strip(),
                    recommendation="Use msg.sender instead of tx.origin"
                ))
        
        return findings
    
    def supports(self, target: str) -> bool:
        return target.endswith('.sol')

class AuditAgent:
    """Main audit agent that orchestrates scanners"""
    
    def __init__(self):
        self.scanners: List[Type[BaseScanner]] = []
        self.load_builtin_scanners()
    
    def load_builtin_scanners(self):
        """Load built-in scanners"""
        self.register_scanner(ReentrancyScanner)
        self.register_scanner(AccessControlScanner)
    
    def register_scanner(self, scanner_class: Type[BaseScanner]):
        """Register a scanner class"""
        self.scanners.append(scanner_class)
    
    def run_audit(self, target: str) -> AuditReport:
        """Run full audit with all applicable scanners"""
        report = AuditReport(target=target)
        
        print(f"Running audit on: {target}")
        
        for scanner_class in self.scanners:
            scanner = scanner_class()
            
            if scanner.supports(target):
                print(f"  → Running {scanner.name}...")
                findings = scanner.scan(target)
                report.findings.extend(findings)
                print(f"     Found {len(findings)} issues")
        
        return report
    
    def generate_report(self, report: AuditReport, format: str = "json") -> str:
        """Generate formatted report"""
        if format == "json":
            return json.dumps(report.to_dict(), indent=2)
        elif format == "html":
            return self._generate_html(report)
        else:
            return self._generate_text(report)
    
    def _generate_text(self, report: AuditReport) -> str:
        """Generate text report"""
        lines = [
            "=" * 70,
            "AUDIT REPORT",
            "=" * 70,
            f"Target: {report.target}",
            "",
            f"Summary:",
            f"  Total Findings: {len(report.findings)}",
        ]
        
        summary = report.to_dict()["summary"]
        for sev in ["critical", "high", "medium", "low"]:
            lines.append(f"  {sev.upper()}: {summary[sev]}")
        
        lines.append("")
        lines.append("Findings:")
        lines.append("-" * 70)
        
        for f in report.findings:
            lines.append(f""")
            lines.append(f"[{f.severity.upper()}] {f.title}")
            lines.append(f"  Scanner: {f.scanner}")
            lines.append(f"  Line {f.line}: {f.code}")
            lines.append(f"  {f.description}")
            lines.append(f"  Fix: {f.recommendation}")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def _generate_html(self, report: AuditReport) -> str:
        """Generate HTML report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Audit Report - {report.target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .critical {{ color: #d32f2f; }}
        .high {{ color: #f57c00; }}
        .medium {{ color: #fbc02d; }}
        .low {{ color: #388e3c; }}
        .finding {{ margin: 20px 0; padding: 15px; border-left: 4px solid #ccc; }}
    </style>
</head>
<body>
    <h1>Audit Report</h1>
    <p>Target: {report.target}</p>
    <p>Total Findings: {len(report.findings)}</p>
    
    <h2>Findings</h2>
"""
        
        for f in report.findings:
            html += f"""
    <div class="finding {f.severity}">
        <h3>[{f.severity.upper()}] {f.title}</h3>
        <p><strong>Line {f.line}:</strong> {f.code}</p>
        <p>{f.description}</p>
        <p><strong>Recommendation:</strong> {f.recommendation}</p>
    </div>
"""
        
        html += "</body></html>"
        return html
