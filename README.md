# Audit Agent Framework 🤖

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

**Modular framework for building automated smart contract audit agents.**

## ✨ Features

- 🧩 **Modular Design** - Plug-and-play scanner modules
- 📝 **Auto Report Generation** - PDF/HTML audit reports
- 🔌 **Extensible** - Easy to add custom checks
- 🎯 **Multi-Engine** - Slither, Mythril, Manticore integration
- 🔄 **CI/CD Ready** - GitHub Actions, GitLab CI support
- 📊 **Metrics Dashboard** - Track audit performance

## 🚀 Quick Start

```bash
pip install audit-agent-framework

# Create agent
audit-agent init my_agent

# Add scanner
audit-agent add slither
audit-agent add custom_check

# Run audit
audit-agent run contract.sol --report pdf
```

## 🏗️ Architecture

```
audit_agent/
├── core/
│   ├── agent.py          # Main agent orchestrator
│   ├── scanner_loader.py # Dynamic scanner loading
│   └── reporter.py       # Report generation
├── scanners/
│   ├── slither_scanner.py
│   ├── mythril_scanner.py
│   └── template.py       # Custom scanner template
├── reports/
│   ├── pdf_generator.py
│   └── html_generator.py
└── cli.py
```

## 🎯 Use Cases

- **Audit Firms** - Standardize audit workflows
- **DeFi Teams** - Continuous security monitoring
- **Developers** - Pre-commit security checks
- **Researchers** - Custom analysis tools

## 📄 License

MIT License - see [LICENSE](LICENSE)
