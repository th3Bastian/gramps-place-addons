# Hide Duplicate Place Names

Hide Duplicate Place Names is a Gramps 6.0 add-on that combines immediately
consecutive identical place names in event displays when the current place type
is configured for suppression.

## Configuration

Open **Preferences → Place display**. Enter one place type per line. Entries
are trimmed, deduplicated, and sorted when the field loses focus. Matching is
case-sensitive and must exactly match the place type stored in Gramps.

## Compatibility

The add-on is registered as a `GENERAL` plug-in and loads only in the graphical
Gramps interface. It decorates the existing Preferences initializer so it can
coexist with the official Themes add-on. The event-display integration depends
on Gramps 6.0's place-display API; the registration deliberately targets 6.0.

## License

Copyright © 2026 Sebastian Klossek.

Licensed under the GNU General Public License, version 2 or later.
