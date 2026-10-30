import os
from pathlib import Path
import sys

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .documents import load_documents, search_documents

ROOT = Path(__file__).resolve().parent.parent
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False)


def create_server(directory: Path) -> FastMCP:
    docs = load_documents(directory)
    if not docs:
        raise ValueError('No numbered Markdown documents found')
    by_name = {doc['name']: doc for doc in docs}
    server = FastMCP('mcp-layer-boilerplate')

    @server.tool(annotations=READ_ONLY)
    def list_documents() -> list[dict]:
        """List available documents and their summaries."""
        return [{'name': doc['name'], 'uri': doc['uri'], 'feature_id': doc['metadata']['feature_id'],
                 'summary': doc['metadata']['summary']} for doc in docs]

    @server.tool(name='search_documents', annotations=READ_ONLY)
    def search_documents_tool(query: str = Field(min_length=1, max_length=500),
                              limit: int = Field(default=5, ge=1, le=20)) -> list[dict]:
        """Search titles, metadata and text using simple keyword matching."""
        return search_documents(docs, query, limit)

    @server.tool(annotations=READ_ONLY)
    def read_document(name: str = Field(min_length=1)) -> str:
        """Read a complete document by its exact listed filename."""
        if name not in by_name:
            raise ValueError(f'Document not found: {name}')
        return by_name[name]['text']

    for doc in docs:
        def register_resource(document):
            @server.resource(document['uri'], name=document['name'], description=document['metadata']['summary'], mime_type='text/markdown')
            def read_resource() -> str:
                return document['text']
        register_resource(doc)
    return server


def main() -> None:
    directory = Path(os.environ.get('MCP_DOCS_DIR', ROOT)).expanduser().resolve()
    try:
        create_server(directory).run(transport='stdio')
    except (ValueError, OSError) as error:
        print(f'Knowledge base error: {error}', file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
