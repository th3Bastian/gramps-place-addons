"""Lädt HideDuplicatePlaceNames nur innerhalb der grafischen Gramps-Oberfläche."""

import os
import sys

from gi.repository import GLib


def _install_when_idle():
    """Installiert die Erweiterung nach den übrigen Start-Add-ons."""

    plugin_directory = os.path.abspath(os.path.dirname(__file__))
    if plugin_directory not in sys.path:
        sys.path.append(plugin_directory)

    from hide_duplicate_place_names import install

    install()
    return False


def load_on_reg(dbstate, uistate, plugin):
    """Wird vom Gramps-Plugin-Loader aufgerufen."""

    if uistate:
        GLib.idle_add(_install_when_idle)
