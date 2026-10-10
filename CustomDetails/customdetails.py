# Derived from Gramps 6.0.8 persondetails.py; original credits and GPL retained.
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2011 Nick Hall
# Copyright (C) 2013 Heinz Brinker <heinzbrinker@yahoo.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <https://www.gnu.org/licenses/>.
#

# -------------------------------------------------------------------------
#
# Gtk modules
#
# -------------------------------------------------------------------------
import locale

from gi.repository import Gtk, GLib
from gi.repository.GLib import markup_escape_text

# -------------------------------------------------------------------------
#
# Gramps modules
#
# -------------------------------------------------------------------------
from gramps.gen.lib import EventType, EventRoleType, AttributeType
from gramps.gen.plug import Gramplet
from gramps.gen.plug.menu import BooleanOption, TextOption
from gramps.gen.relationship import get_relationship_calculator
from gramps.gen.config import config
from kekule_index import build_index
from daboville_index import build_descendant_index
from gramps.gui.widgets import Photo
from gramps.gen.display.name import displayer as name_displayer
from gramps.gen.display.place import displayer as place_displayer
from gramps.gen.datehandler import get_date
from gramps.gen.utils.file import media_path_full
from gramps.gen.const import COLON, GRAMPS_LOCALE as glocale

try:
    _trans = glocale.get_addon_translator(__file__)
except ValueError:
    _trans = glocale.translation
_ = _trans.gettext

CUSTOM_CONFIG = config.register_manager("customdetails")
CUSTOM_CONFIG.register("display.home", True)
CUSTOM_CONFIG.register("display.relationship", True)
CUSTOM_CONFIG.register("display.kekule", True)
CUSTOM_CONFIG.register("display.daboville", True)
CUSTOM_CONFIG.register("attributes.types", [])
CUSTOM_CONFIG.register("attributes.configured", False)
CUSTOM_CONFIG.load()

DISPLAY_OPTIONS = (
    ("display.home", _("Show reference person")),
    ("display.relationship", _("Show kinship")),
    ("display.kekule", _("Show Kekulé number")),
    ("display.daboville", _("Show d’Aboville number")),
)
ATTRIBUTE_LABEL = _("Show the following attributes")


class CustomDetails(Gramplet):
    """
    Displays details for a person.
    """

    def init(self):
        self._config_callbacks = []
        self._saving_config = False
        self.load_settings()
        self._kekule_cache = None
        self._daboville_cache = None
        self._relationship_cache = None
        self.gui.WIDGET = self.build_gui()
        self.gui.get_container_widget().remove(self.gui.textview)
        self.gui.get_container_widget().add(self.gui.WIDGET)
        self.uistate.connect("nameformat-changed", self.update)
        self.uistate.connect("placeformat-changed", self.update)

    @staticmethod
    def clean_attribute_types(values):
        if isinstance(values, str):
            values = values.splitlines()
        cleaned = []
        seen = set()
        for value in values or []:
            for line in str(value).splitlines():
                name = line.strip()
                if name and name.casefold() not in seen:
                    cleaned.append(name)
                    seen.add(name.casefold())
        return sorted(cleaned, key=lambda name: locale.strxfrm(name.casefold()))

    def load_settings(self):
        self.display_settings = {key: CUSTOM_CONFIG.get(key)
                                 for key, _label in DISPLAY_OPTIONS}
        self.attribute_types = self.clean_attribute_types(
            CUSTOM_CONFIG.get("attributes.types"))
        if not CUSTOM_CONFIG.get("attributes.configured"):
            # Initially preserve the previous display of all known attributes.
            names = AttributeType().get_standard_names() + [_("Title"), _("Religion")]
            if self.dbstate.is_open():
                names += self.dbstate.db.get_person_attribute_types()
            self.attribute_types = self.clean_attribute_types(names)

    def on_load(self):
        self.load_settings()
        self.gui.data = []
        for key in [key for key, _label in DISPLAY_OPTIONS] + [
                "attributes.types", "attributes.configured"]:
            self._config_callbacks.append(
                CUSTOM_CONFIG.connect(key, self.shared_settings_changed))

    def on_save(self):
        self.gui.data = []
        for callback in self._config_callbacks:
            CUSTOM_CONFIG.disconnect(callback)
        self._config_callbacks = []

    def shared_settings_changed(self, *_):
        if not self._saving_config:
            self.load_settings()
            self.update()

    def build_options(self):
        self.load_settings()
        for key, label in DISPLAY_OPTIONS:
            self.add_option(BooleanOption(label, self.display_settings[key]))
        self.add_option(TextOption(ATTRIBUTE_LABEL, list(self.attribute_types)))
        widget = self.get_option_widget(ATTRIBUTE_LABEL)
        widget.set_hexpand(True)
        widget.set_vexpand(False)
        widget.set_halign(Gtk.Align.FILL)
        widget.set_min_content_height(140)
        widget.connect("parent-set", self.attribute_option_parent_set)

    def attribute_option_parent_set(self, widget, old_parent):
        if (widget.get_parent() is None or
                getattr(widget, "_layout_pending", False) or
                getattr(widget, "_layout_done", False)):
            return
        widget._layout_pending = True
        GLib.idle_add(self.layout_attribute_option, widget)

    @staticmethod
    def layout_attribute_option(widget):
        widget._layout_pending = False
        grid = widget.get_parent()
        if not isinstance(grid, Gtk.Grid) or getattr(widget, "_layout_done", False):
            return GLib.SOURCE_REMOVE
        # Find this editor's label, not a preceding checkbox label.
        row = grid.child_get_property(widget, "top-attach")
        label = next((child for child in grid.get_children()
                      if isinstance(child, Gtk.Label) and
                      grid.child_get_property(child, "top-attach") == row), None)
        if label is None:
            return GLib.SOURCE_REMOVE
        # Boolean widgets already contain their own descriptive text.
        # Remove Gramps' extra labels and let each checkbox span the full row.
        for checkbox in list(grid.get_children()):
            if not isinstance(checkbox, Gtk.CheckButton):
                continue
            checkbox_row = grid.child_get_property(checkbox, "top-attach")
            duplicate_label = next(
                (child for child in grid.get_children()
                 if isinstance(child, Gtk.Label) and
                 grid.child_get_property(child, "top-attach") == checkbox_row),
                None,
            )
            if duplicate_label is not None:
                grid.remove(duplicate_label)
            grid.remove(checkbox)
            checkbox.set_halign(Gtk.Align.START)
            grid.attach(checkbox, 0, checkbox_row, 2, 1)
        widget._layout_done = True
        grid.remove(label)
        grid.remove(widget)
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.END)
        grid.set_row_spacing(6)
        grid.attach(label, 0, row, 2, 1)
        grid.attach(widget, 0, row + 1, 2, 1)
        grid.show_all()
        return GLib.SOURCE_REMOVE

    def save_options(self):
        """Do not save unconfirmed edits when Gramps rebuilds the panel."""

    def save_update_options(self, widget=None):
        values = {key: bool(self.get_option(label).get_value())
                  for key, label in DISPLAY_OPTIONS}
        attributes = self.clean_attribute_types(
            self.get_option(ATTRIBUTE_LABEL).get_value())
        self._saving_config = True
        try:
            for key, value in values.items():
                CUSTOM_CONFIG.set(key, value)
            CUSTOM_CONFIG.set("attributes.types", attributes)
            CUSTOM_CONFIG.set("attributes.configured", True)
            CUSTOM_CONFIG.save()
        finally:
            self._saving_config = False
        self.load_settings()
        self.get_option(ATTRIBUTE_LABEL).set_value(list(self.attribute_types))
        self.gui.data = []
        self.update()

    def build_gui(self):
        """
        Build the GUI interface.
        """
        self.top = Gtk.Box()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.photo = Photo(self.uistate.screen_height() < 1000)
        self.photo.set_valign(Gtk.Align.START)
        self.photo.set_margin_top(5)
        self.photo.set_margin_bottom(5)
        self.photo.show()
        self.name = Gtk.Label(halign=Gtk.Align.START)
        self.name.set_selectable(True)
        vbox.pack_start(self.name, fill=True, expand=False, padding=7)
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.grid.set_column_spacing(10)
        vbox.pack_start(self.grid, fill=True, expand=False, padding=5)
        vbox.show_all()
        self.top.pack_start(self.photo, fill=True, expand=False, padding=5)
        self.top.pack_start(vbox, fill=True, expand=True, padding=10)
        return self.top

    def add_row(self, title, value):
        """
        Add a row to the table.
        """
        label = Gtk.Label(
            label=title + COLON, halign=Gtk.Align.END, valign=Gtk.Align.START
        )
        label.set_selectable(True)
        label.show()
        value = Gtk.Label(label=value, halign=Gtk.Align.START)
        value.set_selectable(True)
        value.show()
        self.grid.add(label)
        self.grid.attach_next_to(value, label, Gtk.PositionType.RIGHT, 1, 1)

    def clear_grid(self):
        """
        Remove all the rows from the grid.
        """
        list(map(self.grid.remove, self.grid.get_children()))

    def db_changed(self):
        self.load_settings()
        self._kekule_cache = None
        self._daboville_cache = None
        self._relationship_cache = None
        for kind in ("person", "family"):
            for operation in ("add", "update", "delete", "rebuild"):
                self.connect(self.dbstate.db, kind + "-" + operation,
                             self.invalidate_kekule)
        self.connect(self.dbstate.db, "home-person-changed", self.invalidate_kekule)
        for kind in ("event", "place", "media"):
            for operation in ("add", "update", "delete", "rebuild"):
                self.connect(self.dbstate.db, kind + "-" + operation, self.update)

    def invalidate_kekule(self, *_):
        self.load_settings()
        self._kekule_cache = None
        self._daboville_cache = None
        self._relationship_cache = None
        self.update()

    def active_changed(self, handle):
        self.update()

    def update_has_data(self):
        handle = self.get_active("Person")
        self.set_has_data(bool(handle and
                               self.dbstate.db.get_person_from_handle(handle)))

    def relationship_to_home(self, home, active_person):
        """Describe the selected person relative to the home person."""
        if home.get_handle() == active_person.get_handle():
            return _("Reference person themself")
        depth = config.get("behavior.generation-depth")
        key = (home.get_handle(), active_person.get_handle(), depth)
        if self._relationship_cache is None or self._relationship_cache[0] != key:
            # A fresh calculator avoids retaining stale database ancestry maps.
            calculator = get_relationship_calculator()
            calculator.set_depth(depth)
            relation = calculator.get_one_relationship(self.dbstate.db, home, active_person)
            self._relationship_cache = (key, relation or
                _("No relationship found within the configured search depth"))
        return self._relationship_cache[1]

    def display_kekule(self, active_person):
        show_home = self.display_settings["display.home"]
        show_relationship = self.display_settings["display.relationship"]
        show_kekule = self.display_settings["display.kekule"]
        show_daboville = self.display_settings["display.daboville"]
        if not (show_home or show_relationship or show_kekule or show_daboville):
            return
        db = self.dbstate.db
        home = db.get_default_person()
        if home is None:
            if show_home:
                self.add_row(_("Reference person"), _("No home person has been set"))
            if show_relationship:
                self.add_row(_("Kinship"), "—")
            if show_kekule:
                self.add_row(_("Kekulé number"), "—")
            if show_daboville:
                self.add_row(_("d’Aboville number"), "—")
            return
        home_handle = home.get_handle()
        if show_home:
            self.add_row(_("Reference person"), "%s [%s]" %
                         (name_displayer.display(home), home.get_gramps_id()))
        if show_relationship:
            self.add_row(_("Kinship"), self.relationship_to_home(home, active_person))
        notices = []
        if show_kekule:
            if self._kekule_cache is None or self._kekule_cache[0] != home_handle:
                index, warnings = build_index(db, home_handle, translate=_)
                self._kekule_cache = (home_handle, index, warnings)
            cached_home, index, warnings = self._kekule_cache
            numbers = index.get(active_person.get_handle(), ())
            if numbers:
                value = ", ".join(str(number) for number in numbers)
            elif warnings:
                value = _("No number found in the examined part of the family tree")
            else:
                value = _("Not a direct ancestor of the reference person")
            self.add_row(_("Kekulé number"), value)
            if warnings:
                notices.append(_("Kekulé: %s") % "; ".join(warnings))
        if show_daboville:
            if self._daboville_cache is None or self._daboville_cache[0] != home_handle:
                index, warnings = build_descendant_index(db, home_handle, translate=_)
                self._daboville_cache = (home_handle, index, warnings)
            cached_home, index, warnings = self._daboville_cache
            numbers = index.get(active_person.get_handle(), ())
            if numbers:
                value = ", ".join(numbers)
            elif warnings:
                value = _("No number found in the examined part of the family tree")
            else:
                value = _("Not a direct descendant of the reference person")
            self.add_row(_("d’Aboville number"), value)
            if warnings:
                notices.append(_("d’Aboville: %s") % "; ".join(warnings))
        if notices:
            self.add_row(_("Calculation notice"), " | ".join(notices))

    def main(self):  # return false finishes
        self.display_empty()
        active_handle = self.get_active("Person")
        if active_handle:
            active_person = self.dbstate.db.get_person_from_handle(active_handle)
            self.top.hide()
            if active_person:
                self.display_person(active_person)
            self.top.show()
        self.update_has_data()

    def display_person(self, active_person):
        """
        Display details of the active person.
        """
        self.load_person_image(active_person)
        self.name.set_markup(
            "<span size='large' weight='bold'>%s</span>"
            % markup_escape_text(name_displayer.display(active_person), -1)
        )
        self.clear_grid()
        self.display_alternate_names(active_person)
        self.display_parents(active_person)
        self.display_separator()
        self.display_type(active_person, EventType(EventType.BIRTH))
        self.display_type(active_person, EventType(EventType.BAPTISM))
        self.display_type(active_person, EventType(EventType.DEATH))
        self.display_type(active_person, EventType(EventType.BURIAL))
        self.display_attributes(active_person)
        if any(self.display_settings.values()):
            self.display_separator()
            self.display_kekule(active_person)

    def display_empty(self):
        """
        Display empty details when no person is selected.
        """
        self.photo.set_image(None)
        self.photo.set_uistate(None, None)
        self.name.set_text(_("No active person"))
        self.clear_grid()

    def display_separator(self):
        """
        Display an empty row to separate groupd of entries.
        """
        label = Gtk.Label()
        label.set_markup("<span font='sans 4'> </span>")
        label.set_selectable(True)
        label.show()
        self.grid.add(label)

    def display_alternate_names(self, active_person):
        """
        Display other names of the person
        """
        try:
            nlist = active_person.get_alternate_names()
            if len(nlist) > 0:
                for altname in nlist:
                    name_type = str(altname.get_type())
                    text = name_displayer.display_name(altname)
                    self.add_row(name_type, text)
                self.display_separator()
        except:
            pass

    def display_parents(self, active_person):
        """
        Display the parents of the active person.
        """
        family_handle = active_person.get_main_parents_family_handle()
        family = self.dbstate.db.get_family_from_handle(family_handle) if family_handle else None
        if family:
            handle = family.get_father_handle()
            if handle:
                father = self.dbstate.db.get_person_from_handle(handle)
                father_name = name_displayer.display(father) if father else _("Unknown")
            else:
                father_name = _("Unknown")
            handle = family.get_mother_handle()
            if handle:
                mother = self.dbstate.db.get_person_from_handle(handle)
                mother_name = name_displayer.display(mother) if mother else _("Unknown")
            else:
                mother_name = _("Unknown")
        else:
            father_name = _("Unknown")
            mother_name = _("Unknown")

        self.add_row(_("Father"), father_name)
        self.add_row(_("Mother"), mother_name)

    def display_attributes(self, active_person):
        """Show only the configured types, preserving stored attribute order."""
        allowed = {name.casefold() for name in self.attribute_types}
        attributes = [attribute for attribute in active_person.get_attribute_list()
                      if str(attribute.get_type()).strip().casefold() in allowed]
        if attributes:
            self.display_separator()
        for attribute in attributes:
            self.add_row(str(attribute.get_type()), attribute.get_value())

    def display_type(self, active_person, event_type):
        """
        Display an event type row.
        """
        event = self.get_event(active_person, event_type)
        if event:
            self.add_row(str(event_type), self.format_event(event))

    def get_event(self, person, event_type):
        """
        Return an event of the given type.
        """
        for event_ref in person.get_event_ref_list():
            if int(event_ref.get_role()) == EventRoleType.PRIMARY:
                event = self.dbstate.db.get_event_from_handle(event_ref.ref)
                if event and event.get_type() == event_type:
                    return event
        return None

    def format_event(self, event):
        """
        Format the event for display.
        """
        date = get_date(event)
        handle = event.get_place_handle()
        if handle:
            place = place_displayer.display_event(self.dbstate.db, event)
            retval = _("%(date)s - %(place)s.") % {"date": date, "place": place}
        else:
            retval = _("%(date)s.") % dict(date=date)
        return retval

    def load_person_image(self, person):
        """
        Load the primary image if it exists.
        """
        media_list = person.get_media_list()
        if media_list:
            media_ref = media_list[0]
            object_handle = media_ref.get_reference_handle()
            obj = self.dbstate.db.get_media_from_handle(object_handle)
            if obj is None:
                self.photo.set_image(None)
                self.photo.set_uistate(None, None)
                return
            full_path = media_path_full(self.dbstate.db, obj.get_path())
            mime_type = obj.get_mime_type()
            if mime_type and mime_type.startswith("image"):
                self.photo.set_image(full_path, mime_type, media_ref.get_rectangle())
                self.photo.set_uistate(self.uistate, object_handle)
            else:
                self.photo.set_image(None)
                self.photo.set_uistate(None, None)
        else:
            self.photo.set_image(None)
            self.photo.set_uistate(None, None)
