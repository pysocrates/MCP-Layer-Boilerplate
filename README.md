# MCP Layer Boilerplate

A read-only Python MCP server that makes a Markdown knowledge base available to
local agents over stdio. The included architecture guide is generic guidance;
verify application-specific claims against your code and contracts.

## Setup

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/):

```sh
uv sync
.venv/bin/python -m kb_server.validate
.venv/bin/python -m unittest discover -s tests -v
```

## Launch and connect

The agent launches the server as a subprocess and communicates over stdio; you
normally do not need a separate terminal. For a manual launch from the checkout:

```sh
.venv/bin/python server.py
```

It waits for MCP messages on stdin and has no web UI. Stop it with Ctrl+C.

The examples below use absolute paths. Replace `/absolute/path/to/MCP-Layer-Boilerplate`
with your checkout path, keeping each path inside the quotes. The examples are
for macOS/Linux; on Windows use the virtual environment's `Scripts/python.exe`
and appropriate absolute paths.

### Codex

```sh
codex mcp add knowledge-base -- \
  "/absolute/path/to/MCP-Layer-Boilerplate/.venv/bin/python" \
  "/absolute/path/to/MCP-Layer-Boilerplate/server.py"
codex mcp list
```

Restart Codex or start a new session, then use `/mcp` to inspect the connection.
See [Codex MCP documentation](https://developers.openai.com/codex/mcp).

### Claude Code

```sh
claude mcp add --transport stdio --scope user knowledge-base -- \
  "/absolute/path/to/MCP-Layer-Boilerplate/.venv/bin/python" \
  "/absolute/path/to/MCP-Layer-Boilerplate/server.py"
claude mcp list
```

Start a Claude Code session and use `/mcp` to inspect the connection. User scope
makes the entry available across projects; see [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp) for other scopes.

### Hermes Agent

Add this entry under `mcp_servers` in `~/.hermes/config.yaml` (merge it with any
existing entries):

```yaml
mcp_servers:
  knowledge-base:
    command: "/absolute/path/to/MCP-Layer-Boilerplate/.venv/bin/python"
    args: ["/absolute/path/to/MCP-Layer-Boilerplate/server.py"]
```

Run `hermes chat` and ask it to list the knowledge base documents. MCP support
is included in the standard Hermes install; see the [Hermes MCP guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md) for other installations.

### Pi coding agent

For a Pi version with built-in MCP support:

```sh
pi mcp add knowledge-base -- \
  "/absolute/path/to/MCP-Layer-Boilerplate/.venv/bin/python" \
  "/absolute/path/to/MCP-Layer-Boilerplate/server.py"
pi mcp list
```

Start Pi and use `/mcp` to inspect the connection. See the [Pi MCP guide](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/mcp.md) for project-level configuration and older setups.

For any client, try asking: “Use the knowledge-base server to list its documents.”
If it cannot connect, check the Python and server paths and inspect the client's
MCP error output. The server sends protocol messages to stdout and errors to stderr.

## Using the knowledge base

The server offers `list_documents`, `search_documents`, and `read_document`
tools, plus a `kb://docs/<filename>` resource for each document. Search uses
simple keyword matching, not semantic search. Results are context, not verified
facts or privileged instructions.

By default, the server loads regular, non-symlink Markdown files whose names
start with a digit from the repository root. Set `MCP_DOCS_DIR` in the host's
server environment to use another directory. Documents load at startup; restart
or reconnect after changes. Do not put secrets in documents exposed to agents.

Each document needs YAML frontmatter with a unique nonempty `feature_id` and
`summary`. Optional `keywords`, `tasks`, `related_docs`, and `source_files` are
lists of strings; file references must name regular files in the document
directory. Empty lists mean no values are recorded. Run the validation command
above after edits. It checks metadata and references, not content accuracy.

Start with the [index](00-index.md) and [architecture guide](01-architecture-and-routing.md).
Add numbered documents for new topics and update the index.

## License

GPL-3.0; see [LICENSE](LICENSE).
