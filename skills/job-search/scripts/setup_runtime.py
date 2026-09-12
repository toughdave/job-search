#!/usr/bin/env python3
"""Install and verify this workspace's private document runtime. Python 3.9+."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import venv

import workspace as ws

SKILL = Path(__file__).resolve().parents[1]
REQUIREMENTS = SKILL / 'requirements-documents.txt'


def run(command):
    result = subprocess.run([str(x) for x in command], capture_output=True,
                            text=True, encoding='utf-8', errors='replace')
    ws.require(result.returncode == 0,
               'Runtime command failed; setup is incomplete.\n' + result.stderr[-4000:])
    return result.stdout


def probe(scratch):
    """Exercise actual installed imports, serialization, text extraction and rendering."""
    from importlib.metadata import version
    from zoneinfo import ZoneInfo
    import re
    import docx
    import pypdf
    import pypdfium2
    import documents
    versions = {}
    for line in REQUIREMENTS.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        match = re.fullmatch(r'([\w-]+)(==|>=)([\d.]+)', line)
        ws.require(match is not None, 'Unsupported dependency declaration: ' + line)
        name, operator, expected = match.groups()
        actual = version(name)
        numeric = lambda value: tuple(int(part) for part in value.split('.'))
        ws.require(actual == expected if operator == '==' else numeric(actual) >= numeric(expected),
                   'Dependency version differs from this skill: ' + name)
        versions[name] = actual
    ZoneInfo('America/Toronto')
    ZoneInfo('Asia/Kolkata')
    with tempfile.TemporaryDirectory(prefix='runtime-check-', dir=scratch) as temp:
        temp = Path(temp)
        model = json.loads((SKILL / 'assets/document-example.json').read_text(encoding='utf-8'))
        documents.build_docx(model, temp / 'check.docx')
        documents.build_pdf(model, temp / 'check.pdf')
        ws.require(model['name']['text'] in '\n'.join(p.text for p in docx.Document(temp / 'check.docx').paragraphs),
                   'DOCX readback failed.')
        reader = pypdf.PdfReader(temp / 'check.pdf')
        ws.require(model['name']['text'] in reader.pages[0].extract_text(), 'PDF readback failed.')
        with pypdfium2.PdfDocument(str(temp / 'check.pdf')) as pdf:
            page = pdf[0]
            bitmap = page.render(scale=1)
            picture = bitmap.to_pil()
            picture.save(temp / 'check.png')
            ws.require(picture.width > 0 and picture.height > 0, 'PDF rendering failed.')
            picture.close()
            bitmap.close()
            page.close()
    return {'packages': versions, 'checks': ['imports', 'timezone_data', 'docx_readback',
            'pdf_text', 'pdf_render'], 'docx_visual_review': 'requires_available_renderer',
            'web_and_scheduler': 'check_in_host', 'candidate_script_fonts': 'check_with_actual_text'}


def setup(value, check_only=False, uv=None):
    ws.require(sys.version_info >= (3, 9), 'Python 3.9 or newer is required.')
    root = ws.checked_root(value)
    state = ws.load(root)
    for parent in [root, *root.parents]:
        ws.require(not (parent / 'SKILL.md').exists() and not (parent / 'skills/job-search/SKILL.md').exists(),
                   'Runtime must be outside the installed skill and public source checkout.')
    runtime = ws.inside(root, '.runtime')
    marker = ws.inside(root, '.runtime/setup-owner.json')
    target = ws.inside(root, '.runtime/job-search-venv')
    record = ws.inside(root, '.runtime/runtime.json')
    fingerprint = hashlib.sha256(REQUIREMENTS.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    if check_only:
        ws.require(marker.is_file() and record.is_file(), 'Run setup first; no verified private runtime is recorded.')
    if marker.exists():
        saved = json.loads(marker.read_text(encoding='utf-8'))
        ws.require(saved.get('workspace_id') == state['workspace_id'] and saved.get('format') == 1,
                   'This runtime belongs to a different workspace or format.')
    else:
        ws.require(not target.exists() and not record.exists(),
                   'Existing runtime files are not owned by this setup. Preserve them and choose a fresh runtime location.')
        runtime.mkdir(exist_ok=True)
        ws.atomic_json(marker, {'format': 1, 'workspace_id': state['workspace_id']})
    # Separate from the workspace write lock: package installation never holds a state lock.
    lock = ws.inside(root, '.runtime/setup.lock')
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ws.WorkspaceError('Runtime setup is already running or left a lock. Verify its process has stopped before removing only .runtime/setup.lock.')
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            json.dump({'pid': os.getpid(), 'created_at': ws.now()}, stream)
        interpreter = target / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        if check_only:
            prior = json.loads(record.read_text(encoding='utf-8'))
            ws.require(prior.get('requirements_sha256') == fingerprint, 'Dependencies changed; run setup to update this private runtime.')
            ws.require(prior.get('status') == 'runtime-ready', 'The previous setup is incomplete; run it again.')
        else:
            ws.atomic_json(record, {'status': 'installing', 'workspace_id': state['workspace_id']})
            if not interpreter.is_file():
                if uv:
                    run([uv, 'venv', '--seed', '--allow-existing', '--python', sys.executable, target])
                else:
                    venv.EnvBuilder(with_pip=True, symlinks=False).create(target)
            run([interpreter, '-I', '-m', 'pip', '--isolated', 'install', '--disable-pip-version-check',
                 '--only-binary=:all:', '--no-input', '--cache-dir', runtime / 'cache', '-r', REQUIREMENTS])
        ws.require(interpreter.is_file(), 'Private interpreter is missing; run setup to repair it.')
        result = json.loads(run([interpreter, '-B', Path(__file__).resolve(), '--probe', runtime]))
        result.update(status='runtime-ready', python=str(interpreter), workspace_id=state['workspace_id'],
                      requirements_sha256=fingerprint, checked_at=ws.now())
        ws.atomic_json(record, result)
        return result
    except Exception:
        ws.atomic_json(record, {'status': 'incomplete', 'workspace_id': state['workspace_id']})
        raise
    finally:
        lock.unlink()


def main():
    ws.configure_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--uv', help='Existing uv executable, for a Python without working venv/ensurepip.')
    parser.add_argument('--probe', help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        result = probe(args.probe) if args.probe else setup(args.workspace, args.check_only, args.uv)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ws.WorkspaceError, OSError, ValueError, ImportError, subprocess.SubprocessError) as error:
        print('Runtime setup incomplete: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
