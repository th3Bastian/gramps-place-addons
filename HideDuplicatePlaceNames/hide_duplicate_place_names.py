# -*- coding: utf-8 -*-
#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2026 Sebastian Klossek
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import logging
from functools import wraps

from gi.repository import Gtk

from gramps.gen.config import config
from gramps.gen.const import GRAMPS_LOCALE as glocale
import gramps.gen.display.place as place_module
from gramps.gui.configure import GrampsPreferences


try:
    _trans = glocale.get_addon_translator(__file__)
except ValueError:
    _trans = glocale.translation
_ = _trans.gettext

LOG = logging.getLogger(__name__)


# ============================================================
# Konfiguration
# ============================================================

CONFIG_KEY = "preferences.place-duplicate-suppression-types"

DEFAULT_DUPLICATE_SUPPRESSION_TYPES = [
    _("Church"),
    _("Cemetery"),
]

config.register(
    CONFIG_KEY,
    DEFAULT_DUPLICATE_SUPPRESSION_TYPES,
)


# ============================================================
# Dublettenfilter
# ============================================================

_original_display_event = None
_original_get_location_list = None

_filter_duplicates = False

DISPLAY_PATCH_MARKER = "_hide_duplicate_place_names_display_patch"
PREFERENCES_PATCH_MARKER = "_hide_duplicate_place_names_preferences_patch"
PANEL_MARKER = "_hide_duplicate_place_names_panel_added"


def filtered_get_location_list(db, place, date=None, lang=None):
    """
    Liefert normalerweise die originale Ortsliste.

    Während der Event-/Lesedarstellung werden unmittelbar
    aufeinanderfolgende gleiche Ortsnamen unterdrückt,
    wenn der type.string des aktuellen Eintrags in der
    konfigurierten Liste steht.
    """

    all_places = _original_get_location_list(
        db,
        place,
        date,
        lang,
    )

    if not _filter_duplicates:
        return all_places

    configured_types = config.get(CONFIG_KEY)
    if not isinstance(configured_types, (list, tuple, set)):
        LOG.warning(
            "Invalid value for %s; using default place types.",
            CONFIG_KEY,
        )
        configured_types = DEFAULT_DUPLICATE_SUPPRESSION_TYPES

    duplicate_suppression_types = {
        place_type
        for place_type in configured_types
        if isinstance(place_type, str)
    }

    filtered = []

    for item in all_places:
        try:
            name, place_type = item
        except (TypeError, ValueError):
            LOG.warning("Skipping malformed place-list item: %r", item)
            filtered.append(item)
            continue

        current_type = getattr(place_type, "string", None)

        if filtered:
            previous_item = filtered[-1]
            try:
                previous_name, _previous_type = previous_item
            except (TypeError, ValueError):
                previous_name = None

            if (
                name == previous_name
                and current_type in duplicate_suppression_types
            ):
                continue

        filtered.append(item)

    return filtered


def filtered_display_event(self, db, event, fmt=-1):
    """
    Aktiviert den Dublettenfilter ausschließlich während
    der normalen Event-/Lesedarstellung.
    """

    global _filter_duplicates

    old_value = _filter_duplicates
    _filter_duplicates = True

    try:
        return _original_display_event(
            self,
            db,
            event,
            fmt,
        )
    finally:
        _filter_duplicates = old_value


# ============================================================
# Preferences
# ============================================================

def add_preferences_panel(self):
    """
    Fügt den Preferences-Tab 'Ortsanzeige' hinzu.
    """

    grid = Gtk.Grid()

    # Dieselben Maße wie GrampsPreferences.create_grid().
    grid.set_column_spacing(6)
    grid.set_column_homogeneous(False)
    grid.set_row_spacing(6)
    grid.set_border_width(12)
    grid.set_margin_end(24)

    # --------------------------------------------------------
    # Erklärung unter dem Eingabefeld
    # --------------------------------------------------------

    label = Gtk.Label(
        label=(
            _(
                "Place names in immediately consecutive identical entries "
                "are combined when their place type is included in this "
                "list. Capitalization must match the place type exactly."
            )
        )
    )

    label.set_xalign(0)
    label.set_halign(Gtk.Align.FILL)
    label.set_line_wrap(True)
    label.set_margin_top(10)

    grid.attach(
        label,
        0,
        1,
        2,
        1,
    )

    # --------------------------------------------------------
    # Ortsarten + Eingabefeld
    # --------------------------------------------------------

    list_label = Gtk.Label(
        label=_("Place types:")
    )

    list_label.set_xalign(0)
    list_label.set_valign(Gtk.Align.START)
    list_label.set_margin_top(10)

    grid.attach(
        list_label,
        0,
        0,
        1,
        1,
    )

    # --------------------------------------------------------
    # Mehrzeiliges Eingabefeld
    # --------------------------------------------------------

    text_view = Gtk.TextView()
    
    text_view.set_wrap_mode(
        Gtk.WrapMode.NONE
    )

    text_view.set_hexpand(True)
    text_view.set_vexpand(False)
    text_view.set_left_margin(8)
    text_view.set_right_margin(8)
    text_view.set_top_margin(6)
    text_view.set_bottom_margin(6)

    buffer = text_view.get_buffer()

    values = config.get(CONFIG_KEY) or []

    buffer.set_text(
        "\n".join(values)
    )

    # --------------------------------------------------------
    # Ein Gtk.Entry erhält seine abgerundeten Ecken direkt vom GTK-Theme.
    # Ein mehrzeiliges Gtk.TextView nicht; deshalb erhält dessen Container
    # dieselbe grundlegende Feldoptik über eine lokale CSS-Klasse.
    # --------------------------------------------------------

    field = Gtk.ScrolledWindow()

    field.set_policy(
        Gtk.PolicyType.NEVER,
        Gtk.PolicyType.AUTOMATIC,
    )
    field.set_hexpand(True)
    field.set_halign(Gtk.Align.FILL)
    field.set_margin_top(10)
    field.set_size_request(-1, 192)
    field.add(text_view)

    css = Gtk.CssProvider()
    css.load_from_data(
        b"""
        .place-duplicate-list {
            background-color: @theme_base_color;
            border: 1px solid alpha(@theme_fg_color, 0.45);
            border-radius: 7px;
        }
        .place-duplicate-list > viewport {
            background-color: transparent;
            border-radius: 6px;
        }
        textview.place-duplicate-list-text,
        textview.place-duplicate-list-text text {
            background-color: transparent;
        }
        """
    )
    field.get_style_context().add_class("place-duplicate-list")
    field.get_style_context().add_provider(
        css,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )
    text_view.get_style_context().add_class("place-duplicate-list-text")
    text_view.get_style_context().add_provider(
        css,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    grid.attach(
        field,
        1,
        0,
        1,
        1,
    )

    # --------------------------------------------------------
    # Änderungen speichern
    # --------------------------------------------------------

    def get_values():
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(
            start_iter,
            end_iter,
            True,
        )
        values = []
        for line in text.splitlines():
            value = line.strip()
            if value and value not in values:
                values.append(value)

        return sorted(values, key=str.casefold), text

    def save_values(*_args):
        values, _text = get_values()

        config.set(
            CONFIG_KEY,
            values,
        )

    def normalize_values(_widget, _event):
        values, text = get_values()
        normalized_text = "\n".join(values)

        if text != normalized_text:
            buffer.set_text(normalized_text)

        return False

    buffer.connect(
        "changed",
        save_values,
    )
    text_view.connect(
        "focus-out-event",
        normalize_values,
    )

    # --------------------------------------------------------
    # Preferences-Seite hinzufügen
    # --------------------------------------------------------

    tab_label = Gtk.Label(
        label=_("Place display")
    )

    self.panel.append_page(
        grid,
        tab_label,
    )

    # Wichtig:
    # Neu hinzugefügte Preferences-Seite sichtbar machen.
    grid.show_all()


# ============================================================
# Preferences-Patch
# ============================================================

def install_display_patch():
    """Installiert die Ortslisten- und Event-Anzeige-Patches einmalig."""

    global _original_display_event, _original_get_location_list

    display_event = getattr(place_module.PlaceDisplay, "display_event", None)
    get_location_list = getattr(place_module, "get_location_list", None)
    if not callable(display_event) or not callable(get_location_list):
        LOG.error(
            "HideDuplicatePlaceNames is incompatible with this Gramps "
            "version: required place-display functions are unavailable."
        )
        return

    if getattr(
        display_event,
        DISPLAY_PATCH_MARKER,
        False,
    ):
        return

    _original_display_event = display_event
    _original_get_location_list = get_location_list

    setattr(filtered_display_event, DISPLAY_PATCH_MARKER, True)
    place_module.get_location_list = filtered_get_location_list
    place_module.PlaceDisplay.display_event = filtered_display_event


def install_preferences_patch():
    """Hängt den Einstellungs-Tab an die aktuelle Preferences-Implementierung."""

    current_init = getattr(GrampsPreferences, "__init__", None)
    if not callable(current_init):
        LOG.error(
            "HideDuplicatePlaceNames is incompatible with this Gramps "
            "version: the Preferences dialog is unavailable."
        )
        return

    if getattr(current_init, PREFERENCES_PATCH_MARKER, False):
        return

    @wraps(current_init)
    def place_duplicate_prefs_init(
        self,
        uistate,
        dbstate,
    ):

        current_init(
            self,
            uistate,
            dbstate,
        )

        if not getattr(self, PANEL_MARKER, False):
            add_preferences_panel(self)
            setattr(self, PANEL_MARKER, True)

    setattr(place_duplicate_prefs_init, PREFERENCES_PATCH_MARKER, True)
    GrampsPreferences.__init__ = place_duplicate_prefs_init



def install():
    """Installiert sämtliche GUI-Patches nach dem Laden anderer Add-ons."""

    install_display_patch()
    install_preferences_patch()


# ============================================================
# Installation
# ============================================================
