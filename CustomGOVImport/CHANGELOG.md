# CustomGOVImport release history

## Version 1.2.2 – October 30, 2026

- Cleans up duplicate alternative names when the name, language and normalized
  date are confirmed by current GOV data. Matches legacy from/to dates against
  after/before dates and equal-bound spans against single dates. Different
  languages and historical periods are preserved; unconfirmed names are retained.
- Treats genuinely empty dates consistently for names and place relationships,
  preventing duplicates caused by different internal empty values after manual
  clearing, saving and reloading.
- The existing date sorting option now also sorts alternative names by date or
  span start, with undated names last. Ties remain stable; the primary name is
  not reordered.
- Also applies to successfully fetched parent places.

## Version 1.2.1

- Fixes duplicate place relationships following the switch from equal-bound
  date spans to single dates.
- Converts existing spans with identical boundaries only when the target and
  date are confirmed by current GOV data. Removes matching duplicates even
  with the update option disabled. Applies to year, month and day precision.
- Preserves spans with different start and end dates.

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
