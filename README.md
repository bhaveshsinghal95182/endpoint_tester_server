# 🧠 MCP Server – Endpoint Tester

An **MCP (Model Context Protocol)** server that equips AI agents with powerful tools for making HTTP requests. This server allows an agent to interact with any web API, from fetching simple data to executing complex, authenticated REST calls.

Built with `FastMCP`, it's lightweight, fast, and instantly compatible with any agent framework that supports the Model Context Protocol.

## ✨ Features

-   ⚡️ **High-Performance:** Built on `FastMCP` for rapid tool registration and low-latency execution.
-   🌐 **Versatile HTTP Tools:**
    -   `http_request`: For simple GET requests.
    -   `http_request_with_method`: For specifying any HTTP method (GET, POST, etc.).
    -   `detailed_http_request`: For full control over headers, body, query parameters, and timeouts.
-   📦 **Smart Response Handling:** Automatically parses the response body based on its `Content-Type`:
    -   `application/json` → Python `dict`
    -   `text/*` → Python `str`
    -   Other types (e.g., `image/png`) → Python `bytes`
-   🧩 **Agent-Ready:** Designed for plug-and-play use with LLM agents like Claude, or orchestration frameworks that can call MCP tools.

---

## 📂 Project Structure

```
ENDPOINT_TESTER_SERVER/
├── .venv/                  # Virtual environment managed by uv
├── .gitignore              # Files and directories ignored by Git
├── .python-version         # Specifies the project's Python version (e.g., for pyenv)
├── main.py                 # The main MCP server application and tool definitions
├── pyproject.toml          # Project metadata and dependencies for uv
├── README.md               # This documentation file
├── sourcecode.py           # Module with helper functions (e.g., send_http_request)
└── uv.lock                 # Pinned versions of dependencies for reproducible builds
```

---

## ⚙️ Setup and Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for fast package management and execution.

### Prerequisites

-   Python 3.8+ (as specified in your `.python-version` file).
-   [UV](https://github.com/astral-sh/uv) installed on your system.

### 1. Install Dependencies

From the project root directory, create a virtual environment and install the required packages using `uv`.

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On macOS / Linux
source .venv/bin/activate
# On Windows
.venv\Scripts\activate

# Install dependencies from pyproject.toml
uv pip install -e .
```
This command reads the `pyproject.toml` file, installs the listed dependencies, and creates the `uv.lock` file to ensure that every install is identical.

---

## 🚀 Usage

There are two primary ways to use this MCP server: running it locally for development or registering its tools directly with a compatible agent.

### 1. Running the Server Locally

This starts a local web server that exposes the tools over an HTTP API. This is useful for testing or when an agent needs to call tools over a network.

```bash
# Run the server using the mcp CLI, executed by uv
uv run mcp run main.py
```

The server will start, and you'll see output indicating the address it's running on (e.g., `http://127.0.0.1:8000`).

### 2. Making Tools Available to an Agent (e.g., Claude)

The `mcp` CLI can inspect your code and register the tools directly with a compatible LLM provider or agent framework. This is the most direct way to give an agent new capabilities without needing to run a separate server.

```bash
# Use the 'mcp install' command via uv
uv run mcp install main.py
```

This command will:
1.  Parse `main.py` without running a web server.
2.  Extract the definitions and docstrings for `http_request`, `http_request_with_method`, and `detailed_http_request`.
3.  Register them with your configured MCP-compatible agent or platform.

---

## 🛠️ Exposed Tools API

Here are the tools this server provides to an agent. The agent will call them using a structured format like JSON.

### 1. `http_request`

Sends a simple `GET` request. Best for quick data retrieval from a URL.

**Signature:**
```python
http_request(url: str) -> Union[str, Dict[str, Any], bytes]
```

**Example Agent Call:**
```json
{
  "tool": "http_request",
  "args": {
    "url": "https://api.github.com/zen"
  }
}
```

### 2. `http_request_with_method`

Sends a request with a specific HTTP method. Useful for simple non-GET actions like DELETE.

**Signature:**
```python
http_request_with_method(url: str, method: str)
```

**Example Agent Call:**
```json
{
  "tool": "http_request_with_method",
  "args": {
    "url": "https://httpbin.org/delete",
    "method": "DELETE"
  }
}
```

### 3. `detailed_http_request`

The most powerful tool for making fully customized HTTP requests. It supports headers, query parameters, a request body, and timeouts.

**Signature:**
```python
detailed_http_request(
    url: str,
    method: str = 'GET',
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[str, Dict[str, Any]]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Union[str, Dict[str, Any], bytes]
```

**Example Agent Call (POST with JSON Body and Headers):**
```json
{
  "tool": "detailed_http_request",
  "args": {
    "url": "https://httpbin.org/post",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer YOUR_API_KEY",
      "Content-Type": "application/json"
    },
    "data": {
      "user": "agent007",
      "action": "execute"
    },
    "timeout": 15
  }
}
```

---

## 🧩 Extending the Server

Adding new tools is simple. Define a new function in `main.py` and decorate it with `@mcp.tool()`. The MCP framework will automatically discover it.

For instance, to add a tool that finds your server's public IP using the helper in `sourcecode.py`:

**`main.py`:**
```python
from mcp.server.fastmcp import FastMCP
from typing import Union, Dict, Any, Optional
from sourcecode import send_http_request # Import from your helper module

mcp = FastMCP("Endpoint Tester")

# ... existing tools ...

@mcp.tool()
def get_ip_address() -> str:
    """Returns the public IP address of the server."""
    # Note: send_http_request is imported from sourcecode.py
    response = send_http_request(url="https://api.ipify.org?format=json")
    return response.get("ip", "Could not determine IP.")

if __name__ == "__main__":
    mcp.run()
```

---

## 📜 License

This project is open-source. Please add a license file (e.g., `LICENSE`) and specify it here. For example:

Licensed under the [MIT License](LICENSE).