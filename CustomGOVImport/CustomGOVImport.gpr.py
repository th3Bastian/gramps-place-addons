#
# Gramps - a GTK+/GNOME based genealogy program
#
# Custom GOVImport - a fork of GetGOV Gramplet.
# Based on the copied installed GetGOV 1.0.25 version for Gramps 6.0.
# Original copyright holders: Nick Hall (2015) and Gary Griffin (2024).
# Original project:
# https://github.com/gramps-project/addons-source/tree/maintenance/gramps60/GetGOV
#
# Copyright (C) 2015      Nick Hall
# Copyright (C) 2024      Gary Griffin
# Copyright (C) 2026      Sebastian Klossek
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#

# ------------------------------------------------------------------------
#
# CustomGOVImport Gramplet
#
# ------------------------------------------------------------------------

register(
    GRAMPLET,
    id="CustomGOVImport",
    name=_("CustomGOVImport"),
    description=_("Gramplet to get places from the GOV database"),
    status=STABLE,
    audience=EXPERT,
    version="1.0.0",
    gramps_target_version="6.0",
    fname="CustomGOVImport.py",
    gramplet="CustomGOVImport",
    height=375,
    detached_width=510,
    detached_height=480,
    expand=True,
    gramplet_title=_("CustomGOVImport"),
    # Use the original documentation until this fork has its own help page.
    help_url="GetGOV Gramplet",
    include_in_listing=True,
)
