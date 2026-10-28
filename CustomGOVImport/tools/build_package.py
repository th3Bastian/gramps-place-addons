"""Build the runtime package with an explicit allowlist (no PO sources/tests)."""
import argparse
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def build(output):
    files = [ROOT / name for name in ('CustomGOVImport.py', 'CustomGOVImport.gpr.py',
             'README.md', 'README.de.md', 'CHANGELOG.md', 'CHANGELOG.de.md')]
    files += sorted((ROOT / 'locale').glob('*/LC_MESSAGES/addon.mo'))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output, 'w:gz', format=tarfile.PAX_FORMAT) as archive:
        for path in files:
            archive.add(path, arcname='CustomGOVImport/' + path.relative_to(ROOT).as_posix())
    with tarfile.open(output) as archive:
        assert len(archive.getmembers()) == len(files)
        for item, path in zip(archive.getmembers(), files):
            assert item.isfile()
            assert archive.extractfile(item).read() == path.read_bytes()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    build(parser.parse_args().output)
