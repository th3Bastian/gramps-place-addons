# CustomGOVImport

**[Deutsche Anleitung](README.de.md)**

CustomGOVImport is a Gramps 6.0 Gramplet for importing places from the
[Geschichtliches Ortsverzeichnis (GOV)](https://gov.genealogy.net/). It is an
independent fork of the GetGOV Gramplet and uses its own plugin ID and settings.

## Version 1.2.0

- Adds optional chronological sorting of place relationships, including existing
  references. For equal dates: before, exact date or span, then after. Undated
  references come last; calculation limits are not used.
- Adds optional updating of existing places from GOV, including the primary name,
  supplied place type and coordinates, URLs, and missing alternative names.
- Removes obsolete relationships only in update mode and only when the parent
  place's Gramps ID is confirmed by GOV. Unverified or non-GOV relationships
  remain; failed source requests never trigger removal.
- Imports open dates as before/after, preserving the date values. Closed spans
  remain from/to. GOV's uncertainty within a year or month is not fully represented
  by Gramps' boundary calculations; this is an accepted limitation.
- Corrects legacy from/to dates only for relationships matching the target and
  period in the current GOV response. Duplicate detection ignores input spelling
  for structured dates; unrelated relationships and their dates remain unchanged.
- Adds tooltips for all three checkboxes and updates German, Croatian, Dutch,
  European Portuguese and Slovak translations. Both new options default to off.

## Version 1.1.0

- Sorts excluded place types alphabetically when loading and saving.
- Reads the language directly from the selected Gramps place format; removes
  the obsolete `preferences.place-lang` compatibility path.
- Selects place-type translations in the format language, then German, then
  English, independently of the imported place name's language.
- Logs the format language, missing or invalid language settings, and fallback
  languages. New messages are translated into German, Croatian, Dutch,
  European Portuguese, and Slovak.

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
- reads the preferred place language directly from the selected Gramps place
  format, ignoring capitalization; place types fall back to German, then
  English when no label is available in that language; and
- provides localized date expressions and interface text for German,
  Croatian, Dutch, European Portuguese, and Slovak.

## Use

Add the **CustomGOVImport** Gramplet to a Gramps view, enter a GOV object ID
such as `object_12345`, and select **Get Place**.

Enable **Do not import parent places** to import only the requested object. Its
direct parent references are still inspected. A relationship is created when
the referenced place already exists in Gramps; otherwise the missing reference
is reported in the live log.

Enable **Update existing places with GOV data** to refresh the primary name,
place type and coordinates when supplied by GOV, and replace the URL list with
GOV URLs. Missing alternative names are added; existing alternative names,
notes and other unrelated record data are retained. The checkbox is off by
default.

With updating enabled, relationships absent from the current GOV response are
removed only when the parent place's Gramps ID is confirmed as a GOV object.
Relationships to other or unverified IDs remain unchanged. Failed source
requests do not update the place; failed ID checks never authorize removal.
Without updating, missing relationships are added without removing obsolete
ones. The legacy date correction described below applies in either mode.

Enable **Sort place relationships by date** to sort relationships during import.
The checkbox is off by default. When enabled, the complete reference list of the
place (including existing references) is sorted by the stated date or the start
of a span. For equal dates, before references precede spans and exact dates,
followed by after references. Undated references and text-only dates come last.
Equal sort keys retain their previous order. Calculation limits are not used.

Legacy open dates (from/to) are converted to after/before only when the target
place and period match a relationship in the current GOV response. Duplicate
cleanup is also limited to matching GOV relationships. Other existing
relationships retain their dates and are preserved, even if duplicated.

## Configuration

Open the Gramplet configuration and enter one GOV place type per line under
**Place types that should not be imported**. Matching is case-sensitive and
must exactly match the localized GOV place type. Blank lines and duplicate
entries are removed when the settings are saved. The list is sorted
alphabetically when loaded and saved, ignoring capitalization for sorting.

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
