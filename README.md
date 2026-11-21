# Kali Linux System Audit MCP

A small, read-only [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that lets an MCP-compatible AI assistant request basic system information from a Kali Linux machine.

## Features

- Kali/Linux distribution version
- Running Linux kernel version
- Assigned IP addresses
- Network interfaces and addresses
- Detection of common security-tool executables
- One combined system-audit report

## Requirements

- Kali Linux (or another Linux distribution)
- Python 3.10+
- Claude Desktop or another MCP-compatible client
- Internet access for installing the Python dependency

## 1. Download the project

```bash
git clone https://github.com/musammil-k/kali-system-audit-mcp.git
cd kali-system-audit-mcp
```

Replace `YOUR-USERNAME` with your GitHub username after you publish the repository. Alternatively, download the ZIP from GitHub and extract it.

## 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If `venv` is unavailable:

```bash
sudo apt update
sudo apt install -y python3-venv
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Test the server

```bash
python server.py
```

The server uses MCP's standard input/output transport. When started directly in a terminal, it may appear to wait silently; that is normal. Press `Ctrl+C` to stop it.

## 5. Configure Claude Desktop

First, find the absolute path to this project:

```bash
pwd
```

Find the Python executable inside the virtual environment:

```bash
which python
```

Open Claude Desktop's MCP configuration file. Common locations:

- Linux: `~/.config/Claude/claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration. Replace both example paths with the real absolute paths from your Kali machine.

```json
{
  "mcpServers": {
    "kali-system-audit": {
      "command": "/ABSOLUTE/PATH/TO/kali-system-audit-mcp/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/kali-system-audit-mcp/server.py"
      ]
    }
  }
}
```

Save the file and fully restart Claude Desktop. Open its MCP/tools area and check that `kali-system-audit` is connected.

> If Claude Desktop runs on a different computer, this local configuration runs the server on the computer where Claude Desktop is installed. To audit Kali remotely, you need a separately secured remote MCP setup; do not expose an unauthenticated MCP server to the network.

## 6. Try these prompts in Claude

```text
Use the Kali System Audit MCP tools to check my system.
Show OS version, kernel version, IP addresses, network interfaces,
and installed security tools. Explain each result in simple English.
```

Or:

```text
Run the combined system audit and summarize the results.
```

## Available MCP tools

| Tool | What it reports |
|---|---|
| `get_os_version` | Distribution details from `/etc/os-release` |
| `get_kernel_version` | Running kernel version |
| `get_ip_addresses` | IP addresses from `hostname -I` |
| `get_network_interfaces` | Interface state and addresses from `ip -br addr` |
| `get_installed_security_tools` | Common security-tool executables found in PATH |
| `get_system_audit` | Combined report |

## Security and privacy notes

- The tools are intended to be read-only.
- No commands are accepted from the AI assistant as arbitrary shell input.
- No files are uploaded and no scan is started.
- The tool list checks executable availability in `PATH`; it is not a complete inventory of every installed package.
- Review output before sharing it publicly. IP addresses, hostnames, usernames, and network details can be sensitive.
- Only use this project on systems you own or are authorized to administer.

## Troubleshooting

**MCP server does not appear in Claude**

1. Confirm the paths in the JSON are absolute and correct.
2. Confirm the virtual environment exists and contains the `mcp` package:
   ```bash
   .venv/bin/python -m pip show mcp
   ```
3. Validate the JSON syntax:
   ```bash
   python -m json.tool ~/.config/Claude/claude_desktop_config.json
   ```
4. Fully quit and restart Claude Desktop.
5. Check Claude Desktop's MCP/server logs for the exact error.

**`ip` command not found**

Install the package that provides it:

```bash
sudo apt update
sudo apt install -y iproute2
```

## License

MIT. See [LICENSE](LICENSE).
