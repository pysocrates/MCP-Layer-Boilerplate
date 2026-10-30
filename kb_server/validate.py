import os
from pathlib import Path
import sys
from .documents import load_documents
from .server import ROOT


def main():
    directory = Path(os.environ.get('MCP_DOCS_DIR', ROOT)).expanduser().resolve()
    try:
        docs = load_documents(directory)
        if not docs:
            raise ValueError('No numbered Markdown documents found')
        print(f'Validated {len(docs)} documents in {directory}')
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
