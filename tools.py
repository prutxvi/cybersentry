"""
CyberSentry Tools — All hacking tools the AI agent can call.
Each tool opens a NEW terminal window showing live execution!
"""
import subprocess, requests, socket, ssl, json, os, time
from datetime import datetime


# ── NEW TERMINAL LAUNCHER ──────────────────────────────────
def run_in_new_terminal(command: str, title: str = "CyberSentry") -> str:
    """Pops open a new xterm window and runs the command live inside it."""
    script_path = "/tmp/cybersentry_tool.sh"

    with open(script_path, "w") as f:
        f.write(f"""#!/bin/bash
clear
echo -e "\\e[32m"
echo "  ╔══════════════════════════════════════════════════════╗"
echo "  ║        🔥  CyberSentry — LIVE EXECUTION  🔥          ║"
echo "  ╠══════════════════════════════════════════════════════╣"
echo "  ║  Tool    : {title:<42}║"
echo "  ║  Command : {command[:42]:<42}║"
echo "  ║  Time    : $(date '+%Y-%m-%d %H:%M:%S')                        ║"
echo "  ╚══════════════════════════════════════════════════════╝"
echo -e "\\e[0m"
echo ""
echo -e "\\e[33m▶ RUNNING:\\e[0m {command}"
echo -e "\\e[32m──────────────────────────────────────────────────────\\e[0m"
echo ""
{command}
echo ""
echo -e "\\e[32m──────────────────────────────────────────────────────\\e[0m"
echo -e "\\e[32m✅  Execution complete! Closing in 20 seconds...\\e[0m"
sleep 20
""")
    os.chmod(script_path, 0o755)

    # Open new xterm window — green text on black (hacker style!)
    term_cmd = (
        f"xterm "
        f"-title '⚡ CyberSentry | {title}' "
        f"-bg black -fg '#00ff00' "
        f"-fa 'Monospace' -fs 11 "
        f"-geometry 100x35+900+100 "
        f"-e bash {script_path} &"
    )

    try:
        subprocess.Popen(term_cmd, shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        time.sleep(0.5)  # Let window open
    except Exception as e:
        pass  # Fallback to silent run

    # Capture output for AI agent regardless
    try:
        result = subprocess.run(
            command, shell=True,
            capture_output=True, text=True, timeout=120
        )
        output = result.stdout or result.stderr or "No output."
        return output[:3000]
    except subprocess.TimeoutExpired:
        return f"Command timed out: {command}"
    except Exception as e:
        return f"Error: {e}"


# ── TOOL 1: NMAP SCAN ──────────────────────────────────────
def run_nmap_scan(target: str, flags: str = "-sV -sC --open -T4") -> str:
    host = target.replace("https://","").replace("http://","").split("/")[0].split(":")[0]
    command = f"nmap {flags} {host}"
    return run_in_new_terminal(command, "NMAP PORT SCAN")


# ── TOOL 2: HTTP HEADERS ───────────────────────────────────
def check_http_headers(url: str) -> str:
    command = f"curl -s -I --max-time 10 {url}"
    run_in_new_terminal(command, "HTTP HEADERS CHECK")

    # Also do rich analysis for AI
    try:
        r = requests.get(url, timeout=10, allow_redirects=True)
        h = dict(r.headers)
        must_have = ["Content-Security-Policy","X-Frame-Options",
                     "X-Content-Type-Options","Strict-Transport-Security",
                     "Referrer-Policy","Permissions-Policy"]
        info_leak = ["Server","X-Powered-By","X-AspNet-Version","X-Generator"]
        lines = [f"Status: {r.status_code}", f"Final URL: {r.url}", ""]
        for k in must_have:
            lines.append(("✅ PRESENT: " if k in h else "⚠️  MISSING: ") + k + (f": {h[k]}" if k in h else ""))
        for k in info_leak:
            if k in h:
                lines.append(f"🚨 INFO LEAK: {k}: {h[k]}")
        return "\n".join(lines)
    except Exception as e:
        return f"header error: {e}"


# ── TOOL 3: SSL CHECK ──────────────────────────────────────
def check_ssl_tls(url: str) -> str:
    host = url.replace("https://","").replace("http://","").split("/")[0]
    command = f"echo | openssl s_client -connect {host}:443 -brief 2>/dev/null | head -20"
    run_in_new_terminal(command, "SSL/TLS CHECK")

    try:
        ctx = ssl.create_default_context()
        conn = ctx.wrap_socket(socket.socket(), server_hostname=host)
        conn.settimeout(10)
        conn.connect((host, 443))
        cert = conn.getpeercert()
        lines = [
            f"Subject: {cert.get('subject')}",
            f"Issuer: {cert.get('issuer')}",
            f"Valid until: {cert.get('notAfter')}",
            f"SSL version: {conn.version()}"
        ]
        exp = cert.get("notAfter","")
        if exp:
            d = (datetime.strptime(exp,"%b %d %H:%M:%S %Y %Z") - datetime.now()).days
            lines.append(("🚨 EXPIRES IN " if d < 30 else "✅ Expires in ") + f"{d} days")
        conn.close()
        return "\n".join(lines)
    except Exception as e:
        return f"ssl error: {e}"


# ── TOOL 4: DIRECTORY FUZZING ──────────────────────────────
def directory_fuzzing(url: str) -> str:
    base = url.rstrip("/")
    paths = [
        "admin","administrator","login","wp-admin","dashboard",
        "api","api/v1","api/v2","swagger","swagger-ui",
        ".env",".git",".git/config","config","config.php",
        "backup","backup.zip","backup.sql","db.sql",
        "robots.txt","sitemap.xml","phpinfo.php","test.php",
        "console","debug","logs","uploads","files",
        ".htaccess","web.config","Dockerfile","README.md","package.json"
    ]

    # Build a curl loop command to show in terminal
    curl_cmds = " && ".join([
        f'echo -n "Testing /{p}... " && curl -s -o /dev/null -w "%{{http_code}}\\n" --max-time 3 {base}/{p}'
        for p in paths[:15]  # First 15 in terminal
    ])
    run_in_new_terminal(f"bash -c '{curl_cmds}'", "DIRECTORY FUZZING")

    # Full fuzzing for AI
    found = []
    for p in paths:
        try:
            r = requests.get(f"{base}/{p}", timeout=5, allow_redirects=False)
            if r.status_code in [200, 301, 302, 403]:
                e = "🚨" if r.status_code == 200 else "⚠️"
                found.append(f"{e} [{r.status_code}] /{p}")
        except:
            pass
    return ("Directory Findings:\n" + "\n".join(found)) if found else "No sensitive paths found."


# ── TOOL 5: CORS CHECK ─────────────────────────────────────
def check_cors(url: str) -> str:
    command = (
        f'echo "Testing CORS..." && '
        f'curl -s -I -H "Origin: https://evil.com" --max-time 8 {url} | grep -i "access-control" || '
        f'echo "No CORS headers found"'
    )
    run_in_new_terminal(command, "CORS MISCONFIGURATION CHECK")

    origins = ["https://evil.com", "null", "https://attacker.com"]
    lines = []
    for o in origins:
        try:
            r = requests.get(url, headers={"Origin": o}, timeout=8)
            acao = r.headers.get("Access-Control-Allow-Origin", "not set")
            acac = r.headers.get("Access-Control-Allow-Credentials", "false")
            if acao == "*":
                lines.append(f"⚠️  Wildcard CORS with origin {o}")
            elif acao == o and acac.lower() == "true":
                lines.append(f"🚨 CRITICAL: Reflects {o} + credentials allowed!")
            elif acao == o:
                lines.append(f"⚠️  CORS reflects arbitrary origin: {o}")
            else:
                lines.append(f"✅ {o} → ACAO={acao}")
        except Exception as e:
            lines.append(f"error for {o}: {e}")
    return "CORS Results:\n" + "\n".join(lines)


# ── TOOL 6: ROBOTS & SITEMAP ───────────────────────────────
def check_robots_sitemap(url: str) -> str:
    base = url.rstrip("/")
    command = (
        f'echo "=== robots.txt ===" && curl -s --max-time 8 {base}/robots.txt && '
        f'echo "" && echo "=== sitemap.xml ===" && curl -s --max-time 8 {base}/sitemap.xml | head -30'
    )
    run_in_new_terminal(command, "ROBOTS & SITEMAP RECON")

    out = []
    for p in ["robots.txt", "sitemap.xml"]:
        try:
            r = requests.get(f"{base}/{p}", timeout=8)
            out.append(f"--- {p} [{r.status_code}] ---")
            if r.status_code == 200:
                out.append(r.text[:600])
        except Exception as e:
            out.append(f"--- {p} ERROR: {e} ---")
    return "\n".join(out)


# ── TOOL 7: TECH DETECTION ─────────────────────────────────
def tech_detection(url: str) -> str:
    command = (
        f'echo "=== Response Headers ===" && '
        f'curl -s -I --max-time 10 {url} && '
        f'echo "" && echo "=== Checking meta tags ===" && '
        f'curl -s --max-time 10 {url} | grep -i "generator\\|framework\\|powered" | head -10'
    )
    run_in_new_terminal(command, "TECH STACK DETECTION")

    try:
        r = requests.get(url, timeout=10)
        body = r.text.lower()
        found = []
        sv = r.headers.get("Server", "")
        px = r.headers.get("X-Powered-By", "")
        if sv: found.append(f"Server header: {sv}")
        if px: found.append(f"X-Powered-By: {px}")
        checks = {
            "WordPress": ["wp-content", "wp-includes"],
            "Laravel":   ["laravel", "csrf-token"],
            "Django":    ["csrfmiddlewaretoken"],
            "React":     ["data-reactroot", "__reactfiber"],
            "Angular":   ["ng-version", "ng-app"],
            "Vue.js":    ["__vue__", "v-app"],
            "Cloudflare":["cf-ray", "cloudflare"],
            "jQuery":    ["jquery"],
            "Bootstrap": ["bootstrap"],
            "PHP":       [".php"],
            "Drupal":    ["drupal"],
            "Joomla":    ["joomla"],
            "Next.js":   ["__next", "_next/static"],
            "Vercel":    ["vercel"],
        }
        for name, pats in checks.items():
            if any(p in body or p in sv.lower() or p in px.lower() for p in pats):
                found.append(f"🔍 {name} detected")
        return "Tech Stack:\n" + ("\n".join(found) if found else "Nothing detected")
    except Exception as e:
        return f"tech detect error: {e}"


# ── TOOL 8: COOKIES ────────────────────────────────────────
def check_cookies(url: str) -> str:
    command = (
        f'echo "=== Cookie Analysis ===" && '
        f'curl -s -I --max-time 10 {url} | grep -i "set-cookie" || '
        f'echo "No Set-Cookie headers found"'
    )
    run_in_new_terminal(command, "COOKIE SECURITY CHECK")

    try:
        r = requests.get(url, timeout=10)
        if not r.cookies:
            return "No cookies set."
        lines = []
        for c in r.cookies:
            flags = []
            if not c.secure:
                flags.append("🚨 Missing Secure flag")
            if not c.has_nonstandard_attr("HttpOnly"):
                flags.append("⚠️  Missing HttpOnly flag")
            samesite = c.get_nonstandard_attr("SameSite", "not set")
            flags.append(f"SameSite={samesite}")
            lines.append(f"Cookie '{c.name}': " + " | ".join(flags))
        return "\n".join(lines)
    except Exception as e:
        return f"cookie check error: {e}"


# ── Tool registry ──────────────────────────────────────────
TOOLS = {
    "nmap_scan":         run_nmap_scan,
    "check_headers":     check_http_headers,
    "check_ssl":         check_ssl_tls,
    "directory_fuzzing": directory_fuzzing,
    "check_cors":        check_cors,
    "robots_sitemap":    check_robots_sitemap,
    "tech_detection":    tech_detection,
    "check_cookies":     check_cookies,
}

# ── OpenAI function definitions ────────────────────────────
TOOL_DEFS = [
    {"type":"function","function":{
        "name":"nmap_scan",
        "description":"Run Nmap port scan on the target.",
        "parameters":{"type":"object","properties":{
            "target":{"type":"string"},
            "flags": {"type":"string"}
        },"required":["target"]}}},
    {"type":"function","function":{
        "name":"check_headers",
        "description":"Check HTTP security headers.",
        "parameters":{"type":"object","properties":{
            "url":{"type":"string"}
        },"required":["url"]}}},
    {"type":"function","function":{
        "name":"check_ssl",
        "description":"Check SSL/TLS certificate.",
        "parameters":{"type":"object","properties":{
            "url":{"type":"string"}
        },"required":["url"]}}},
    {"type":"function","function":{
        "name":"directory_fuzzing",
        "description":"Fuzz for hidden directories and files.",
        "parameters":{"type":"object","properties":{
            "url":{"type":"string"}
        },"required":["url"]}}},
    {"type":"function","function":{
        "name":"check_cors",
        "description":"Test CORS misconfiguration.",
        "parameters":{"type":"object","properties":{
            "url":{"type":"string"}
        },"required":["url"]}}},
    {"type":"function","function":{
        "name":"robots_sitemap",
        "description":"Fetch robots.txt and sitemap.xml.",
        "parameters":{"type":"object","properties":{
            "url":{"type":"string"}
        },"required":["url"]}}},
    {"type":"function","function":{
        "name":"tech_detection",
        "description":"Detect technology stack.",
        "parameters":{"type":"object","properties":{
            "url":{"type":"string"}
        },"required":["url"]}}},
    {"type":"function","function":{
        "name":"check_cookies",
        "description":"Inspect cookie security flags.",
        "parameters":{"type":"object","properties":{
            "url":{"type":"string"}
        },"required":["url"]}}},
]