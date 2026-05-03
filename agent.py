#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║   ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███╗  ██╗ ║
║  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝████╗ ██║ ║
║  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗██╔██╗██║ ║
║  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██║╚████║ ║
║  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║ ╚███║ ║
║   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚══╝║
║                                                               ║
║         AI-Powered Ethical Hacking Agent                      ║
║         Brain: Llama 3.1 70B on NVIDIA NIM                    ║
║         Built by: Pruthvi Raj | NIAT Aurora                   ║
╚═══════════════════════════════════════════════════════════════╝
"""

import os, json, sys, time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich import box
from tools import TOOLS, TOOL_DEFS

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
TARGET_URL     = os.getenv("TARGET_URL", "")
MODEL          = "meta/llama-3.1-70b-instruct"
BASE_URL       = "https://integrate.api.nvidia.com/v1"
MAX_STEPS      = 20

console = Console()

# ── Hacker color theme ─────────────────────────────────────
MATRIX_GREEN  = "bright_green"
CYBER_CYAN    = "cyan"
WARN_YELLOW   = "yellow"
DANGER_RED    = "bold red"
DIM_GRAY      = "dim"

TOOL_EMOJI = {
    "robots_sitemap":    "📄",
    "tech_detection":    "🔍",
    "check_headers":     "🛡️ ",
    "check_ssl":         "🔒",
    "check_cookies":     "🍪",
    "directory_fuzzing": "📂",
    "check_cors":        "🌐",
    "nmap_scan":         "🔌",
}

PHASE_MAP = {
    "robots_sitemap":    "① PASSIVE RECON",
    "tech_detection":    "① PASSIVE RECON",
    "check_headers":     "② ACTIVE SCANNING",
    "check_ssl":         "② ACTIVE SCANNING",
    "check_cookies":     "② ACTIVE SCANNING",
    "directory_fuzzing": "③ ATTACK SURFACE",
    "check_cors":        "③ ATTACK SURFACE",
    "nmap_scan":         "④ INFRASTRUCTURE",
}

# ── Validate setup ─────────────────────────────────────────
if not NVIDIA_API_KEY or "paste" in NVIDIA_API_KEY:
    console.print(Panel(
        "[bold red]❌ NVIDIA_API_KEY not set in .env![/bold red]",
        border_style="red"
    ))
    sys.exit(1)

if not TARGET_URL or "your-website" in TARGET_URL:
    console.print()
    TARGET_URL = console.input(
        "[bold cyan]  🎯 TARGET URL (your own site only) ► [/bold cyan]"
    ).strip()
    if not TARGET_URL.startswith("http"):
        TARGET_URL = "https://" + TARGET_URL

client = OpenAI(
    api_key=NVIDIA_API_KEY,
    base_url=BASE_URL,
    timeout=90
)

# ── System prompt ──────────────────────────────────────────
SYSTEM_PROMPT = f"""You are CyberSentry, an autonomous penetration testing agent.
Target: {TARGET_URL}

You have these tools available. You MUST call one tool per response — never just write text.

EXECUTE IN THIS EXACT ORDER:
Step 1:  Call robots_sitemap
Step 2:  Call tech_detection  
Step 3:  Call check_headers
Step 4:  Call check_ssl
Step 5:  Call check_cookies
Step 6:  Call directory_fuzzing
Step 7:  Call check_cors
Step 8:  Call nmap_scan
Step 9:  Write the final report (only after all 8 tools are done)

RULES:
- ALWAYS respond by calling the next tool. Never just write text until Step 9.
- Call ONLY ONE tool per response.
- After receiving a tool result, immediately call the NEXT tool in the list.
- Only write the final report after ALL 8 tools have been called.

Target: {TARGET_URL}
"""

def print_banner():
    console.clear()
    banner = Text()
    banner.append("\n")
    banner.append("  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███╗  ██╗\n", style=MATRIX_GREEN)
    banner.append(" ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝████╗ ██║\n", style=MATRIX_GREEN)
    banner.append(" ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗██╔██╗██║\n", style="green")
    banner.append(" ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██║╚████║\n", style="green")
    banner.append(" ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║ ╚███║\n", style="dark_green")
    banner.append("  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚══╝\n", style="dark_green")
    banner.append("\n")
    console.print(banner, justify="center")

    info = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    info.add_column("k", style="dim cyan", width=12)
    info.add_column("v", style="bold white")
    info.add_row("Brain",   "Llama 3.1 70B (NVIDIA NIM)")
    info.add_row("Target",  f"[bold yellow]{TARGET_URL}[/bold yellow]")
    info.add_row("Mode",    "Autonomous ReAct Agent")
    info.add_row("Started", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    info.add_row("Scope",   "[dim]Authorized target only[/dim]")
    console.print(info, justify="center")
    console.print()
    console.print(Rule(style=MATRIX_GREEN))
    console.print()


def print_step_header(step: int, total: int):
    console.print()
    console.print(Rule(
        f"[bold yellow] ⟳  STEP {step} of {total} [/bold yellow]",
        style="yellow"
    ))


def stream_thinking(text: str):
    """Print AI thinking token by token for hacker effect."""
    if not text.strip():
        return
    console.print(f"\n[{DIM_GRAY}]  ┌─ 🧠 AI THINKING {'─'*50}[/{DIM_GRAY}]")
    words = text.strip().split()
    line = "  │  "
    for word in words:
        line += word + " "
        if len(line) > 90:
            console.print(f"[{DIM_GRAY} italic]{line}[/{DIM_GRAY} italic]")
            line = "  │  "
    if line.strip():
        console.print(f"[{DIM_GRAY} italic]{line}[/{DIM_GRAY} italic]")
    console.print(f"[{DIM_GRAY}]  └{'─'*57}[/{DIM_GRAY}]")


def stream_decision(text: str):
    """Print agent decision with typewriter effect."""
    if not text.strip():
        return
    console.print()
    console.print(f"[{CYBER_CYAN}]  ┌─ 🤖 AGENT DECISION {'─'*48}[/{CYBER_CYAN}]")
    for line in text.strip().split("\n"):
        console.print(f"[{CYBER_CYAN}]  │[/{CYBER_CYAN}] [white]{line}[/white]")
    console.print(f"[{CYBER_CYAN}]  └{'─'*57}[/{CYBER_CYAN}]")


def print_tool_launch(tool_name: str, args: dict):
    emoji = TOOL_EMOJI.get(tool_name, "🔧")
    phase = PHASE_MAP.get(tool_name, "SCANNING")
    console.print()
    console.print(f"[bold {MATRIX_GREEN}]  ╔══ LAUNCHING TOOL ══════════════════════════════════╗[/bold {MATRIX_GREEN}]")
    console.print(f"[bold {MATRIX_GREEN}]  ║[/bold {MATRIX_GREEN}]  {emoji}  [bold white]{tool_name.upper()}[/bold white]  [{DIM_GRAY}]{phase}[/{DIM_GRAY}]")
    for k, v in args.items():
        console.print(f"[bold {MATRIX_GREEN}]  ║[/bold {MATRIX_GREEN}]  [{CYBER_CYAN}]{k}:[/{CYBER_CYAN}] [yellow]{v}[/yellow]")
    console.print(f"[bold {MATRIX_GREEN}]  ╚═══════════════════════════════════════════════════╝[/bold {MATRIX_GREEN}]")

    # Fake scanning animation
    with Live(Spinner("dots", text=f"[{MATRIX_GREEN}] Scanning...[/{MATRIX_GREEN}]"),
              refresh_per_second=10, transient=True):
        time.sleep(0.8)


def print_tool_result(tool_name: str, result: str):
    emoji = TOOL_EMOJI.get(tool_name, "📊")
    lines = result.strip().split("\n")
    colored = []
    for line in lines:
        if any(x in line for x in ["🚨", "CRITICAL", "MISSING"]):
            colored.append(f"[bold red]  {line}[/bold red]")
        elif any(x in line for x in ["⚠️", "⚠", "WARNING", "[403]"]):
            colored.append(f"[yellow]  {line}[/yellow]")
        elif any(x in line for x in ["✅", "PRESENT", "[200]"]):
            colored.append(f"[green]  {line}[/green]")
        elif any(x in line for x in ["🔍", "Detected", "Server"]):
            colored.append(f"[cyan]  {line}[/cyan]")
        else:
            colored.append(f"[dim]  {line}[/dim]")

    console.print(Panel(
        "\n".join(colored),
        title=f"[bold {MATRIX_GREEN}]{emoji}  {tool_name.upper()} — RESULTS[/bold {MATRIX_GREEN}]",
        border_style=MATRIX_GREEN,
        padding=(0, 2)
    ))


def print_progress_table(findings_log: list):
    t = Table(
        title=f"[bold {MATRIX_GREEN}]📊 SCAN PROGRESS[/bold {MATRIX_GREEN}]",
        box=box.SIMPLE_HEAVY,
        border_style=MATRIX_GREEN,
        show_lines=True,
        padding=(0, 1)
    )
    t.add_column("Step",   style="dim", width=6, justify="center")
    t.add_column("Phase",  style="cyan", width=24)
    t.add_column("Tool",   style="bold white", width=24)
    t.add_column("Status", style="green", width=10, justify="center")

    all_tools = list(PHASE_MAP.keys())
    done_tools = [fl["tool"] for fl in findings_log]

    for tool in all_tools:
        step_num = next((fl["step"] for fl in findings_log if fl["tool"] == tool), "-")
        status   = "[green]✅ Done[/green]" if tool in done_tools else "[dim]⏳ Pending[/dim]"
        emoji    = TOOL_EMOJI.get(tool, "🔧")
        console.print() if False else None
        t.add_row(str(step_num), PHASE_MAP[tool], f"{emoji} {tool}", status)

    console.print(t)


def run_agent():
    print_banner()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Start the security assessment of {TARGET_URL}. Begin with Step 1: robots_sitemap."}
    ]

    findings_log = []
    step = 0
    total_vulns = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

    while step < MAX_STEPS:
        step += 1
        print_step_header(step, MAX_STEPS)

        thinking_buf       = ""
        content_buf        = ""
        current_tool_calls = {}

        # ── Spinner while waiting for AI ──────────────────
        with Live(
            Spinner("aesthetic", text=f"[{CYBER_CYAN}] Waiting for AI response...[/{CYBER_CYAN}]"),
            refresh_per_second=10,
            transient=True
        ):
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOL_DEFS,
                tool_choice="required",
                temperature=0.3,
                top_p=0.7,
                max_tokens=4096,
                stream=True
            )

            for chunk in stream:
                if not getattr(chunk, "choices", None):
                    continue
                delta = chunk.choices[0].delta

                reasoning = getattr(delta, "reasoning_content", None)
                if reasoning:
                    thinking_buf += reasoning

                if delta.content:
                    content_buf += delta.content

                if delta.tool_calls:
                    for tc in delta.tool_calls:
                        idx = tc.index
                        if idx not in current_tool_calls:
                            current_tool_calls[idx] = {
                                "id": tc.id or f"call_{idx}",
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            }
                        if tc.id:
                            current_tool_calls[idx]["id"] = tc.id
                        if tc.function.name:
                            current_tool_calls[idx]["function"]["name"] += tc.function.name
                        if tc.function.arguments:
                            current_tool_calls[idx]["function"]["arguments"] += tc.function.arguments

        tool_calls_list = list(current_tool_calls.values())

        # Show AI thinking
        stream_thinking(thinking_buf)

        # ── Agent chose a tool ─────────────────────────────
        if tool_calls_list:
            if content_buf.strip():
                stream_decision(content_buf)

            messages.append({
                "role": "assistant",
                "content": content_buf or None,
                "tool_calls": tool_calls_list
            })

            # Only process FIRST tool (Llama limitation)
            tc = tool_calls_list[0]
            tool_name = tc["function"]["name"]
            try:
                args = json.loads(tc["function"]["arguments"])
            except:
                args = {}

            print_tool_launch(tool_name, args)

            result = TOOLS[tool_name](**args) if tool_name in TOOLS else f"Unknown tool: {tool_name}"
            findings_log.append({"step": step, "tool": tool_name, "args": args, "result": result})

            # Count vulns
            for sev in ["Critical", "High", "Medium", "Low"]:
                if sev.lower() in result.lower() or "🚨" in result:
                    total_vulns[sev] += result.lower().count(sev.lower())

            print_tool_result(tool_name, result)

            # Add tool result for ALL tool calls (even if we only ran first)
            for t in tool_calls_list:
                messages.append({
                    "role": "tool",
                    "tool_call_id": t["id"],
                    "content": result if t == tc else "Skipped - only one tool per step allowed"
                })

            # Show progress every 2 steps
            if step % 2 == 0:
                print_progress_table(findings_log)

        # ── No tool calls = final report ───────────────────
        else:
            console.print()
            console.print(Rule(f"[bold {MATRIX_GREEN}] 📋  FINAL REPORT [/bold {MATRIX_GREEN}]", style=MATRIX_GREEN))
            console.print()
            console.print(Markdown(content_buf))
            console.print()

            # Final progress table
            print_progress_table(findings_log)

            # Vuln summary
            vsummary = Table(
                title=f"[bold red]🚨 VULNERABILITY SUMMARY[/bold red]",
                box=box.HEAVY,
                border_style="red"
            )
            vsummary.add_column("Severity", style="bold", width=12)
            vsummary.add_column("Count", justify="center", width=8)
            vsummary.add_row("[bold red]Critical[/bold red]", str(total_vulns["Critical"]))
            vsummary.add_row("[yellow]High[/yellow]", str(total_vulns["High"]))
            vsummary.add_row("[cyan]Medium[/cyan]", str(total_vulns["Medium"]))
            vsummary.add_row("[dim]Low[/dim]", str(total_vulns["Low"]))
            console.print(vsummary)

            # Save report
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"report_{ts}.md"
            with open(report_path, "w") as f:
                f.write(f"# CyberSentry Bug Bounty Report\n")
                f.write(f"**Target:** {TARGET_URL}\n")
                f.write(f"**Date:** {datetime.now()}\n")
                f.write(f"**Model:** {MODEL}\n\n---\n\n")
                f.write(content_buf)
                f.write("\n\n---\n\n## Raw Tool Findings\n\n")
                for fl in findings_log:
                    f.write(f"### {fl['tool']}\n**Args:** {fl['args']}\n\n```\n{fl['result']}\n```\n\n")

            console.print(Panel(
                f"[bold {MATRIX_GREEN}]✅ Assessment Complete![/bold {MATRIX_GREEN}]\n\n"
                f"  [dim]Report:[/dim]  [cyan]{report_path}[/cyan]\n"
                f"  [dim]View  :[/dim]  [white]cat {report_path}[/white]\n"
                f"  [dim]Tools :[/dim]  [white]{len(findings_log)}/8 completed[/white]",
                title="[bold white on green] MISSION COMPLETE [/bold white on green]",
                border_style=MATRIX_GREEN,
                padding=(1, 4)
            ))
            return

    console.print(Panel("[bold red]⚠️  Max steps reached![/bold red]", border_style="red"))


if __name__ == "__main__":
    run_agent()