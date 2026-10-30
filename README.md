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

## Writing and maintaining documents

Start with the [index](00-index.md), [architecture guide](01-architecture-and-routing.md),
and [topic template](templates/topic.md). Copy the template into the document
directory with a filename such as `02-orders.md`, give it a unique ID, and add
a link to the index. Keep each document focused and remove sections that do not
apply. Use [AGENTS.md](AGENTS.md) for repository-wide agent instructions.

The frontmatter is this project's convention, not an MCP standard:

- Required: nonempty string `feature_id` (unique across documents) and `summary`.
- Optional: `keywords` and `tasks` are lists of search phrases; `related_docs`
  lists filenames in the document directory; `source_files` lists paths relative
  to the source root. Omit fields that have no recorded values.
- Optional `owner` and quoted `last_verified` (for example, `"2026-10-30"`)
  are maintainer notes. Review them as part of your team's documentation process;
  the server does not enforce ownership or freshness.
- Other fields are allowed for older documents or local conventions, but the
  server does not interpret them as filters or authority signals.

By default, the source root is the document directory. When documentation and
application code live in separate directories, set both `MCP_DOCS_DIR` and
`MCP_SOURCE_ROOT` to absolute paths in the client's server environment. For
example, use `/project/docs` and `/project` respectively, then a source reference
can be `src/orders.py`. Paths must be relative, stay inside the source root, and
resolve to existing files. Source references are checked for existence; the
server does not serve their contents. `related_docs` remains a list of filenames
in the document directory.

Run `.venv/bin/python -m kb_server.validate` after changes; set the same environment
variables when validating a separate knowledge base. Validation checks metadata,
unique IDs, and references, but cannot verify whether claims are correct or
current. Link important claims to their source code, tests, contracts, or design
decisions, and review them when those sources change. Markdown links and index
coverage are not validated automatically.

### Migrating an older knowledge base

Existing documents with `feature_id` and `summary` remain supported; no bulk
migration is required. Preserve IDs and filenames used by clients, remove unused
fields gradually, and replace self-references in `source_files` with useful
sources. Set `MCP_SOURCE_ROOT` before adding application-relative paths. Empty
lists mean no values are recorded, not that a capability or permission is absent.

## License

GPL-3.0; see [LICENSE](LICENSE).
