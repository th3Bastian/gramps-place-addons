"""Numbering and UI-logic regressions without GTK. GPL-2.0-or-later."""
import ast
import gettext
import importlib.util
import itertools
import locale
import re
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def load_helper(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ancestors = load_helper('kekule_index').build_index
descendants = load_helper('daboville_index').build_descendant_index


class Person:
    def __init__(self, handle, parents=None, families=()):
        self.handle = handle; self.parents = parents; self.families = families
    def get_handle(self): return self.handle
    def get_gramps_id(self): return self.handle
    def get_main_parents_family_handle(self): return self.parents
    def get_family_handle_list(self): return self.families


class Family:
    def __init__(self, father=None, mother=None, children=()):
        self.father = father; self.mother = mother; self.children = children
    def get_father_handle(self): return self.father
    def get_mother_handle(self): return self.mother
    def get_child_ref_list(self):
        return [SimpleNamespace(get_reference_handle=lambda h=h: h) for h in self.children]


class DB:
    def __init__(self):
        self.people = {
            'home': Person('home', 'parents', ('kids1', 'kids2')),
            'father': Person('father', 'paternal'), 'mother': Person('mother', 'maternal'),
            'shared_ancestor': Person('shared_ancestor'),
            'a': Person('a', families=('grandkids1',)),
            'b': Person('b', families=('grandkids2',)), 'c': Person('c'),
            'shared_child': Person('shared_child'), 'outside': Person('outside')}
        self.families = {
            'parents': Family('father', 'mother'), 'paternal': Family('shared_ancestor'),
            'maternal': Family(mother='shared_ancestor'),
            'kids1': Family(children=('a', 'b')), 'kids2': Family(children=('c',)),
            'grandkids1': Family(children=('shared_child',)),
            'grandkids2': Family(children=('shared_child',))}
        self.home = self.people['home']
    def get_default_person(self): return self.home
    def get_person_from_handle(self, handle): return self.people.get(handle)
    def get_family_from_handle(self, handle): return self.families.get(handle)


class NumberingTest(unittest.TestCase):
    def test_ancestry_gaps_and_multiple_paths(self):
        result, notices = ancestors(DB(), 'home')
        self.assertEqual(result['shared_ancestor'], [4, 7])
        self.assertEqual(result['home'], [1]); self.assertFalse(notices)
        self.assertNotIn('outside', result)
    def test_descendants_across_families_and_multiple_paths(self):
        result, notices = descendants(DB(), 'home')
        self.assertEqual(result['c'], ['1.3'])
        self.assertEqual(result['shared_child'], ['1.1.1', '1.2.1'])
        self.assertFalse(notices)
        self.assertNotIn('father', result)
    def test_numeric_path_sorting(self):
        db = DB(); db.families['kids1'].children = ('c',) * 10
        db.people['home'].families = ('kids1',)
        self.assertEqual(descendants(db, 'home')[0]['c'], ['1.' + str(n) for n in range(1, 11)])
    def test_changed_reference_person(self):
        self.assertEqual(descendants(DB(), 'b')[0]['shared_child'], ['1.1'])
        self.assertEqual(ancestors(DB(), 'mother')[0]['shared_ancestor'], [3])
    def test_cycles_do_not_remove_valid_paths(self):
        db = DB(); db.people['shared_child'].families = ('loop',)
        db.families['loop'] = Family(children=('home',))
        result, notices = descendants(db, 'home')
        self.assertEqual(result['shared_child'], ['1.1.1', '1.2.1'])
        self.assertEqual(result['home'], ['1']); self.assertTrue(notices)
        db.people['shared_ancestor'].parents = 'parents'
        self.assertTrue(ancestors(db, 'home')[1])
    def test_missing_records_preserve_child_positions(self):
        db = DB(); db.families['kids1'].children = ('missing', 'b')
        result, notices = descendants(db, 'home')
        self.assertEqual(result['b'], ['1.2']); self.assertTrue(notices)
        del db.people['shared_ancestor']; self.assertTrue(ancestors(db, 'home')[1])
    def test_limits_report_incomplete_traversal(self):
        for builder in (ancestors, descendants):
            self.assertTrue(builder(DB(), 'home', max_depth=0)[1])
            self.assertTrue(builder(DB(), 'home', max_paths=1)[1])


class DisplayTest(unittest.TestCase):
    def test_all_display_combinations_and_cache_invalidation(self):
        tree = ast.parse((ROOT / 'customdetails.py').read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef)); cls.bases = []
        cls.body = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in {'display_kekule', 'invalidate_kekule', 'clean_attribute_types'}]
        namespace = {'_': lambda text: text, 'build_index': ancestors, 'build_descendant_index': descendants, 'locale': locale,
                     'name_displayer': SimpleNamespace(display=lambda person: person.handle)}
        exec(compile(ast.Module(body=[cls], type_ignores=[]), 'customdetails', 'exec'), namespace)
        view = namespace['CustomDetails'](); db = DB(); view.dbstate = SimpleNamespace(db=db)
        view.load_settings = lambda: None; view.update = lambda: None
        view.relationship_to_home = lambda home, person: 'Relative'
        rows = []; view.add_row = lambda key, value: rows.append((key, value))
        keys = ('display.home', 'display.relationship', 'display.kekule', 'display.daboville')
        labels = ('Reference person', 'Kinship', 'Kekulé number', 'd’Aboville number')
        for flags in itertools.product((False, True), repeat=4):
            view.display_settings = dict(zip(keys, flags)); view.invalidate_kekule(); rows.clear()
            view.display_kekule(db.people['shared_child'])
            self.assertEqual([key for key, _value in rows], [label for label, flag in zip(labels, flags) if flag])
            self.assertEqual(view._kekule_cache is not None, flags[2])
            self.assertEqual(view._daboville_cache is not None, flags[3])
            home = db.home; db.home = None; rows.clear(); view.display_kekule(db.people['outside'])
            self.assertEqual(len(rows), sum(flags)); db.home = home
        self.assertEqual(view.clean_attribute_types(' Titel\nBERUF\nberuf\nReligion\n'), ['BERUF', 'Religion', 'Titel'])


class TranslationTest(unittest.TestCase):
    def test_complete_catalogs_and_format_placeholders(self):
        messages = set()
        for source in ROOT.glob('*.py'):
            for node in ast.walk(ast.parse(source.read_text())):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == '_' and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    messages.add(node.args[0].value)
        for language in ('de', 'en'):
            translation = gettext.translation('addon', localedir=str(ROOT / 'locale'), languages=[language])
            for message in messages:
                self.assertIn(message, translation._catalog)
                self.assertTrue(translation.gettext(message))
                pattern = r'%(?:\([^)]+\))?[sd]'
                self.assertEqual(sorted(re.findall(pattern, message)), sorted(re.findall(pattern, translation.gettext(message))))
            db = DB(); del db.people['father']
            self.assertIn(translation.gettext('Missing person record skipped'), ancestors(db, 'home', translate=translation.gettext)[1])
    def test_registration(self):
        data = {}
        exec((ROOT / 'customdetails.gpr.py').read_text(), {'register': lambda *args, **kwargs: data.update(kwargs), 'GRAMPLET': 10, 'STABLE': 3, '_': lambda text: text})
        self.assertEqual(data['id'], 'CustomDetails')
        self.assertEqual(data['gramps_target_version'], '6.0')
        self.assertTrue((ROOT / data['fname']).exists())


if __name__ == '__main__':
    unittest.main()
