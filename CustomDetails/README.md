# CustomDetails — Version 1.3.0

**[Deutsche Anleitung](README.de.md)**

CustomDetails is a Gramplet for Gramps 6.0 based on the original Person Details
Gramplet from Gramps 6.0.8. It retains the original photo, names, parents and life
events and adds selected person attributes, a reference person, kinship, Kekulé
numbers and d’Aboville numbers. Original author credits are retained.

License: GNU General Public License, version 2 or later.

## Installation

Install the complete `CustomDetails` folder in the Gramps 6.0 user plugin directory.
Restart Gramps, then choose **CustomDetails** from **Add a Gramplet** in a person
view's sidebar or bottom bar. It can replace the original Details Gramplet.

The photo is aligned to the top, with 5 pixels of space above and below. Additional
rows appear below the original detail fields and selected person attributes.

## Reference person and kinship

The Gramps **home person** is the reference person, displayed with its name and
Gramps ID. Use Gramps' **Set Home Person** action to change it. A notice is shown
when no home person is set.

Kinship describes the selected person relative to the home person, using Gramps'
localized relationship calculator and configured generation search depth. Gramps
selects the most relevant relationship if several exist. Failure to find a
relationship within the search depth does not prove that the people are unrelated.

## Kekulé numbering

The home person is **1**. For a person numbered *n*, their father is **2n** and their
mother **2n+1**. All valid numbers are shown for ancestors occurring along multiple
paths. Unknown parents leave gaps. Non-ancestors receive an explanatory message.

Numbering follows each person's **main parent family**, matching the original
Details parent display. Adoptive or foster parents are included if their family is
the main parent family. This may differ from the Ahnentafel report, which searches
for birth relationships.

## d’Aboville numbering

The home person is **1**, their children are **1.1**, **1.2**, etc., and subsequent
generations have numbers such as **1.2.1**. Children are numbered across all of a
parent's families in Gramps' stored family and child order, as in the detailed
descendant report. Birth dates are not used to sort them.

All recorded child relationships, including adoption and foster relationships,
are included. A spouse receives no descendant number solely through a partnership.
All valid descent paths are displayed, sorted by numeric path. Non-descendants
receive an explanatory message.

## Configuration

Open the Gramplet configuration, in the same way as for CustomGOVImport. Four
independent checkboxes control the additional rows:

- **Show reference person**
- **Show kinship**
- **Show Kekulé number**
- **Show d’Aboville number**

All four are enabled initially. Hidden kinship and numbering fields are not
computed. There are no additional duplicate labels before the checkboxes.

Under **Show the following attributes**, enter one attribute type per line,
using the type name displayed in Gramps. Only listed types are shown; an empty list
hides all person attributes. Outer whitespace, blank lines and duplicate types are
removed, ignoring case. The list is sorted alphabetically according to the current
locale when loaded and saved. After **Save**, the editor immediately shows the
cleaned, sorted list. Repeated values remain separate rows in their stored order.

Before the first save, standard types and known custom types from the open tree
populate the list. After saving, only the saved selection is used; new types must
be added explicitly. Changes take effect only after **Save**. Settings are shared
between CustomDetails instances through a dedicated Gramps configuration manager.
Existing configuration keys remain compatible.

## Updates and limits

The display updates on selection, home-person, person and family changes. Changes
to events, places and media refresh the original detail fields. Person, family and
home-person changes invalidate the numbering caches. No genealogy records or
attributes are written.

Each numbering traversal is limited to 100 parent/child steps and 100,000 path
positions. Cycles, missing records and reached limits produce calculation notices;
incomplete searches do not produce definitive claims of no ancestry or descent.

## Languages

The plugin follows the language selected in Gramps. English source messages and
English and German gettext catalogs are included, following the CustomGOVImport
layout. Editable files are `po/en-local.po` and `po/de-local.po`, with a template in
`po/template.pot`. Runtime files are `locale/en/LC_MESSAGES/addon.mo` and
`locale/de/LC_MESSAGES/addon.mo`.

Names, custom attribute types and attribute values are user data and are not
translated automatically. Attribute selections use displayed type names; when
switching the Gramps language, review selected names of standard attribute types.
