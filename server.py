#!/usr/bin/env python3
"""Read-only Kali Linux system audit MCP server."""

import json
import platform
import shutil
import socket
import subprocess
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kali-system-audit")

SECURITY_TOOLS = [
    "nmap", "wireshark", "tshark", "burpsuite", "msfconsole",
    "sqlmap", "nikto", "hydra", "john", "aircrack-ng",
    "gobuster", "ffuf", "nuclei", "whatweb", "wpscan",
    "enum4linux", "tcpdump", " netcat", "nc", "hashcat",
    "theHarvester", "searchsploit", "dirb", "dnsrecon",
]

def run_readonly(command: list[str]) -> str:
    """Run a fixed, read-only system command with a short timeout."""
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=10, check=False
        )
        output = result.stdout.strip()
        if result.stderr.strip() and not output:
            output = result.stderr.strip()
        return output or "(No output)"
    except FileNotFoundError:
        return f"Command not found: {command[0]}"
    except subprocess.TimeoutExpired:
        return f"Command timed out: {' '.join(command)}"
    except Exception as exc:
        return f"Unable to run command: {exc}"

@mcp.tool()
def get_os_version() -> str:
    """Get Linux distribution name and version."""
    os_release = Path("/etc/os-release")
    if os_release.exists():
        return os_release.read_text(encoding="utf-8", errors="replace").strip()
    return platform.platform()

@mcp.tool()
def get_kernel_version() -> str:
    """Get the currently running Linux kernel version."""
    return platform.release()

@mcp.tool()
def get_ip_addresses() -> str:
    """List IP addresses assigned to the system."""
    return run_readonly(["hostname", "-I"])

@mcp.tool()
def get_network_interfaces() -> str:
    """List network interfaces, state, and assigned addresses."""
    return run_readonly(["ip", "-br", "addr"])

@mcp.tool()
def get_installed_security_tools() -> str:
    """Check common security tools using installed command-line executables."""
    found = []
    missing = []
    for name in SECURITY_TOOLS:
        command_name = name.strip()
        if not command_name:
            continue
        path = shutil.which(command_name)
        if path:
            found.append({"tool": command_name, "path": path})
        else:
            missing.append(command_name)
    return json.dumps(
        {"installed": found, "not_found": missing},
        indent=2
    )

@mcp.tool()
def get_system_audit() -> dict[str, Any]:
    """Return a combined, read-only Kali Linux system audit report."""
    return {
        "os_version": get_os_version(),
        "kernel_version": get_kernel_version(),
        "ip_addresses": get_ip_addresses(),
        "network_interfaces": get_network_interfaces(),
        "security_tools": json.loads(get_installed_security_tools()),
    }

if __name__ == "__main__":
    # MCP stdio transport: Claude Desktop launches this process locally.
    mcp.run(transport="stdio")
