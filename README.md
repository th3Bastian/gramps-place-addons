# Gramps Place Addons

Independent Gramps add-ons for working with places.

**[Deutsche Anleitung](README.de.md)**

## Available add-ons

| Add-on | Status | Purpose |
| --- | --- | --- |
| [Hide Duplicate Place Names](HideDuplicatePlaceNames/) | Stable for Gramps 6.0 | Combines immediately consecutive identical place names in event displays for configured place types. |

## Install through Gramps Addon Manager

The add-ons are installed from this project's release branch. In Gramps 6.0:

1. Open **Edit → Addon Manager**.
2. Select the **Projects** tab and click **+**.
3. Enter a name such as `Bastian's Gramps Place Addons`.
4. Use this URL:

   ```text
   https://raw.githubusercontent.com/th3Bastian/gramps-place-addons/dist/gramps60
   ```

5. Return to the **Addons** tab and refresh the list.
6. Search for the add-on, select **Install**, then restart Gramps.

The project URL must end in `gramps60`; it is specifically for Gramps 6.0.

## Hide Duplicate Place Names

This add-on affects only the display of place hierarchies in event and narrative
views. It does not modify your family tree or any place records.

Open **Preferences → Place display** after installation. Add one place type per
line. Place names are combined only when all of the following are true:

- two entries with the same name are immediately consecutive;
- the later entry's place type appears in the configured list; and
- capitalization exactly matches the place type stored in Gramps.

Blank entries and duplicates are removed automatically. Leading and trailing
spaces are removed, and entries are sorted alphabetically when the field loses
focus. A value such as `City (municipality)` is supported unchanged.

## Updating and troubleshooting

When a later version is published, Gramps can discover it through the same
project URL in the Addon Manager. Install the update and restart Gramps.

If an add-on does not appear:

- confirm the project URL exactly matches the Gramps major version;
- refresh the add-on list; and
- check the **Plugin Manager** for loading errors.

Do not keep a manually copied version of the same add-on in the user plugin
directory while testing an Addon Manager installation; both versions use the
same plugin ID.

## Development

The `main` branch contains source code, tests, and translation sources. The
`dist` branch contains the packaged add-ons and listings consumed by Gramps
Addon Manager. Releases are tested before being added to `dist`.

## Feedback and license

Please report problems or suggestions through the repository's
[Issues](https://github.com/th3Bastian/gramps-place-addons/issues).

Each add-on documents its copyright and license. Hide Duplicate Place Names is
licensed under GPL-2.0-or-later.
