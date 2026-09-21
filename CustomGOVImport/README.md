# CustomGOVImport

**[Deutsche Anleitung](README.de.md)**

CustomGOVImport is a Gramps 6.0 Gramplet for importing places from the
[Geschichtliches Ortsverzeichnis (GOV)](https://gov.genealogy.net/). It is an
independent fork of the GetGOV Gramplet and uses its own plugin ID and settings.

## Features

- imports a GOV place and its outgoing `isPartOf` and `isLocatedIn`
  relationships;
- follows parent relationships even when an intermediate place already exists
  in the Gramps database;
- can import only the requested place and connect it to parent places that
  already exist;
- excludes configured place types from import while continuing to inspect
  their parent relationships;
- shows import progress and skipped references in a live log;
- reads the preferred place language from Gramps and handles the setting
  without regard to capitalization; and
- provides localized date expressions and interface text for German,
  Croatian, Dutch, European Portuguese, and Slovak.

## Use

Add the **CustomGOVImport** Gramplet to a Gramps view, enter a GOV object ID
such as `object_12345`, and select **Get Place**.

Enable **Do not import parent places** to import only the requested object. Its
direct parent references are still inspected. A relationship is created when
the referenced place already exists in Gramps; otherwise the missing reference
is reported in the live log.

## Configuration

Open the Gramplet configuration and enter one GOV place type per line under
**Place types that should not be imported**. Matching is case-sensitive and
must exactly match the localized GOV place type. Blank lines and duplicate
entries are removed when the settings are saved.

When the requested object itself is excluded, it is not added to Gramps. In a
normal import, its parent relationships are still followed so eligible parent
places can be imported.

The blacklist is shared by all CustomGOVImport Gramplet instances and is saved
only when the configuration's **Save** button is used.

## Compatibility

The add-on targets Gramps 6.0 and requires network access to
`gov.genealogy.net`.

## Origin and license

CustomGOVImport is based on GetGOV 1.0.25 by Nick Hall and Gary Griffin from
the [Gramps add-ons project](https://github.com/gramps-project/addons-source/tree/maintenance/gramps60/GetGOV).

Copyright © 2015 Nick Hall  
Copyright © 2024 Gary Griffin  
Copyright © 2026 Sebastian Klossek

Licensed under the GNU General Public License, version 2 or later.
