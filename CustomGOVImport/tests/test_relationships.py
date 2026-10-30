"""Exercise the plugin's relationship reconciliation without GTK or a database.

Date is a small test double. The installed Gramps Date class and the live
Gramps import were additionally checked before releasing 1.2.2.
"""
import ast
import copy
from pathlib import Path
from types import SimpleNamespace as NS
import unittest


class Date:
    MOD_NONE, MOD_BEFORE, MOD_AFTER, MOD_FROM, MOD_TO, MOD_SPAN, MOD_TEXTONLY = range(7)

    def __init__(self, other=None, value=(0, 0, 1885, False), modifier=0):
        self.value = other.value if other else value
        self.modifier = other.modifier if other else modifier
        self.text = other.text if other else ''

    def get_text(self): return self.text
    def is_empty(self):
        return not any(self.value[:3]) and not any(self.value[4:7]) and not (self.modifier == self.MOD_TEXTONLY and self.text)
    def get_sort_value(self):
        day, month, year = self.value[:3]
        return year * 372 + month * 31 + day if year else 0
    def get_modifier(self): return self.modifier
    def set_modifier(self, modifier): self.modifier = modifier
    def get_start_date(self): return self.value[:4]
    def get_stop_date(self): return self.value[4:]
    def set(self, modifier, value, text):
        self.modifier, self.value, self.text = modifier, value, text
    def serialize(self, no_text_date=False):
        return self.modifier, self.value, '' if no_text_date else self.text


class Ref:
    def __init__(self, target='parent', date=None):
        self.ref, self.date = target, Date(date)
    def get_date_object(self): return self.date
    def set_date_object(self, date): self.date = Date(date)


class Place:
    def __init__(self, handle, refs=()):
        self.handle = self.gramps_id = handle
        self.refs = list(refs)
    def get_alternative_names(self): return self.names
    def set_alternative_names(self, names): self.names = names
    def get_placeref_list(self): return self.refs
    def set_placeref_list(self, refs): self.refs = refs
    def add_placeref(self, ref): self.refs.append(ref)


class Transaction:
    def __init__(self, *args): pass
    def __enter__(self): return self
    def __exit__(self, *args): pass


def load_plugin():
    source = Path(__file__).parents[1] / 'CustomGOVImport.py'
    tree = ast.parse(source.read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    cls.bases = []
    methods = {'__import_places', '__reference_identity', '__reference_date_sort_key', '__name_identity', '__update_place_values'}
    cls.body = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in methods]
    ns = dict(Date=Date, PlaceRef=Ref, DbTxn=Transaction, _=lambda x: x,
              config=NS(get=lambda _: 0),
              _pd=NS(get_formats=lambda: [NS(language='de')]),
              CUSTOM_CONFIG=NS(get=lambda _: []))
    exec(compile(ast.Module(body=[cls], type_ignores=[]), str(source), 'exec'), ns)
    return ns['CustomGOVImport']()


class RelationshipsTest(unittest.TestCase):
    def run_import(self, existing, incoming, update=False, names=None, sort=False):
        plugin = load_plugin()
        place = Place('child', copy.deepcopy(existing))
        place.names = copy.deepcopy(names or [])
        self.last_place = place
        targets = {key: Place(key) for key in ('parent', 'other')}
        targets['child'] = place
        db = NS(get_place_from_gramps_id=targets.get,
                get_place_from_handle=targets.get, commit_place=lambda *args: None)
        plugin.dbstate = NS(db=db)
        plugin.type_dic = {'loaded': True}
        for name, value in [('skip_parent_places', True),
                            ('sort_place_references', sort),
                            ('update_existing_places', update)]:
            setattr(plugin, name, NS(get_active=lambda v=value: v))
        plugin._CustomGOVImport__log = lambda *args: None
        plugin._CustomGOVImport__clean_blacklist = lambda values: values
        plugin._CustomGOVImport__get_place = lambda *args: (place, incoming, '')
        plugin._CustomGOVImport__update_place_values = lambda *args: None
        plugin._CustomGOVImport__is_gov_id = lambda *args: True
        plugin._CustomGOVImport__import_places('child')
        return place.refs

    def test_equal_bound_spans_collapse_and_repeat_is_stable(self):
        for value in [(0, 0, 1885, False), (0, 0, 1900, False),
                      (0, 12, 1885, False), (1, 12, 1885, False)]:
            for update in (False, True):
                single = Date(value=value)
                span = Date(value=value + value, modifier=Date.MOD_SPAN)
                for dates in ((span, span, single), (single, span, span), (span, span)):
                    with self.subTest(value=value, update=update, dates=dates):
                        incoming = [('parent', single), ('parent', single)]
                        refs = self.run_import([Ref(date=d) for d in dates], incoming, update)
                        self.assertEqual(len(refs), 1)
                        self.assertEqual(refs[0].date.serialize(), single.serialize())
                        self.assertEqual(len(self.run_import(refs, incoming, update)), 1)

    def test_unconfirmed_dates_and_targets_are_preserved(self):
        for ref in [Ref('other', Date(value=(0,0,1885,False)*2, modifier=Date.MOD_SPAN)),
                    Ref(date=Date(value=(0,0,1886,False)*2, modifier=Date.MOD_SPAN)),
                    Ref(date=Date(value=(0,0,1982,False,0,0,2015,False), modifier=Date.MOD_SPAN))]:
            original = ref.date.serialize()
            result = self.run_import([ref], [('parent', Date())])
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].date.serialize(), original)

    def test_open_dates_are_still_normalized(self):
        for old, new in [(Date.MOD_FROM, Date.MOD_AFTER), (Date.MOD_TO, Date.MOD_BEFORE)]:
            result = self.run_import([Ref(date=Date(modifier=old))]*2,
                                     [('parent', Date(modifier=new))])
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].date.modifier, new)


if __name__ == '__main__':
    unittest.main()
