Restaurant MCP Server

A Model Context Protocol (MCP) server built with Python and FastMCP.

This project allows AI applications and MCP-compatible clients to interact with restaurant-related tools and services through the Model Context Protocol.

Requirements

Before installing the project, make sure you have:

- Python 3.10 or newer (Python 3.13 is supported in your current setup).
- pip (Python package installer).
- Git (to clone the repository).
- Node.js and npm (required for MCP Inspector).

Installation

1. Clone the repository

git clone https://github.com/rakanzeytouni/test-mcp.git
cd test-mcp

2. Create a virtual environment

Windows (PowerShell):

python -m venv .venv

Activate it:

.venv\Scripts\Activate.ps1

3. Install dependencies

Upgrade pip:

python -m ensurepip --upgrade
python -m pip install --upgrade pip

Install the MCP SDK and CLI:

python -m pip install "mcp[cli]>=1.30.0,<2.0.0"

4. Verify installation

Run:

python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP installed successfully')"

Expected output:

FastMCP installed successfully

Running the MCP Server

Make sure your virtual environment is activated.

Start the MCP Inspector:

mcp dev server.py

Alternatively, if you have uv installed:

uv run mcp dev server.py

The MCP Inspector will start locally and allow you to connect to, inspect, and test the server's available tools.

Project Structure

test-mcp/
│
├── server.py          # FastMCP server implementation
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
├── .gitignore         # Git ignored files
└── .venv/             # Local virtual environment (not committed)

Technologies

- Python
- Model Context Protocol (MCP)
- FastMCP
- MCP Inspector

Notes

- Always activate the virtual environment before installing dependencies or running the server.
- Do not upload the ".venv" directory to GitHub.
- Do not commit API keys, passwords, or other sensitive credentials.
- Keep dependencies documented in "requirements.txt".

License

Specify the project's license before distributing or reusing the code.
