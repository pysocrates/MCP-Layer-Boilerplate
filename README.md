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

Add the following to your MCP host's configuration, replacing the paths with
absolute paths to your checkout. Configuration locations and formats vary by host.

```json
{
  "mcpServers": {
    "knowledge-base": {
      "command": "/absolute/path/to/MCP-Layer-Boilerplate/.venv/bin/python",
      "args": ["/absolute/path/to/MCP-Layer-Boilerplate/server.py"]
    }
  }
}
```

Reconnect the host after configuration changes. Running
`.venv/bin/python server.py` directly waits for an MCP client; there is no web UI.

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
