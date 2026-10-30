import asyncio
import os
from pathlib import Path
import sys
import tempfile
import unittest

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from kb_server.documents import load_documents, search_documents

ROOT = Path(__file__).resolve().parent.parent


class DocumentTests(unittest.TestCase):
    def test_search_and_validation(self):
        docs = load_documents(ROOT)
        self.assertEqual(search_documents(docs, 'middleware')[0]['name'], '01-architecture-and-routing.md')
        self.assertEqual(search_documents(docs, 'qzxunmatched'), [])
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, '01-broken.md').write_text('---\nfeature_id: broken\nsummary: Example\nrelated_docs: [missing.md]\n---\n# Example\n')
            with self.assertRaisesRegex(ValueError, 'missing file'):
                load_documents(Path(tmp))

    def test_stdio_client(self):
        async def exercise():
            parameters = StdioServerParameters(command=sys.executable, args=[str(ROOT / 'server.py')], cwd=ROOT,
                                               env={**os.environ, 'MCP_DOCS_DIR': str(ROOT)})
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    self.assertEqual({tool.name for tool in tools.tools}, {'list_documents', 'search_documents', 'read_document'})
                    result = await session.call_tool('search_documents', {'query': 'middleware'})
                    self.assertIn('01-architecture-and-routing.md', str(result.content))
                    missing = await session.call_tool('read_document', {'name': '../pyproject.toml'})
                    self.assertTrue(missing.isError)
                    resources = await session.list_resources()
                    self.assertEqual(len(resources.resources), 2)
                    resource = await session.read_resource('kb://docs/01-architecture-and-routing.md')
                    self.assertIn('# Architecture and Routing', resource.contents[0].text)
        asyncio.run(exercise())


if __name__ == '__main__':
    unittest.main()
