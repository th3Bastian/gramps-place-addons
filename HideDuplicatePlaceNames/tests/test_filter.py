"""Regression tests for duplicate-place filtering."""

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace


class Config:
    """Minimal config double used by the filter tests."""

    value = ["Church"]

    def register(self, *_args):
        pass

    def get(self, _key):
        return self.value

    def set(self, _key, value):
        self.value = value


def load_module():
    """Load the filter module without a running GTK/Gramps application."""

    config = Config()
    gi = ModuleType("gi")
    repository = ModuleType("gi.repository")
    repository.Gtk = SimpleNamespace()
    sys.modules["gi"] = gi
    sys.modules["gi.repository"] = repository

    for name in ("gramps", "gramps.gen", "gramps.gen.display", "gramps.gui"):
        sys.modules[name] = ModuleType(name)

    config_module = ModuleType("gramps.gen.config")
    config_module.config = config
    sys.modules["gramps.gen.config"] = config_module
    const_module = ModuleType("gramps.gen.const")
    const_module.GRAMPS_LOCALE = SimpleNamespace(
        translation=SimpleNamespace(gettext=lambda text: text),
        get_addon_translator=lambda _path: (_ for _ in ()).throw(ValueError()),
    )
    sys.modules["gramps.gen.const"] = const_module
    place_module = ModuleType("gramps.gen.display.place")
    place_module.PlaceDisplay = type(
        "PlaceDisplay", (), {"display_event": lambda *_args: ""}
    )
    place_module.get_location_list = lambda *_args: []
    sys.modules["gramps.gen.display.place"] = place_module
    configure_module = ModuleType("gramps.gui.configure")
    configure_module.GrampsPreferences = type("GrampsPreferences", (), {})
    sys.modules["gramps.gui.configure"] = configure_module

    source = Path(__file__).parents[1] / "hide_duplicate_place_names.py"
    spec = importlib.util.spec_from_file_location("hide_duplicate_test", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, config


class FilterTest(unittest.TestCase):
    """The filter must preserve malformed entries and suppress matches."""

    def test_duplicate_and_malformed_entries(self):
        module, config = load_module()
        church = SimpleNamespace(string="Church")
        city = SimpleNamespace(string="City")
        config.value = ["Church"]
        module._filter_duplicates = True
        module._original_get_location_list = lambda *_args: [
            ("Example", church),
            ("Example", church),
            "invalid",
            ("Example", city),
        ]

        self.assertEqual(
            module.filtered_get_location_list(None, None),
            [("Example", church), "invalid", ("Example", city)],
        )

    def test_invalid_configuration_uses_defaults(self):
        module, config = load_module()
        church = SimpleNamespace(string="Church")
        config.value = "invalid"
        module._filter_duplicates = True
        module._original_get_location_list = lambda *_args: [
            ("Example", church),
            ("Example", church),
        ]

        self.assertEqual(
            module.filtered_get_location_list(None, None),
            [("Example", church)],
        )
