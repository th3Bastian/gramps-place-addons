"""Prepare a complete local Gramps 6.0 dist payload; never publish. GPL-2.0-or-later."""
import argparse
import ast
import gzip
import io
import json
import subprocess
import tarfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-ref', default='dist', help='Local ref containing existing Gramps listings/packages')
    parser.add_argument('--output', type=Path, default=REPO / 'release')
    args = parser.parse_args()
    # Read only Git-tracked release files. Keep the older addons byte-for-byte.
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', args.base_ref, '--', 'gramps60'], cwd=REPO, text=True).splitlines()
    if not paths:
        raise ValueError('The base ref has no gramps60 payload')
    for name in paths:
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe path in base ref')
        destination = args.output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(subprocess.check_output(['git', 'show', args.base_ref + ':' + name], cwd=REPO))
    registration = {}
    exec((PLUGIN / 'customdetails.gpr.py').read_text(), {'register': lambda *a, **kw: registration.update(kw), 'GRAMPLET': 10, 'STABLE': 3, '_': lambda message: message})
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as archive:
        for source in sorted(PLUGIN.rglob('*')):
            if not source.is_file():
                continue
            relative = source.relative_to(PLUGIN)
            if any(part in {'__pycache__', 'tests', 'tools', '.pytest_cache'} for part in relative.parts) or source.name == '.DS_Store' or source.suffix in {'.pyc', '.pyo'}:
                continue
            info = archive.gettarinfo(str(source), arcname='CustomDetails/' + relative.as_posix())
            info.mtime = 0; info.uid = 0; info.gid = 0; info.uname = ''; info.gname = ''; info.mode = 0o644
            with source.open('rb') as stream:
                archive.addfile(info, stream)
    archive_path = args.output / 'gramps60/download/CustomDetails.addon.tgz'
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_bytes(gzip.compress(buffer.getvalue(), mtime=0))
    descriptions = {'en': registration['description'], 'de': 'Personendetails mit Kekulé- und d’Aboville-Nummern sowie Bezugsperson'}
    for language in ('en', 'de'):
        listing = args.output / ('gramps60/listings/addons-' + language + '.json')
        entries = json.loads(listing.read_text())
        entries = [entry for entry in entries if entry['i'] != registration['id']]
        entries.append({'n': registration['name'], 'i': registration['id'], 't': 10, 'd': descriptions[language], 'v': registration['version'], 'g': registration['gramps_target_version'], 's': 3, 'z': archive_path.name, 'h': 'https://github.com/th3Bastian/gramps-place-addons/blob/main/CustomDetails/' + ('README.de.md' if language == 'de' else 'README.md')})
        listing.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n')
    print('Prepared local release payload: ' + str(args.output / 'gramps60'))


if __name__ == '__main__':
    main()
