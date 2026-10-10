"""Compile/check CustomDetails gettext catalogs without external tools. GPL-2.0-or-later."""
import argparse
import ast
import gettext
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_catalog(path):
    messages = {}
    entry = {}
    field = None
    def finish():
        if 'msgid' in entry:
            if entry['msgid'] in messages:
                raise ValueError('Duplicate message: ' + entry['msgid'])
            messages[entry['msgid']] = entry.get('msgstr', '')
    for line in path.read_text().splitlines() + ['']:
        line = line.strip()
        if not line:
            finish(); entry = {}; field = None
        elif line.startswith('#'):
            continue
        elif line.startswith(('msgid ', 'msgstr ')):
            field, value = line.split(' ', 1)
            entry[field] = ast.literal_eval(value)
        elif line.startswith('"') and field:
            entry[field] += ast.literal_eval(line)
        else:
            raise ValueError('Unsupported PO syntax: ' + line)
    return messages


def encode_catalog(messages):
    keys = sorted(messages)
    sources = [key.encode('utf-8') for key in keys]
    values = [messages[key].encode('utf-8') for key in keys]
    count = len(keys)
    base = 28 + 16 * count
    source_data = b''; value_data = b''; source_table = []; value_table = []
    for value in sources:
        source_table.append((len(value), base + len(source_data)))
        source_data += value + b'\0'
    for value in values:
        value_table.append((len(value), base + len(source_data) + len(value_data)))
        value_data += value + b'\0'
    header = struct.pack('<7I', 0x950412de, 0, count, 28, 28 + count * 8, 0, 0)
    return header + b''.join(struct.pack('<2I', *item) for item in source_table + value_table) + source_data + value_data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify committed MO files match PO sources')
    args = parser.parse_args()
    template = read_catalog(ROOT / 'po/template.pot')
    for language in ('de', 'en'):
        catalog = read_catalog(ROOT / ('po/' + language + '-local.po'))
        if catalog.keys() != template.keys() or any(not value for value in catalog.values()):
            raise ValueError('Incomplete translation catalog: ' + language)
        dest = ROOT / ('locale/' + language + '/LC_MESSAGES/addon.mo')
        binary = encode_catalog(catalog)
        if args.check:
            if dest.read_bytes() != binary:
                raise ValueError('Rebuild the translation catalog: ' + str(dest))
        else:
            dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(binary)
        with dest.open('rb') as stream:
            translation = gettext.GNUTranslations(stream)
        assert all(translation.gettext(key) == value for key, value in catalog.items() if key)
        print(language + ': ' + str(len(catalog) - 1) + ' messages verified')


if __name__ == '__main__':
    main()
