```
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███╗   ██╗████████╗██████╗ ██╗   ██╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝ 
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝  
 ╚██████╗  ██║   ██████╔╝███████╗██║  ██║███████║██║ ╚████║   ██║   ██║  ██║   ██║   
  ╚═════╝  ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   
                                                                                        
          🔐 AI-Powered Autonomous Ethical Hacking Agent 🔐
```

# CyberSentry: Autonomous Ethical Website Security Auditor

[![Python 3.13](https://img.shields.io/badge/Python-3.13-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM-76B900?style=flat-square&logo=nvidia&logoColor=white)](https://build.nvidia.com/)
[![Llama 3.1 70B](https://img.shields.io/badge/LLM-Llama%203.1%2070B-FF9E64?style=flat-square)](https://www.llama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![ReAct Architecture](https://img.shields.io/badge/Architecture-ReAct%20Loop-4B8BBE?style=flat-square)](docs/ARCHITECTURE.md)
[![Ethical Hacking](https://img.shields.io/badge/Type-Ethical%20Hacking-3DDC84?style=flat-square)](DISCLAIMER.md)

---

## 📋 Table of Contents

- [Overview](#overview)
- [✨ Features](#-features)
- [🎯 Architecture](#-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [🔍 Real Findings](#-real-findings)
- [🗺️ Roadmap](#-roadmap)
- [👨‍💻 About the Developer](#-about-the-developer)
- [⚖️ Legal & Ethical Disclaimer](#-legal--ethical-disclaimer)
- [📄 License](#-license)

---

## Overview

**CyberSentry** is an autonomous AI-powered security auditing agent designed for ethical website penetration testing and vulnerability assessment. Powered by **NVIDIA NIM** running **Llama 3.1 70B**, it implements a **ReAct loop architecture** (Think → Act → Observe → Repeat) to intelligently coordinate 8 advanced security scanning tools.

Unlike traditional security scanners, CyberSentry reasons about findings, adapts its approach based on results, and generates professional bug-bounty style security reports with actionable recommendations.

### Key Innovation
- **Autonomous Decision-Making**: Uses Llama 3.1 70B to reason about security findings and adjust scanning strategy
- **Real-time Terminal Visualization**: Live xterm windows with hacker-themed green-on-black UI
- **8 Integrated Security Tools**: Robots/Sitemap, Tech Detection, HTTP Headers, SSL Analysis, Cookie Audit, Directory Fuzzing, CORS Testing, Nmap Scanning
- **Professional Reporting**: Generates industry-standard security audit reports with CVSS-style severity ratings

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Reasoning** | Llama 3.1 70B makes autonomous decisions about which tools to run and how to interpret results |
| 🔄 **ReAct Loop** | Implements Think → Act → Observe → Reason cycle for intelligent tool orchestration |
| 🎯 **8 Security Tools** | Robots/Sitemap Recon, Tech Stack Detection, HTTP Header Analysis, SSL Certificate Checking, Cookie Auditing, Directory Fuzzing, CORS Analysis, Nmap Port Scanning |
| 📊 **Real-time UI** | Rich terminal interface with color-coded severity indicators and live progress |
| 📈 **Professional Reports** | Generates markdown security reports with findings, severity levels, and remediation steps |
| 🛡️ **Ethical Focus** | Built with explicit ethical guidelines and requires authorized target specification |
| ⚡ **Efficient Scanning** | Intelligent tool coordination reduces scanning time vs. running all tools sequentially |
| 🔒 **Secure Credential Management** | Uses environment variables for API key management |

---

## 🎯 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (Target URL)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           ReAct Agent Loop (Autonomous)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 1️⃣  THINK: LLM analyzes target & plans tools        │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ 2️⃣  ACT: Execute planned security tools             │   │
│  │    ├─ Robots/Sitemap Parser                          │   │
│  │    ├─ Tech Stack Detector (Wappalyzer)              │   │
│  │    ├─ HTTP Header Analyzer                           │   │
│  │    ├─ SSL Certificate Checker                        │   │
│  │    ├─ Cookie Auditor                                 │   │
│  │    ├─ Directory Fuzzer                               │   │
│  │    ├─ CORS Policy Tester                             │   │
│  │    └─ Nmap Port Scanner                              │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ 3️⃣  OBSERVE: Collect tool outputs & results         │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ 4️⃣  REASON: LLM interprets findings & decides next  │   │
│  │    ├─ Run more focused scans?                        │   │
│  │    ├─ Deep dive on vulnerabilities?                 │   │
│  │    └─ Generate final report?                         │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│        Professional Security Audit Report (Markdown)         │
│  ├─ Findings by Severity (Critical/High/Medium/Low)         │
│  ├─ CVSS Scores & Risk Assessment                           │
│  ├─ Remediation Recommendations                             │
│  └─ Executive Summary                                        │
└─────────────────────────────────────────────────────────────┘
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.13 |
| **LLM Engine** | NVIDIA NIM (Llama 3.1 70B) |
| **Agent Pattern** | ReAct (Reasoning + Acting) |
| **Terminal UI** | Rich Python library |
| **Network Tools** | Nmap, requests, ssl, socket, subprocess |
| **Security Tools** | Robots parser, sslyze, requests_toolbelt |
| **Environment** | Kali Linux / WSL2 Ubuntu |
| **API Integration** | OpenAI-compatible NVIDIA NIM API |

---

## 📦 Installation

### Prerequisites

- **Python 3.13+**
- **pip** (Python package manager)
- **NVIDIA NIM API Key** ([Get free access](https://build.nvidia.com/))
- **Nmap** (for port scanning)
- **Kali Linux or WSL2 Ubuntu** (recommended for full tool support)

### Step 1: Clone Repository

```bash
git clone https://github.com/prutxvi/cybersentry.git
cd cybersentry
```

### Step 2: Create Virtual Environment

```bash
# On Kali Linux / Ubuntu
python3 -m venv venv
source venv/bin/activate

# On Windows (WSL2)
python -m venv venv
source venv/Scripts/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `openai` - NVIDIA NIM API client
- `python-dotenv` - Environment variable management
- `rich` - Beautiful terminal UI
- `requests` - HTTP requests
- `scapy` - Network packet manipulation

### Step 4: Configure Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your NVIDIA API key
nano .env
```

Add your NVIDIA NIM API key:
```
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TARGET_URL=https://your-own-website.com
```

### Step 5: Install System Dependencies

#### On Kali Linux:
```bash
sudo apt update
sudo apt install nmap xterm -y
```

#### On WSL2 Ubuntu:
```bash
sudo apt update
sudo apt install nmap xterm -y
```

---

## 🚀 Usage

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run security audit on configured target
python agent.py

# Expected output:
#   ✓ Tool 1/8: Robots.txt & Sitemap Analysis
#   ✓ Tool 2/8: Tech Stack Detection
#   ✓ Tool 3/8: HTTP Header Analysis
#   ✓ Tool 4/8: SSL Certificate Check
#   ✓ Tool 5/8: Cookie Audit
#   ✓ Tool 6/8: Directory Fuzzing
#   ✓ Tool 7/8: CORS Testing
#   ✓ Tool 8/8: Nmap Port Scan
#
#   📄 Report saved to: report_20260503_021648.md
```

### Interactive Mode

The agent will:
1. **Display its reasoning** in the terminal as it decides which tools to run
2. **Show real-time tool execution** in xterm windows with live output
3. **Ask follow-up questions** about findings that need deeper investigation
4. **Summarize results** after all tools complete
5. **Generate professional report** with findings and recommendations

### Output Files

```
report_YYYYMMDD_HHMMSS.md  ← Professional security audit report
```

The report includes:
- Executive summary
- Findings grouped by severity
- Technical details of each vulnerability
- CVSS scores (where applicable)
- Remediation recommendations
- Scan metadata (tool versions, timestamp, scope)

---

## 🔍 Real Findings

### Scan Target: bangaruvakili.com (May 2, 2026)

This is a real security audit performed on the developer's portfolio website. **Note: Scan was authorized by the domain owner.**

| Finding | Severity | CVSS | Status |
|---------|----------|------|--------|
| Missing Content-Security-Policy Header | **Medium** | 5.3 | ⚠️ Unpatched |
| Server Header Reveals Vercel Platform | **Low** | 2.7 | ℹ️ Info |
| SSL Certificate Expires June 2, 2026 | **Medium** | 5.9 | ⚠️ 30 Days |
| WordPress Paths Detected (403 Errors) | **Low** | 3.1 | ℹ️ Hardened |
| Missing X-Content-Type-Options Header | **Low** | 2.7 | ⚠️ Unpatched |

#### Detailed Findings

**[1] Missing Content-Security-Policy (CSP) Header** (Medium Severity)

- **Risk**: Without CSP, the site is vulnerable to XSS (Cross-Site Scripting) attacks
- **Finding**: Response headers lack `Content-Security-Policy` directive
- **CVSS v3.1**: 5.3 (Medium)
- **Recommendation**: Implement CSP header with strict directives
  ```
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'
  ```

**[2] Server Header Reveals Technology Stack** (Low Severity)

- **Risk**: Attackers learn site runs on Vercel, enabling targeted attacks
- **Finding**: `Server: Vercel` header exposed in HTTP response
- **CVSS v3.1**: 2.7 (Low)
- **Recommendation**: Remove or obfuscate server header
  ```
  # In Vercel vercel.json
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Server",
          "value": "Web Server"
        }
      ]
    }
  ]
  ```

**[3] SSL Certificate Expires Soon** (Medium Severity)

- **Risk**: Service interruption, potential MITM attacks during renewal
- **Finding**: Certificate valid until June 2, 2026 (30 days remaining)
- **CVSS v3.1**: 5.9 (Medium)
- **Recommendation**: Renew certificate immediately (auto-renewal via Vercel)

**[4] WordPress Paths Detected** (Low Severity)

- **Risk**: Potential information disclosure; 403 responses leak existence of WP paths
- **Finding**: Paths detected: `/wp-admin`, `/wp-includes`, `/wp-content` (all return 403)
- **CVSS v3.1**: 3.1 (Low)
- **Recommendation**: These are hardened and return 403, which is good. No action needed.

**[5] Missing X-Content-Type-Options Header** (Low Severity)

- **Risk**: MIME-type sniffing attacks
- **Finding**: `X-Content-Type-Options: nosniff` header not present
- **Recommendation**: Add header to prevent MIME-sniffing
  ```
  X-Content-Type-Options: nosniff
  ```

### Scan Statistics

- **Scan Date**: May 2, 2026
- **Total Tools Run**: 8/8 ✅
- **Findings Discovered**: 5
- **Critical Issues**: 0
- **High Issues**: 0
- **Medium Issues**: 2
- **Low Issues**: 3
- **Scan Duration**: ~45 seconds

For complete findings details, see [docs/FINDINGS.md](docs/FINDINGS.md)

---

## 🗺️ Roadmap

### ✅ Completed (v1.0)
- [x] Core ReAct agent implementation
- [x] 8 security tools integrated
- [x] Real-time terminal UI with Rich library
- [x] Professional report generation
- [x] NVIDIA NIM API integration
- [x] Environment configuration system
- [x] Ethical guidelines framework

### 🔄 In Development (v1.1)
- [ ] Multi-target batch scanning
- [ ] Persistent finding database
- [ ] Trend analysis and historical comparisons
- [ ] Slack/Discord notifications
- [ ] CI/CD integration support
- [ ] Extended tool set (15+ tools)

### 🚀 Planned (v2.0)
- [ ] Web dashboard for report visualization
- [ ] SQLite database for finding history
- [ ] Machine learning-based vulnerability prioritization
- [ ] Integration with bug bounty platforms (HackerOne API)
- [ ] Docker containerization
- [ ] Multi-LLM support (Claude, GPT-4, etc.)
- [ ] Advanced exploitation module (with proper safeguards)

---

## 👨‍💻 About the Developer

**Pruthvi Raj**

- 📍 Location: NIAT Aurora, Bhuvanagiri, Telangana, India
- 🎓 Education: B.Tech 1st Year (2025-2029)
- 🔐 Focus: Cybersecurity, AI, Ethical Hacking
- 🐙 GitHub: [github.com/prutxvi](https://github.com/prutxvi)
- 📧 Email: pruthviraj73962@gmail.com

### Motivation

CyberSentry was created as part of a mission to democratize security auditing tools and demonstrate the power of combining AI reasoning with traditional security scanning. This project showcases how autonomous agents can make intelligent decisions about security testing strategies.

### Vision

To develop tools that empower ethical hackers, security professionals, and organizations to assess and improve their security posture, while maintaining the highest standards of responsible disclosure and ethical conduct.

---

## ⚖️ Legal & Ethical Disclaimer

**IMPORTANT: READ BEFORE USE**

### Authorization Requirements

CyberSentry is designed **ONLY for authorized security testing**. You MUST have explicit written permission from the website owner before running any scans.

**Unauthorized access to computer systems is illegal.** Violations of the Computer Fraud and Abuse Act (CFAA) and similar laws worldwide can result in criminal charges.

### Acceptable Use

✅ DO:
- Test only systems you own or have explicit written authorization to test
- Use for educational purposes on authorized test environments
- Participate in legitimate bug bounty programs
- Help organizations identify and fix security issues
- Responsibly disclose all findings to affected parties

❌ DON'T:
- Scan systems without authorization
- Attempt to cause harm or disruption
- Exploit vulnerabilities maliciously
- Violate privacy laws (GDPR, CCPA, etc.)
- Share or sell findings without consent

### Disclaimer

The creators of CyberSentry assume no liability for misuse or damage caused by this tool. Users are solely responsible for complying with applicable laws and regulations. By using this tool, you agree to use it ethically and legally.

For complete ethical guidelines, see [DISCLAIMER.md](DISCLAIMER.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright © 2026 Pruthvi Raj**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions...

---

## 🤝 Contributing

Contributions are welcome! Please note that this project is designed for ethical security testing. Any contributions should maintain the ethical standards outlined in [DISCLAIMER.md](DISCLAIMER.md).

If you find a bug or have a feature suggestion, please open an issue on GitHub.

---

## 📚 Additional Resources

- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)
- [Llama 3.1 Model Card](https://www.llama.com/)
- [OWASP Top 10 Web Application Risks](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Bug Bounty Resources](https://www.hacker101.com/)

---

## 📞 Support

For issues, questions, or suggestions:
1. Check [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for technical details
2. Review [docs/FINDINGS.md](docs/FINDINGS.md) for example output
3. Open an issue on GitHub
4. Contact the developer at your.email@example.com

---

**Built for cybersecurity education and ethical hacking**

*Last Updated: May 3, 2026*
