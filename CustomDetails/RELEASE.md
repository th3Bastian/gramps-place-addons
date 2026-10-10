# Release preparation

The source and runtime translation catalogs belong in `main`. Installable packages
and addon listings belong in `dist`, matching the existing repository layout.

## Validate and build

From the repository root:

```sh
python3 -m unittest discover -s CustomDetails/tests -v
python3 CustomDetails/tools/compile_translations.py --check
python3 CustomDetails/tools/build_release.py --base-ref dist
```

The last command creates an ignored local `release/gramps60/` directory containing
all existing packages from the chosen local ref, the new `CustomDetails.addon.tgz`,
and updated English and German listings. It neither switches branches nor commits
or pushes. Tests, development tools, caches and local configuration are excluded
from the installable CustomDetails package.

After editing translations, rebuild catalogs before the check:

```sh
python3 CustomDetails/tools/compile_translations.py
```

## Publish when authorized

1. Review and commit `CustomDetails/`, both repository READMEs and `.gitignore` to
   `main`, then push the source changes.
2. Fetch the current remote `dist` state and regenerate the release payload against
   that ref if it is newer, for example with `--base-ref origin/dist`.
3. Copy the prepared `gramps60/` payload into a checkout of `dist`, review its changes,
   commit and push. Keep the existing add-on packages and listing entries.
4. Optionally attach `CustomDetails.addon.tgz` to a GitHub Release for version 1.3.0.
5. Verify the addon appears under the project's existing Gramps 6.0 Addon Manager
   URL, and check a fresh installation in Gramps.

The GUI was used locally during development. Automated checks exercise numbering,
configuration, registration and catalogs without launching GTK; they do not replace
an Addon Manager installation check after publication.
