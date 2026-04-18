"""
Example: Creating a custom scanner
"""
from audit_agent_framework.core import BaseScanner, Finding

class MyCustomScanner(BaseScanner):
    """Example custom scanner"""
    
    name = "my_custom"
    description = "My custom vulnerability scanner"
    
    def scan(self, target: str) -> list:
        findings = []
        # Your scanning logic here
        return findings

# Register and use
from audit_agent_framework.core import AuditAgent

agent = AuditAgent()
agent.register_scanner(MyCustomScanner)
report = agent.run_audit("contract.sol")
