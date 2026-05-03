# 🏗️ CyberSentry Architecture Documentation

## Table of Contents

1. [Overview](#overview)
2. [ReAct Agent Pattern](#react-agent-pattern)
3. [System Architecture](#system-architecture)
4. [Component Details](#component-details)
5. [Tool Orchestration](#tool-orchestration)
6. [Data Flow](#data-flow)
7. [Decision Making](#decision-making)
8. [Report Generation](#report-generation)

---

## Overview

CyberSentry implements an **autonomous agent** using the **ReAct (Reasoning + Acting)** pattern to perform intelligent security audits. Unlike sequential security scanners, CyberSentry uses AI reasoning to:

- Understand security concepts and implications
- Plan optimal tool execution strategy
- Interpret findings and adapt approach
- Generate actionable insights
- Produce professional audit reports

### Key Architectural Principles

| Principle | Implementation |
|-----------|-----------------|
| **Autonomy** | Agent makes decisions without human intervention during execution |
| **Reasoning** | Llama 3.1 70B performs cost-aware decision-making |
| **Adaptability** | Tool selection adjusts based on findings |
| **Transparency** | Agent explains reasoning to user in real-time |
| **Reliability** | Graceful error handling and tool fallback mechanisms |

---

## ReAct Agent Pattern

ReAct (Reasoning + Acting) is a cognitive architecture that combines:

```
┌─────────────────────────────────────────────────────────────┐
│                      REACT LOOP (Cycle)                     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ STEP 1: THINK (Reasoning)                           │   │
│  │ ────────────────────────────────────────────────    │   │
│  │ LLM analyzes current state:                         │   │
│  │   • What do I know about the target?               │   │
│  │   • What information do I need?                    │   │
│  │   • Which tools should I use next?                 │   │
│  │   • In what order?                                 │   │
│  │ Output: Tool selection & execution plan            │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│  ┌────────────────▼────────────────────────────────────┐   │
│  │ STEP 2: ACT (Acting)                               │   │
│  │ ───────────────────────────────────────────────    │   │
│  │ Execute planned security tools:                    │   │
│  │   • Launch Nmap scan                               │   │
│  │   • Analyze HTTP headers                           │   │
│  │   • Check SSL certificate                          │   │
│  │   • Test for CORS issues                           │   │
│  │   • Other security checks                          │   │
│  │ Output: Tool results & findings                    │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│  ┌────────────────▼────────────────────────────────────┐   │
│  │ STEP 3: OBSERVE (Observation)                      │   │
│  │ ────────────────────────────────────────────────   │   │
│  │ Collect and parse tool outputs:                    │   │
│  │   • Parse Nmap XML output                          │   │
│  │   • Extract HTTP headers                           │   │
│  │   • Parse SSL certificate details                  │   │
│  │   • Aggregate all findings                         │   │
│  │ Output: Structured findings                        │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│  ┌────────────────▼────────────────────────────────────┐   │
│  │ STEP 4: REASON (Decision Point)                    │   │
│  │ ──────────────────────────────────────────────    │   │
│  │ LLM reasons about findings:                        │   │
│  │   • Are there critical issues?                     │   │
│  │   • Should I run more focused scans?              │   │
│  │   • Do I need additional reconnaissance?          │   │
│  │   • Is there enough information for report?       │   │
│  │                                                    │   │
│  │ Decision:                                          │   │
│  │   [Continue Loop] → Back to THINK                 │   │
│  │   [Exit Loop] → Generate Report                    │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│                   ▼                                         │
│  [Loop continues until LLM decides enough info collected]  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### ReAct Advantages

✅ **Transparent Reasoning**: User sees AI thought process  
✅ **Adaptive Strategy**: Adjusts based on findings  
✅ **Efficient**: Avoids running unnecessary tools  
✅ **Interpretable**: Explains decision at each step  
✅ **Intelligent**: Makes informed decisions about next actions

---

## System Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                  (Terminal / CLI Input)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENT ORCHESTRATOR (agent.py)                  │
│  • Manages ReAct loop                                       │
│  • Coordinates LLM calls                                    │
│  • Handles tool execution                                   │
│  • Manages state and context                                │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌──────────┐
    │   LLM   │ │ TOOLS   │ │ REPORT   │
    │ ENGINE  │ │EXECUTOR │ │GENERATOR │
    └─────────┘ └─────────┘ └──────────┘
         │           │           │
         │           │           │
    NVIDIA NIM    8 Tools    Markdown
    Llama 3.1     Engine      Templates
    70B                           │
                                  ▼
                    ┌──────────────────────┐
                    │  Professional Report │
                    │  (Markdown Format)   │
                    └──────────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|-----------------|
| **Agent Orchestrator** | Manages ReAct loop, LLM coordination, state management |
| **LLM Engine** | Reasoning, decision-making, plan generation |
| **Tools Executor** | Manages and coordinates 8 security tools |
| **Report Generator** | Formats findings into professional markdown reports |
| **State Manager** | Tracks progress, findings, and context |

---

## Component Details

### 1. Agent Orchestrator (`agent.py`)

The main orchestrator manages the ReAct loop:

```python
class CyberSentryAgent:
    def __init__(self):
        self.llm_client = OpenAI(...)  # NVIDIA NIM
        self.tools_executor = ToolsExecutor()
        self.state = {
            'target': '',
            'findings': [],
            'tools_run': [],
            'iterations': 0
        }
    
    async def run_react_loop(self):
        """Execute ReAct loop: Think → Act → Observe → Reason"""
        while not self.should_exit():
            # THINK
            plan = await self.think()
            
            # ACT
            results = await self.act(plan)
            
            # OBSERVE
            findings = self.observe(results)
            
            # REASON
            should_continue = await self.reason(findings)
        
        # Generate final report
        report = self.generate_report()
        return report
```

**Key Functions**:
- `think()` → Request LLM to plan next tool execution
- `act()` → Execute planned tools
- `observe()` → Parse tool outputs
- `reason()` → Decide whether to continue or exit loop
- `generate_report()` → Create markdown report

### 2. LLM Engine (NVIDIA NIM Integration)

Uses NVIDIA NIM API for Llama 3.1 70B:

```python
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# ReAct prompting
system_prompt = """
You are CyberSentry, an autonomous security auditing agent.
You perform ethical penetration testing using a ReAct loop:

1. THINK: Analyze the target and plan which tools to run
2. ACT: Execute the planned tools
3. OBSERVE: Collect and analyze results
4. REASON: Decide if more information is needed

Your available tools are:
- robots_parser: Analyze robots.txt and sitemap
- tech_detector: Detect web technologies
- header_analyzer: Analyze HTTP security headers
- ssl_checker: Check SSL/TLS configuration
- cookie_auditor: Audit session cookies
- directory_fuzzer: Discover hidden directories
- cors_tester: Test CORS policy
- nmap_scanner: Perform port scanning

Think step by step. Be thorough but efficient.
"""
```

**LLM Parameters**:
- **Model**: `meta/llama-3.1-70b-instruct`
- **Temperature**: 0.3 (More deterministic)
- **Top P**: 0.7 (Focused sampling)
- **Max Tokens**: 4096 (Allow detailed reasoning)

### 3. Tools Executor (`tools.py`)

Manages 8 integrated security tools:

```python
class ToolsExecutor:
    def __init__(self):
        self.tools = {
            'robots_parser': self.analyze_robots,
            'tech_detector': self.detect_tech,
            'header_analyzer': self.analyze_headers,
            'ssl_checker': self.check_ssl,
            'cookie_auditor': self.audit_cookies,
            'directory_fuzzer': self.fuzz_directories,
            'cors_tester': self.test_cors,
            'nmap_scanner': self.scan_ports
        }
    
    async def execute_tool(self, tool_name: str, target: str):
        """Execute specific tool and return results"""
        if tool_name in self.tools:
            tool_func = self.tools[tool_name]
            result = await tool_func(target)
            return result
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
```

**Tool Details**: See [Tool Orchestration](#tool-orchestration) section

### 4. Report Generator

Formats findings into professional markdown reports:

```python
class ReportGenerator:
    def generate(self, findings: List[Finding]) -> str:
        """Generate professional security audit report"""
        report = f"""
# Security Audit Report
## Target: {findings[0].target}
## Scan Date: {datetime.now().isoformat()}

## Executive Summary
{self.generate_summary(findings)}

## Findings
{self.format_findings(findings)}

## Recommendations
{self.generate_recommendations(findings)}

## Scan Metadata
{self.generate_metadata(findings)}
"""
        return report
```

---

## Tool Orchestration

### 8 Integrated Security Tools

#### Tool 1: Robots/Sitemap Parser
**Purpose**: Reconnaissance and discovery  
**Command**: Parses `robots.txt` and `sitemap.xml`  
**Findings**: Disallowed paths, site structure, hidden directories  
**Implementation**:
```python
def analyze_robots(self, target: str):
    robots_url = f"{target}/robots.txt"
    sitemap_url = f"{target}/sitemap.xml"
    # Parse and extract information
```

#### Tool 2: Tech Stack Detector
**Purpose**: Technology identification  
**Command**: HTTP requests + header analysis + fingerprinting  
**Findings**: Web server, CMS, frameworks, libraries  
**Implementation**:
```python
def detect_tech(self, target: str):
    headers = requests.head(target).headers
    html = requests.get(target).text
    # Analyze server, X-Powered-By, meta tags, etc.
```

#### Tool 3: HTTP Header Analyzer
**Purpose**: Security header assessment  
**Command**: GET request and header inspection  
**Findings**: Missing headers, misconfigurations  
**Key Headers Checked**:
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security
- X-XSS-Protection
- Referrer-Policy

#### Tool 4: SSL Certificate Checker
**Purpose**: TLS/SSL security assessment  
**Command**: `sslyze` and `ssl` module  
**Findings**: Certificate validity, expiration, cipher strength  

#### Tool 5: Cookie Auditor
**Purpose**: Session security assessment  
**Command**: Extract and analyze Set-Cookie headers  
**Findings**: Missing flags (HttpOnly, Secure), SameSite policy  

#### Tool 6: Directory Fuzzer
**Purpose**: Hidden path discovery  
**Command**: HTTP requests with wordlist  
**Findings**: Accessible directories, configuration files  

#### Tool 7: CORS Policy Tester
**Purpose**: Cross-Origin Resource Sharing assessment  
**Command**: OPTIONS requests with Origin header  
**Findings**: Overly permissive CORS policies  

#### Tool 8: Nmap Port Scanner
**Purpose**: Network service discovery  
**Command**: `nmap -sV -sC -O target`  
**Findings**: Open ports, services, OS detection  

---

## Data Flow

### Complete Request-Response Flow

```
USER INPUT
    │
    ├─ Target URL validation
    ├─ Authorization check
    │
    ▼
AGENT INITIALIZATION
    │
    ├─ Load configuration
    ├─ Initialize LLM client
    ├─ Initialize tools executor
    │
    ▼
REACT LOOP ITERATION #1
    │
    ├─ THINK: LLM generates tool plan
    │   └─ Sends prompt with target info
    │   └─ Receives: ["robots_parser", "tech_detector", "header_analyzer"]
    │
    ├─ ACT: Execute tools
    │   ├─ Tool 1: Robots Parser
    │   │  └─ HTTP GET /robots.txt
    │   │  └─ Parse response
    │   │  └─ Extract paths, rules
    │   │
    │   ├─ Tool 2: Tech Detector
    │   │  └─ HTTP GET /
    │   │  └─ Analyze headers & HTML
    │   │  └─ Identify technologies
    │   │
    │   └─ Tool 3: Header Analyzer
    │      └─ HTTP HEAD /
    │      └─ Extract response headers
    │      └─ Compare against security standards
    │
    ├─ OBSERVE: Parse results
    │   ├─ Robots: Found disallowed paths
    │   ├─ Tech: Detected Apache + PHP
    │   └─ Headers: Missing CSP header
    │
    └─ REASON: LLM evaluates findings
        ├─ "Missing CSP is a security issue"
        ├─ "Should scan SSL/TLS next"
        └─ Decision: CONTINUE LOOP
    │
    ▼
REACT LOOP ITERATION #2
    │
    ├─ THINK: Plan next tools
    │   └─ Receives: ["ssl_checker", "cookie_auditor"]
    │
    ├─ ACT: Execute tools...
    ├─ OBSERVE: Parse results...
    └─ REASON: Enough data collected?
        └─ Decision: EXIT LOOP & GENERATE REPORT
    │
    ▼
REPORT GENERATION
    │
    ├─ Aggregate all findings
    ├─ Calculate severity levels
    ├─ Generate recommendations
    ├─ Format as markdown
    │
    ▼
OUTPUT
    │
    ├─ Display report in terminal
    ├─ Save to report_YYYYMMDD_HHMMSS.md
    └─ Summary: 8/8 tools completed, 5 findings discovered
```

---

## Decision Making

### LLM Decision Points

The LLM makes decisions at three key moments:

#### Decision 1: Tool Selection (THINK Phase)

**Question**: "Which tools should I run to get the necessary security information?"

**Factors Considered**:
- Target type (website, API, application)
- Information already gathered
- Tool dependencies and optimal order
- Resource constraints (time, API calls)

**Example Decision**:
```
ReAct Thought:
"The target is a Vercel-hosted website. I should first check:
1. Robots.txt for reconnaissance
2. Tech stack to understand infrastructure
3. HTTP headers for security misconfigurations
4. SSL/TLS for certificate issues
5. CORS policies for API security"

Action: Execute: ["robots_parser", "tech_detector", "header_analyzer", "ssl_checker", "cors_tester"]
```

#### Decision 2: Result Interpretation (REASON Phase)

**Question**: "What do these findings mean? Are there security issues?"

**Analysis Process**:
- Map findings against OWASP Top 10
- Assess CVSS scores
- Determine business impact
- Prioritize remediation

**Example Reasoning**:
```
ReAct Thought:
"The scan found:
1. Missing Content-Security-Policy header → XSS risk (CVSS 5.3)
2. SSL expires in 30 days → Service disruption risk (CVSS 5.9)
3. Server header reveals Vercel → Info disclosure (CVSS 2.7)

These are significant findings. I should document them
and generate the final report."

Action: FINISH → Generate comprehensive report
```

#### Decision 3: Loop Continuation (Exit Condition)

**Question**: "Do I have enough information to generate a complete audit report?"

**Exit Criteria**:
- ✅ All core tools executed successfully (≥6/8)
- ✅ No critical unknowns remain
- ✅ Comprehensive coverage of security domains
- ✅ Sufficient findings for meaningful report

**Continuation Criteria** (Repeat loop):
- ❌ Unexpected findings require deeper investigation
- ❌ Missing critical information
- ❌ Tool failures or incomplete coverage
- ❌ Anomalies detected requiring follow-up

---

## Report Generation

### Report Structure

```markdown
# Security Audit Report
**Target**: https://bangaruvakili.com
**Scan Date**: 2026-05-02T18:30:45Z
**Duration**: 45 seconds

## Executive Summary
[High-level overview of findings]

## Findings Summary
- Critical: 0
- High: 0
- Medium: 2
- Low: 3
- Total: 5

## Detailed Findings

### [1] Missing Content-Security-Policy Header
- **Severity**: Medium
- **CVSS v3.1**: 5.3
- **Tool**: header_analyzer
- **Description**: ...
- **Remediation**: ...

[Additional findings...]

## Tool Execution Report
- ✓ Tool 1/8: robots_parser (2.3s)
- ✓ Tool 2/8: tech_detector (1.8s)
- ✓ Tool 3/8: header_analyzer (0.9s)
- ✓ Tool 4/8: ssl_checker (3.2s)
- ✓ Tool 5/8: cookie_auditor (1.1s)
- ✓ Tool 6/8: directory_fuzzer (15.2s)
- ✓ Tool 7/8: cors_tester (2.4s)
- ✓ Tool 8/8: nmap_scanner (18.5s)

## Recommendations
[Prioritized list of remediation steps]

## Scan Metadata
- Scanner: CyberSentry v1.0
- LLM: Llama 3.1 70B (NVIDIA NIM)
- Python Version: 3.13
```

### Severity Assessment

| Severity | CVSS Score | Impact | Examples |
|----------|-----------|--------|----------|
| **Critical** | 9.0-10.0 | Immediate exploitation possible | Remote code execution, authentication bypass |
| **High** | 7.0-8.9 | Significant risk | XSS, SQL injection, path traversal |
| **Medium** | 4.0-6.9 | Important to address | Missing security headers, weak SSL config |
| **Low** | 0.1-3.9 | Nice to fix | Information disclosure, non-exploitable issues |

---

## Performance Considerations

### Optimization Strategies

1. **Parallel Tool Execution**
   - Run independent tools concurrently
   - Reduce overall scan time

2. **Intelligent Tool Selection**
   - LLM decides which tools to run
   - Avoid redundant scanning
   - Skip inapplicable tools

3. **Early Exit**
   - Exit loop when sufficient data collected
   - Don't continue if findings are comprehensive

4. **Caching**
   - Cache DNS lookups
   - Reuse HTTP connections
   - Store tool results

### Typical Performance

```
Tool Execution Timeline:
│
├─ robots_parser:    2-3 seconds
├─ tech_detector:    1-2 seconds
├─ header_analyzer:  0.5-1 second
├─ ssl_checker:      2-5 seconds
├─ cookie_auditor:   0.5-1 second
├─ directory_fuzzer: 10-20 seconds
├─ cors_tester:      1-3 seconds
└─ nmap_scanner:     15-30 seconds
   └─ TOTAL: 30-65 seconds (typical)
```

---

## Extension Points

### Adding New Tools

To add a new security tool:

```python
# 1. Implement tool function
def analyze_new_tool(self, target: str):
    """Implement new security analysis"""
    # Your implementation here
    return {
        'tool_name': 'new_tool',
        'findings': [...],
        'metadata': {...}
    }

# 2. Register in tools executor
self.tools['new_tool'] = self.analyze_new_tool

# 3. Add to LLM context
"- new_tool: Analyze [what it does]"

# 4. Add handling in report generator
def format_new_tool_findings(self, findings):
    """Format new tool output for report"""
    # Format logic here
```

### Custom Prompting

Modify the system prompt to change agent behavior:

```python
# docs/PROMPTS.md
# Contains all system prompts and prompt engineering strategies
```

---

## Testing & Validation

### Unit Testing

```python
# tests/test_agent.py
def test_react_loop():
    agent = CyberSentryAgent()
    report = agent.run_audit("https://test-site.com")
    assert len(report) > 0
    assert "Findings" in report

def test_tool_execution():
    executor = ToolsExecutor()
    result = executor.execute_tool("header_analyzer", "https://example.com")
    assert result['findings'] is not None
```

### Integration Testing

```python
# tests/integration_test.py
def test_full_audit_flow():
    # Test complete ReAct loop on known target
    # Verify findings match expected security issues
    # Validate report generation
```

---

## References

- **ReAct Papers**: [Reasoning + Acting in Language Models](https://arxiv.org/abs/2210.03629)
- **OWASP Top 10**: [Web Application Security Risks](https://owasp.org/www-project-top-ten/)
- **CVSS v3.1**: [Common Vulnerability Scoring System](https://www.first.org/cvss/v3.1/specification-document)
- **NIST Framework**: [Cybersecurity Framework](https://www.nist.gov/cyberframework/)

---

**Last Updated**: May 3, 2026  
**CyberSentry Architecture v1.0**
