# CustomGOVImport release history

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
