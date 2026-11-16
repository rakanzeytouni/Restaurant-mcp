# Restaurant MCP Server

<div align="center">

### Connecting AI Applications with Restaurant Management Tools

A Python-powered Model Context Protocol server built with FastMCP.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/Protocol-MCP-22C55E?style=for-the-badge)](https://modelcontextprotocol.io/)
[![FastMCP](https://img.shields.io/badge/Framework-FastMCP-blue?style=for-the-badge)](https://github.com/modelcontextprotocol/python-sdk)
[![Task](https://img.shields.io/badge/Task_1-Completed-success?style=for-the-badge)](#project-completion)

</div>

---

## Overview

Restaurant MCP Server is a Python-based implementation of the **Model Context Protocol (MCP)** using FastMCP.

It allows AI applications and MCP-compatible clients to interact with restaurant-related tools and services through a standardized protocol.

## Features

- Python-based MCP server.
- FastMCP integration.
- Restaurant-related tool integration.
- MCP-compatible client support.
- Local testing using MCP Inspector.

## Tech Stack

| Technology | Purpose |
|:---|:---|
| Python | Main programming language |
| MCP | Communication protocol |
| FastMCP | Server framework |
| MCP Inspector | Testing and debugging |

---

## Getting Started

### Requirements

Make sure you have installed:

- Python 3.10+
- pip
- Git

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/rakanzeytouni/Restaurant-mcp.git
cd Restaurant-mcp
```

**2. Create a virtual environment**

```powershell
python -m venv .venv
```

**3. Activate the environment**

```powershell
.venv\Scripts\Activate.ps1
```

**4. Upgrade pip**

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

**5. Install MCP SDK and CLI**

```bash
python -m pip install "mcp[cli]>=1.30.0,<2.0.0"
```

**6. Verify installation**

```bash
python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP installed successfully')"
```

Expected output:

```text
FastMCP installed successfully
```

---

## Running the Server

Make sure your virtual environment is activated.

Start the MCP Inspector:

```bash
mcp dev server.py
```

Alternatively, using `uv`:

```bash
uv run mcp dev server.py
```

The MCP Inspector allows you to connect to, inspect, and test the available server tools locally.

---
## Claude Desktop Configuration

To connect the Restaurant MCP Server to Claude Desktop, follow these steps.

### 1. Locate the Claude Configuration File

On Windows, the configuration file is located at:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

Open it using PowerShell:

```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

### 2. Add the MCP Server Configuration

Add the following configuration:

```json
{
  "mcpServers": {
    "restaurant-mcp": {
      "command": "C:\\Users\\User\\restaurant-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\User\\restaurant-mcp\\server.py"
      ]
    }
  }
}
```

**Important:** Replace `C:\\Users\\User\\restaurant-mcp` with the actual absolute path of your project directory if it is different.

### 3. Restart Claude Desktop

1. Save the configuration file.
2. Completely close Claude Desktop.
3. Reopen Claude Desktop.
4. Check the available MCP tools in Claude.

### Configuration Explanation

| Property | Description |
|---|---|
| `mcpServers` | Defines available MCP servers |
| `restaurant-mcp` | Server identifier |
| `command` | Python executable inside the virtual environment |
| `args` | Path to the MCP server entry point |

The configuration allows Claude Desktop to launch the Restaurant MCP Server directly using its Python virtual environment.



## Project Structure

```text
Restaurant-mcp/
│
├── server.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
```

| File | Description |
|:---|:---|
| `server.py` | FastMCP server implementation |
| `requirements.txt` | Project dependencies |
| `README.md` | Project documentation |
| `.gitignore` | Git ignore configuration |
| `.venv/` | Local virtual environment |

---

## Project Completion

<div align="center">

### <img src="https://img.shields.io/badge/TASK_01-COMPLETED-22C55E?style=for-the-badge" />

**Technical Task — NexLevr**

Task 1 has been completed and documented.

</div>

---

## Acknowledgments

Special thanks to **NexLevr** for providing this technical task and the opportunity to work on this project.

---


## License

No license has been specified for this project yet.

---

<div align="center">

**Restaurant MCP Server**

Built with Python & FastMCP.

</div>
