# Working on this repository

This project serves a read-only Markdown knowledge base over MCP stdio. See the
[README](README.md) for setup and client connections, and the
[documentation index](00-index.md) for the example content.

- Preserve existing MCP tool names and the `feature_id` and `summary` metadata
  fields when changing the documentation convention.
- Treat generic examples as guidance, and verify system-specific claims against
  the relevant code, contracts, and tests.
- Run `.venv/bin/python -m kb_server.validate` after documentation changes.
- Run `.venv/bin/python -m unittest discover -s tests -v` after code changes.
- Do not print diagnostic output to stdout in the stdio server.
