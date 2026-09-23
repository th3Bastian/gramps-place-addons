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

"""
CustomGOVImport Gramplet.
"""

# ------------------------------------------------------------------------
#
# Python modules
#
# ------------------------------------------------------------------------

import urllib.parse
import urllib.request
import urllib.error
import ssl
import locale

from xml.dom.minidom import parseString

# ------------------------------------------------------------------------
#
# GTK modules
#
# ------------------------------------------------------------------------
from gi.repository import GLib, Gtk, Pango

# ------------------------------------------------------------------------
#
# Gramps modules
#
# ------------------------------------------------------------------------
from gramps.gen.plug import Gramplet
from gramps.gen.plug.menu import TextOption
from gramps.gen.db import DbTxn
from gramps.gen.lib import Place, PlaceName, PlaceType, PlaceRef, Url, UrlType
from gramps.gen.datehandler import parser
from gramps.gen.config import config
from gramps.gen.display.place import displayer as _pd
from gramps.gui.dialog import WarningDialog

# ------------------------------------------------------------------------
#
# Internationalisation
#
# ------------------------------------------------------------------------
from gramps.gen.const import GRAMPS_LOCALE as glocale

try:
    _trans = glocale.get_addon_translator(__file__)
except ValueError:
    _trans = glocale.translation
_ = _trans.gettext

# Shared by every CustomGOVImport gramplet instance in every view.
CUSTOM_CONFIG = config.register_manager("customgovimport")
CUSTOM_CONFIG.register("blacklist.types", [])
CUSTOM_CONFIG.register("blacklist.shared", False)
CUSTOM_CONFIG.load()

# ------------------------------------------------------------------------
#
# Constants
#
# ------------------------------------------------------------------------

GOV_NAMESPACE = "http://gov.genealogy.net/ontology.owl#"
RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

ISO_CODE_LOOKUP = {
    "aar": "aa",
    "abk": "ab",
    "afr": "af",
    "aka": "ak",
    "alb": "sq",
    "amh": "am",
    "ara": "ar",
    "arg": "an",
    "arm": "hy",
    "asm": "as",
    "ava": "av",
    "ave": "ae",
    "aym": "ay",
    "aze": "az",
    "bak": "ba",
    "bam": "bm",
    "baq": "eu",
    "bel": "be",
    "ben": "bn",
    "bih": "bh",
    "bis": "bi",
    "bod": "bo",
    "bos": "bs",
    "bre": "br",
    "bul": "bg",
    "bur": "my",
    "cat": "ca",
    "ces": "cs",
    "cha": "ch",
    "che": "ce",
    "chi": "zh",
    "chu": "cu",
    "chv": "cv",
    "cor": "kw",
    "cos": "co",
    "cre": "cr",
    "cym": "cy",
    "cze": "cs",
    "dan": "da",
    "deu": "de",
    "div": "dv",
    "dut": "nl",
    "dzo": "dz",
    "ell": "el",
    "eng": "en",
    "epo": "eo",
    "est": "et",
    "eus": "eu",
    "ewe": "ee",
    "fao": "fo",
    "fas": "fa",
    "fij": "fj",
    "fin": "fi",
    "fra": "fr",
    "fre": "fr",
    "fry": "fy",
    "ful": "ff",
    "geo": "ka",
    "ger": "de",
    "gla": "gd",
    "gle": "ga",
    "glg": "gl",
    "glv": "gv",
    "gre": "el",
    "grn": "gn",
    "guj": "gu",
    "hat": "ht",
    "hau": "ha",
    "heb": "he",
    "her": "hz",
    "hin": "hi",
    "hmo": "ho",
    "hrv": "hr",
    "hun": "hu",
    "hye": "hy",
    "ibo": "ig",
    "ice": "is",
    "ido": "io",
    "iii": "ii",
    "iku": "iu",
    "ile": "ie",
    "ina": "ia",
    "ind": "id",
    "ipk": "ik",
    "isl": "is",
    "ita": "it",
    "jav": "jv",
    "jpn": "ja",
    "kal": "kl",
    "kan": "kn",
    "kas": "ks",
    "kat": "ka",
    "kau": "kr",
    "kaz": "kk",
    "khm": "km",
    "kik": "ki",
    "kin": "rw",
    "kir": "ky",
    "kom": "kv",
    "kon": "kg",
    "kor": "ko",
    "kua": "kj",
    "kur": "ku",
    "lao": "lo",
    "lat": "la",
    "lav": "lv",
    "lim": "li",
    "lin": "ln",
    "lit": "lt",
    "ltz": "lb",
    "lub": "lu",
    "lug": "lg",
    "mac": "mk",
    "mah": "mh",
    "mal": "ml",
    "mao": "mi",
    "mar": "mr",
    "may": "ms",
    "mkd": "mk",
    "mlg": "mg",
    "mlt": "mt",
    "mon": "mn",
    "mri": "mi",
    "msa": "ms",
    "mya": "my",
    "nau": "na",
    "nav": "nv",
    "nbl": "nr",
    "nde": "nd",
    "ndo": "ng",
    "nep": "ne",
    "nld": "nl",
    "nno": "nn",
    "nob": "nb",
    "nor": "no",
    "nya": "ny",
    "oci": "oc",
    "oji": "oj",
    "ori": "or",
    "orm": "om",
    "oss": "os",
    "pan": "pa",
    "per": "fa",
    "pli": "pi",
    "pol": "pl",
    "por": "pt",
    "pus": "ps",
    "que": "qu",
    "roh": "rm",
    "ron": "ro",
    "rum": "ro",
    "run": "rn",
    "rus": "ru",
    "sag": "sg",
    "san": "sa",
    "sin": "si",
    "slk": "sk",
    "slo": "sk",
    "slv": "sl",
    "sme": "se",
    "smo": "sm",
    "sna": "sn",
    "snd": "sd",
    "som": "so",
    "sot": "st",
    "spa": "es",
    "sqi": "sq",
    "srd": "sc",
    "srp": "sr",
    "ssw": "ss",
    "sun": "su",
    "swa": "sw",
    "swe": "sv",
    "tah": "ty",
    "tam": "ta",
    "tat": "tt",
    "tel": "te",
    "tgk": "tg",
    "tgl": "tl",
    "tha": "th",
    "tib": "bo",
    "tir": "ti",
    "ton": "to",
    "tsn": "tn",
    "tso": "ts",
    "tuk": "tk",
    "tur": "tr",
    "twi": "tw",
    "uig": "ug",
    "ukr": "uk",
    "urd": "ur",
    "uzb": "uz",
    "ven": "ve",
    "vie": "vi",
    "vol": "vo",
    "wel": "cy",
    "wln": "wa",
    "wol": "wo",
    "xho": "xh",
    "yid": "yi",
    "yor": "yo",
    "zha": "za",
    "zho": "zh",
    "zul": "zu",
}


# ------------------------------------------------------------------------
#
# CustomGOVImport class
#
# ------------------------------------------------------------------------
class CustomGOVImport(Gramplet):
    """
    Gramplet to get places from the GOV database.
    """

    def init(self):
        """
        Initialise the gramplet.
        """
        self.blacklist = []
        self._blacklist_callback_id = None
        root = self.__create_gui()
        self.gui.get_container_widget().remove(self.gui.textview)
        self.gui.get_container_widget().add_with_viewport(root)
        root.show_all()
        self.type_dic = dict()
        self._scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self._scontext.verify_mode = ssl.VerifyMode.CERT_NONE

    def build_options(self):
        """Expose the blacklist in Gramps' view configuration."""
        label = _("Place types that should not be imported")
        self.add_option(TextOption(label, list(self.blacklist)))

        # GuiTextOption already provides Gramps' standard multi-line editor.
        # Give it a full-width row below its label and twice the default height.
        widget = self.get_option_widget(label)
        widget.set_hexpand(True)
        widget.set_vexpand(False)
        widget.set_halign(Gtk.Align.FILL)
        widget.set_min_content_height(140)
        widget.connect("parent-set", self.__blacklist_option_parent_set)

    def __blacklist_option_parent_set(self, widget, old_parent):
        """Arrange the option label above its editor after Gramps attaches it."""
        if (
            widget.get_parent() is None
            or getattr(widget, "_layout_pending", False)
            or getattr(widget, "_layout_done", False)
        ):
            return
        widget._layout_pending = True
        GLib.idle_add(self.__layout_blacklist_option, widget)

    @staticmethod
    def __layout_blacklist_option(widget):
        """Use the complete configuration-page width for the blacklist."""
        widget._layout_pending = False
        grid = widget.get_parent()
        if not isinstance(grid, Gtk.Grid) or getattr(widget, "_layout_done", False):
            return GLib.SOURCE_REMOVE

        option_label = next(
            (child for child in grid.get_children() if isinstance(child, Gtk.Label)),
            None,
        )
        if option_label is None:
            return GLib.SOURCE_REMOVE

        widget._layout_done = True
        grid.remove(option_label)
        grid.remove(widget)
        option_label.set_halign(Gtk.Align.START)
        option_label.set_valign(Gtk.Align.END)
        grid.set_row_spacing(6)
        grid.attach(option_label, 0, 0, 2, 1)
        grid.attach(widget, 0, 1, 2, 1)
        grid.show_all()
        return GLib.SOURCE_REMOVE

    def save_options(self):
        """Leave unconfirmed editor contents untouched during GUI rebuilds."""

    def save_update_options(self, widget=None):
        """Store the blacklist only when the Gramplet Save button is used."""
        self.blacklist = self.__clean_blacklist(
            self.get_option(_("Place types that should not be imported")).get_value()
        )
        CUSTOM_CONFIG.set("blacklist.types", list(self.blacklist))
        CUSTOM_CONFIG.set("blacklist.shared", True)
        CUSTOM_CONFIG.save()
        self.gui.data = []
        self.update()

    def on_load(self):
        shared = self.__clean_blacklist(CUSTOM_CONFIG.get("blacklist.types"))
        if not CUSTOM_CONFIG.get("blacklist.shared"):
            # Migrate and combine the former per-view values during rollout.
            shared = self.__clean_blacklist(shared + list(self.gui.data or []))
            CUSTOM_CONFIG.set("blacklist.types", list(shared))
            CUSTOM_CONFIG.save()
        self.blacklist = shared
        self.gui.data = []
        self._blacklist_callback_id = CUSTOM_CONFIG.connect(
            "blacklist.types", self.__shared_blacklist_changed
        )

    def on_save(self):
        self.gui.data = []
        if self._blacklist_callback_id is not None:
            CUSTOM_CONFIG.disconnect(self._blacklist_callback_id)
            self._blacklist_callback_id = None

    def __shared_blacklist_changed(self, *args):
        """Keep already open gramplet instances in sync."""
        self.blacklist = self.__clean_blacklist(
            CUSTOM_CONFIG.get("blacklist.types")
        )
        option = self.option_dict.get(_("Place types that should not be imported"))
        if option is not None:
            option[1].set_value(list(self.blacklist))

    @staticmethod
    def __clean_blacklist(values):
        """Clean type names and sort alphabetically for the current locale."""
        if isinstance(values, str):
            values = values.splitlines()
        cleaned = []
        seen = set()
        for value in values or []:
            for line in str(value).splitlines():
                place_type = line.strip()
                if place_type and place_type not in seen:
                    cleaned.append(place_type)
                    seen.add(place_type)
        return sorted(cleaned, key=lambda name: locale.strxfrm(name.casefold()))

    def __create_gui(self):
        """
        Create and display the GUI components of the gramplet.
        """
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # Match the spacing used by Gramps' Filter gramplet.
        vbox.set_border_width(6)
        vbox.set_spacing(6)

        label = Gtk.Label(_("Place ID to import from GOV (Historical Gazetteer):"))
        label.set_halign(Gtk.Align.FILL)
        label.set_xalign(0.0)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)

        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.entry.set_halign(Gtk.Align.FILL)

        self.skip_parent_places = Gtk.CheckButton(
            label=_("Do not import parent places")
        )
        self.skip_parent_places.set_hexpand(True)
        self.skip_parent_places.set_halign(Gtk.Align.FILL)
        checkbox_label = self.skip_parent_places.get_child()
        if isinstance(checkbox_label, Gtk.Label):
            checkbox_label.set_xalign(0.0)
            checkbox_label.set_line_wrap(True)
            checkbox_label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)

        button_box = Gtk.ButtonBox()
        button_box.set_layout(Gtk.ButtonBoxStyle.START)

        get = Gtk.Button(label=_("Get Place"))
        get.connect("clicked", self.__get_places)
        button_box.add(get)
        self.get_button = get
        self._import_running = False

        self.log_view = Gtk.TextView()
        self.log_view.set_editable(False)
        self.log_view.set_cursor_visible(False)
        self.log_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.log_buffer = self.log_view.get_buffer()
        self.log_end = self.log_buffer.create_mark(
            None, self.log_buffer.get_end_iter(), False
        )
        log_scroll = Gtk.ScrolledWindow()
        log_scroll.set_hexpand(True)
        log_scroll.set_halign(Gtk.Align.FILL)
        log_scroll.set_shadow_type(Gtk.ShadowType.NONE)
        log_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        log_scroll.set_min_content_height(120)
        log_style = log_scroll.get_style_context()
        # Use the active GTK theme's entry frame, colors and corner radius.
        log_style.add_class(Gtk.STYLE_CLASS_ENTRY)
        log_style.add_class(Gtk.STYLE_CLASS_FRAME)
        log_scroll.add(self.log_view)

        vbox.pack_start(label, False, True, 0)
        vbox.pack_start(self.entry, False, True, 0)
        vbox.pack_start(self.skip_parent_places, False, True, 0)
        vbox.pack_start(button_box, False, True, 0)
        vbox.pack_start(log_scroll, True, True, 0)

        return vbox

    def __log(self, message):
        """Append plain text and repaint without dispatching input callbacks."""
        self.log_buffer.insert(self.log_buffer.get_end_iter(), str(message) + "\n")
        self.log_view.scroll_mark_onscreen(self.log_end)
        self.log_view.queue_draw()
        window = self.log_view.get_window(Gtk.TextWindowType.WIDGET)
        if window is not None:
            window.process_updates(True)

    def __clear_log(self):
        """Clear the previous import log and reset its scroll position."""
        start, end = self.log_buffer.get_bounds()
        self.log_buffer.delete(start, end)
        start = self.log_buffer.get_start_iter()
        self.log_buffer.move_mark(self.log_end, start)
        self.log_view.scroll_mark_onscreen(self.log_end)
        self.log_view.queue_draw()
        window = self.log_view.get_window(Gtk.TextWindowType.WIDGET)
        if window is not None:
            window.process_updates(True)

    def main(self):
        """
        Called to update the display.
        """
        pass

    def __get_places(self, obj):
        if self._import_running:
            return
        self.__clear_log()
        gov_id = self.entry.get_text().strip()
        if not gov_id:
            self.__log(_("Please enter a GOV ID."))
            return
        self._import_running = True
        self.get_button.set_sensitive(False)
        self.entry.set_sensitive(False)
        self.skip_parent_places.set_sensitive(False)
        try:
            self.__log(_("Starting import: %s") % gov_id)
            self.__import_places(gov_id)
        except Exception as error:
            self.__log(_("Import failed: %s") % str(error))
            raise
        finally:
            self._import_running = False
            self.get_button.set_sensitive(True)
            self.entry.set_sensitive(True)
            self.skip_parent_places.set_sensitive(True)

    def __import_places(self, gov_id):
        to_do = [gov_id]
        import_parent_places = not self.skip_parent_places.get_active()
        fmt = config.get("preferences.place-format")
        pf = _pd.get_formats()[fmt]
        preferred_lang = (pf.language or "").strip().lower()
        if preferred_lang:
            self.__log(_("Language read from place format: %s") % preferred_lang)
        else:
            self.__log(_("No language found in the selected place format."))
        if len(preferred_lang) != 2:
            if preferred_lang:
                self.__log(_("Invalid place format language: %s") % preferred_lang)
            preferred_lang = "de"
            self.__log(_("Using fallback language: %s") % preferred_lang)
        visited = {}
        self.blacklist = self.__clean_blacklist(
            CUSTOM_CONFIG.get("blacklist.types")
        )
        blacklist = set(self.blacklist)

        if not self.type_dic:
            self.__log(_("Loading GOV place types..."))
            self.__get_types()
        if not self.type_dic:
            self.__log(_("Import stopped: no GOV place types available."))
            return
        with DbTxn(_("Add GOV-id place %s") % gov_id, self.dbstate.db) as trans:
            while to_do:
                gov_id = to_do.pop()
                place = self.dbstate.db.get_place_from_gramps_id(gov_id)
                if place is not None:
                    self.__log(_("Place already exists: %s") % gov_id)
                    _fetched_place, ref_list, _place_type_name = self.__get_place(
                        gov_id, self.type_dic, preferred_lang
                    )
                    self.__log(_("References found: %s") % len(ref_list))
                    if import_parent_places:
                        for ref, date in ref_list:
                            if ref and (ref not in to_do) and (ref not in visited):
                                to_do.append(ref)
                    visited[gov_id] = (place, ref_list)
                else:
                    self.__log(_("Loading place: %s") % gov_id)
                    place, ref_list, place_type_name = self.__get_place(
                        gov_id, self.type_dic, preferred_lang
                    )
                    self.__log(_("References found: %s") % len(ref_list))
                    if place.get_name().get_value() != "":
                        if import_parent_places:
                            for ref, date in ref_list:
                                if ref and (ref not in to_do) and (ref not in visited):
                                    to_do.append(ref)
                        if place_type_name in blacklist:
                            visited[gov_id] = (None, ref_list)
                            self.__log(
                                _("Place skipped by blacklist: %s (%s)")
                                % (gov_id, place_type_name)
                            )
                        else:
                            self.dbstate.db.add_place(place, trans)
                            self.__log(_("Place added: %s") % gov_id)
                            visited[gov_id] = (place, ref_list)
                    else:
                        raise ValueError(_("No usable place data: %s") % gov_id)

            self.__log(_("Saving place relationships..."))
            for place, ref_list in visited.values():
                if place is not None and len(ref_list) > 0:
                    place_changed = False
                    for ref, date in ref_list:
                        target = visited.get(ref)
                        if target is None and not import_parent_places:
                            existing_target = (
                                self.dbstate.db.get_place_from_gramps_id(ref)
                            )
                            if existing_target is None:
                                self.__log(
                                    _(
                                        "Reference to %s not created because the "
                                        "place does not exist."
                                    )
                                    % ref
                                )
                                continue
                            target = (existing_target, [])
                        if target is None or target[0] is None:
                            continue
                        handle = target[0].handle
                        place_ref = PlaceRef()
                        place_ref.ref = handle
                        place_ref.set_date_object(date)
                        if any(
                            existing_ref.is_equal(place_ref)
                            for existing_ref in place.get_placeref_list()
                        ):
                            continue
                        place.add_placeref(place_ref)
                        place_changed = True
                    if place_changed:
                        self.dbstate.db.commit_place(place, trans)
        self.__log(_("Import finished."))

    def __get_types(self):
        type_url = "https://gov.genealogy.net/types.owl"
        try:
            response = urllib.request.urlopen(url=type_url, context=self._scontext)
        except urllib.error.URLError as e:
            self.__log(_("GOV request failed: %s") % str(e.reason))
            WarningDialog(_("CustomGOVImport error: %s") % e.reason)
            return
        data = response.read()
        dom = parseString(data)
        for group in dom.getElementsByTagName("owl:Class"):
            url_value = group.attributes["rdf:about"].value
            group_number = url_value.split("#")[1]
            for element in dom.getElementsByTagNameNS(
                "http://gov.genealogy." "net/types.owl#", group_number
            ):
                type_number = element.attributes["rdf:about"].value.split("#")[1]
                for pname in element.getElementsByTagName("rdfs:label"):
                    type_lang = pname.attributes["xml:lang"].value
                    type_text = pname.childNodes[0].data
                    self.type_dic[type_number, type_lang] = type_text
            for element in dom.getElementsByTagNameNS(
                "http://gov.genealogy." "net/ontology.owl#", "Type"
            ):
                type_number = element.attributes["rdf:about"].value.split("#")[1]
                for pname in element.getElementsByTagName("rdfs:label"):
                    type_lang = pname.attributes["xml:lang"].value
                    type_text = pname.childNodes[0].data
                    self.type_dic[type_number, type_lang] = type_text

    def __get_place(self, gov_id, type_dic, preferred_lang):
        gov_url = "https://gov.genealogy.net/semanticWeb/about/" + urllib.parse.quote(
            gov_id
        )
        Internet_url = Url()
        place_url = "https://gov.genealogy.net/item/show/" + urllib.parse.quote(
	        gov_id
        )
        Internet_url.set_path(place_url)
        Internet_url.set_type(_("GOV link"))
        place = Place()
        place.gramps_id = gov_id
        place.add_url(Internet_url)
        try:
            response = urllib.request.urlopen(url=gov_url, context=self._scontext)
        except urllib.error.URLError as e:
            self.__log(_("GOV request failed: %s") % str(e.reason))
            eMsg = _("GOV error on id %s with code: " % gov_id)
            WarningDialog(eMsg + e.reason)
            return place, [], ""
        data = response.read()

        dom = parseString(data)
        top = dom.getElementsByTagName("gov:GovObject")

        if not len(top):
            self.__log(_("No GOV data found: %s") % gov_id)
            return place, [], ""

        count = 0
        place_type_name = ""
        for element in top[0].getElementsByTagName("gov:hasName"):
            count += 1
            place_name = self.__get_hasname(element)
            if count == 1:
                place.set_name(place_name)
            else:
                if place_name.lang == preferred_lang:
                    place.add_alternative_name(place.get_name())
                    place.set_name(place_name)
                else:
                    place.add_alternative_name(place_name)
        for element in top[0].getElementsByTagName("gov:hasType"):
            place_type, place_type_name = self.__get_hastype(
                element, type_dic, preferred_lang
            )
            place.set_type(place_type)
        for element in top[0].getElementsByTagName("gov:position"):
            latitude, longitude = self.__get_position(element)
            place.set_latitude(latitude)
            place.set_longitude(longitude)
        ref_list = self.__get_references(top[0])
        for element in top[0].getElementsByTagName("gov:hasURL"):
            url = self.__get_hasurl(element)
            place.add_url(url)

        return place, ref_list, place_type_name

    def __get_hasname(self, element):
        name = PlaceName()
        pname = element.getElementsByTagName("gov:PropertyName")
        if len(pname):
            value = pname[0].getElementsByTagName("gov:value")
            if len(value):
                name.set_value(value[0].childNodes[0].data)
            language = pname[0].getElementsByTagName("gov:language")
            if len(language):
                name.set_language(ISO_CODE_LOOKUP.get(language[0].childNodes[0].data))
            date = self.__get_date_range(pname[0])
            name.set_date_object(date)
        return name

    def __get_hastype(self, element, type_dic, preferred_lang):
        place_type = PlaceType()
        place_type_name = ""
        ptype = element.getElementsByTagName("gov:PropertyType")
        if len(ptype):
            value = ptype[0].getElementsByTagName("gov:type")
            if len(value):
                type_url = value[0].attributes["rdf:resource"].value
                type_code = type_url.split("#")[1]
                for language in (preferred_lang, "de", "en"):
                    if (type_code, language) in type_dic:
                        place_type_name = type_dic[type_code, language]
                        if language != preferred_lang:
                            self.__log(
                                _("Place type %s: no translation in %s; using fallback language: %s")
                                % (type_code, preferred_lang, language)
                            )
                        break
                if place_type_name:
                    place_type.set_from_xml_str(place_type_name)
        return place_type, place_type_name

    def __get_position(self, element):
        latitude = ""
        longitude = ""
        point = element.getElementsByTagName("wgs84:Point")
        if len(point):
            lat = element.getElementsByTagName("wgs84:lat")
            if len(lat):
                latitude = lat[0].childNodes[0].data
            lon = element.getElementsByTagName("wgs84:lon")
            if len(lon):
                longitude = lon[0].childNodes[0].data
        return (latitude, longitude)

    def __get_references(self, gov_object):
        """Return hierarchical and geographical GOV parent relations."""
        ref_list = []
        for element in gov_object.childNodes:
            if element.nodeType != element.ELEMENT_NODE:
                continue
            if element.namespaceURI != GOV_NAMESPACE or element.localName not in (
                "isPartOf",
                "isLocatedIn",
            ):
                continue
            if not element.getElementsByTagNameNS(GOV_NAMESPACE, "Relation"):
                continue
            ref, date = self.__get_relation(element)
            if ref:
                ref_list.append((ref, date))
        return ref_list

    def __get_relation(self, element):
        ref_url = None
        relation = element.getElementsByTagNameNS(GOV_NAMESPACE, "Relation")
        if len(relation):
            ref = relation[0].getElementsByTagNameNS(GOV_NAMESPACE, "ref")
            if len(ref):
                ref_url = ref[0].getAttributeNS(RDF_NAMESPACE, "resource")
        if ref_url:
            ref = ref_url.rstrip("/").rsplit("/", 1)[-1]
        else:
            ref = None
        date = self.__get_date_range(element)
        return (ref, date)

    def __get_hasurl(self, element):
        url = Url()
        pobj = element.getElementsByTagName("gov:PropertyForObject")
        if len(pobj):
            value = pobj[0].getElementsByTagName("gov:value")
            if len(value):
                url.set_path(value[0].childNodes[0].data)
                url.set_type(UrlType.WEB_HOME)
        return url

    def __get_date_range(self, element):
        begin_str = None
        begin = element.getElementsByTagNameNS(GOV_NAMESPACE, "timeBegin")
        if len(begin):
            begin_str = begin[0].childNodes[0].data
        end_str = None
        end = element.getElementsByTagNameNS(GOV_NAMESPACE, "timeEnd")
        if len(end):
            end_str = end[0].childNodes[0].data

        if begin_str and end_str:
            date_str = _trans.pgettext(
                "end", "from %(begin)s to %(end)s"
            ) % {"begin": begin_str, "end": end_str}
        elif begin_str:
            date_str = _("from %s") % begin_str
        elif end_str:
            date_str = _("to %s") % end_str
        else:
            date_str = ""

        return parser.parse(date_str)
