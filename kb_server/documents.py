from pathlib import Path
import re
from urllib.parse import quote

import yaml


def load_documents(directory: Path, source_root: Path | None = None) -> list[dict]:
    directory = Path(directory).resolve()
    source_root = Path(source_root).resolve() if source_root is not None else directory
    files = {p.name for p in directory.iterdir() if p.is_file() and not p.is_symlink()}
    names = sorted(name for name in files if re.match(r'^\d.*\.md$', name))
    documents = []
    ids = set()
    for name in names:
        text = (directory / name).read_text(encoding='utf-8')
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
        if not match:
            raise ValueError(f'{name}: missing YAML frontmatter')
        try:
            metadata = yaml.safe_load(match.group(1))
        except yaml.YAMLError as error:
            raise ValueError(f'{name}: invalid YAML: {error}') from error
        if not isinstance(metadata, dict):
            raise ValueError(f'{name}: frontmatter must be a mapping')
        for field in ('feature_id', 'summary'):
            if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                raise ValueError(f'{name}: {field} must be a non-empty string')
        for field in ('keywords', 'tasks', 'related_docs', 'source_files'):
            value = metadata.get(field, [])
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise ValueError(f'{name}: {field} must be an array of strings')
        if metadata['feature_id'] in ids:
            raise ValueError(f"{name}: duplicate feature_id {metadata['feature_id']}")
        ids.add(metadata['feature_id'])
        for ref in metadata.get('related_docs', []):
            if ref not in files:
                raise ValueError(f'{name}: related_docs references missing file {ref}')
        for ref in metadata.get('source_files', []):
            relative = Path(ref)
            if not ref.strip() or relative.is_absolute() or '..' in relative.parts:
                raise ValueError(f'{name}: source_files requires a relative path within the source root: {ref}')
            target = (source_root / relative).resolve()
            if not target.is_relative_to(source_root) or not target.is_file():
                raise ValueError(f'{name}: source_files references missing or unsafe file {ref}')
        documents.append({'name': name, 'metadata': metadata, 'text': text,
                          'uri': f'kb://docs/{quote(name, safe="")}'} )
    return documents


def search_documents(documents: list[dict], query: str, limit: int = 5) -> list[dict]:
    terms = set(re.findall(r'[\w-]+', query.lower()))
    results = []
    for doc in documents:
        metadata = doc['metadata']
        title = f"{doc['name']} {metadata['feature_id']} {metadata['summary']}".lower()
        tags = ' '.join(metadata.get('keywords', []) + metadata.get('tasks', [])).lower()
        body = doc['text'].lower()
        score = sum(4 * (term in title) + 2 * (term in tags) + (term in body) for term in terms)
        if score:
            results.append({'name': doc['name'], 'uri': doc['uri'], 'feature_id': metadata['feature_id'],
                            'summary': metadata['summary'], 'score': score})
    return sorted(results, key=lambda item: (-item['score'], item['name']))[:limit]
