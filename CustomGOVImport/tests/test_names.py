"""Regression coverage for 1.2.2 name and empty-date reconciliation."""
import copy
import unittest
import test_relationships as relationships
from test_relationships import Date, Ref, load_plugin


def empty(text=False):
    return Date(value=(0, 0, 0, False), modifier=Date.MOD_TEXTONLY if text else Date.MOD_NONE)


class Name:
    def __init__(self, value, lang='de', date=None):
        self.value, self.lang, self.date = value, lang, Date(date or empty())
    def get_value(self): return self.value
    def get_language(self): return self.lang
    def get_date_object(self): return self.date
    def set_date_object(self, date): self.date = Date(date)


class NamedPlace:
    def __init__(self, names):
        self.main = Name('Primary')
        self.names = names
    def get_name(self): return self.main
    def set_name(self, name): self.main = name
    def get_alternative_names(self): return self.names
    def get_all_names(self): return [self.main] + self.names
    def set_alternative_names(self, names): self.names = names
    def get_latitude(self): return ''
    def get_longitude(self): return ''
    def get_url_list(self): return []
    def set_url_list(self, urls): pass


class NamesTest(unittest.TestCase):
    def setUp(self):
        self.plugin = load_plugin()
        self.update = self.plugin._CustomGOVImport__update_place_values
        self.key = self.plugin._CustomGOVImport__name_identity

    def test_open_dates_deduplicate_per_language(self):
        for old, new in [(Date.MOD_FROM, Date.MOD_AFTER), (Date.MOD_TO, Date.MOD_BEFORE)]:
            existing = [Name('Same', lang, Date(modifier=m))
                        for lang in ('de', 'nl', 'en') for m in (old, new)]
            place = NamedPlace(existing)
            fetched = NamedPlace([Name('Same', lang, Date(modifier=new)) for lang in ('de', 'nl', 'en')])
            for _ in range(2):
                self.update(place, fetched, '')
                self.assertEqual(len(place.names), 3)
                self.assertEqual({n.lang for n in place.names}, {'de', 'en', 'nl'})
                self.assertTrue(all(n.date.modifier == new for n in place.names))

    def test_empty_dates_after_manual_clear_and_reload(self):
        place = NamedPlace([Name('Kalbe', date=empty()), Name('Kalbe', date=empty(True))])
        for _ in range(4):
            self.update(place, NamedPlace([Name('Kalbe', date=empty(True))]), '')
            self.assertEqual(len(place.names), 1)
            # Editor clears via parser; DateBase stores an empty date as None.
            place.names[0].date = empty(True)
            place = copy.deepcopy(place)
            place.names[0].date = empty()

    def test_equal_bound_spans(self):
        for value in [(0,0,1900,False), (0,12,1885,False), (1,12,1885,False)]:
            place = NamedPlace([Name('Same', date=Date(value=value*2, modifier=Date.MOD_SPAN))])
            single = Date(value=value)
            self.update(place, NamedPlace([Name('Same', date=single)]), '')
            self.assertEqual(len(place.names), 1)
            self.assertEqual(place.names[0].date.serialize(), single.serialize())

    def test_unconfirmed_names_and_historical_periods_preserved(self):
        span = Date(value=(0,0,1945,False,0,0,1947,False), modifier=Date.MOD_SPAN)
        names = [Name('Same', date=span), Name('Local'), Name('Local')]
        place = NamedPlace(copy.deepcopy(names))
        self.update(place, NamedPlace([Name('Same', date=Date())]), '')
        self.assertEqual([self.key(n) for n in place.names[:3]], [self.key(n) for n in names])
        self.assertEqual(len(place.names), 4)

    def test_primary_duplicate_removed(self):
        place = NamedPlace([Name('Primary')])
        self.update(place, NamedPlace([]), '')
        self.assertEqual(place.names, [])

    def test_date_text(self):
        a, b = Date(), Date()
        a.text, b.text = '1885', 'different spelling'
        self.assertEqual(self.key(Name('X', date=a)), self.key(Name('X', date=b)))
        a.modifier = b.modifier = Date.MOD_TEXTONLY
        self.assertNotEqual(self.key(Name('X', date=a)), self.key(Name('X', date=b)))
        self.assertNotEqual(self.key(Name('X', date=a)), self.key(Name('X', date=empty())))

    def test_sorting_option_in_import(self):
        names = [Name('late-nl','nl',Date(value=(0,0,1990,False))), Name('undated'),
                 Name('early','de',Date(value=(0,0,1934,False))),
                 Name('late-en','en',Date(value=(0,0,1990,False)))]
        harness = relationships.RelationshipsTest()
        for enabled in (False, True):
            harness.run_import([], [], names=names, sort=enabled)
            self.assertEqual([n.value for n in harness.last_place.names],
                             ['early','late-nl','late-en','undated'] if enabled else [n.value for n in names])


class EmptyReferencesTest(unittest.TestCase):
    def test_empty_reference_roundtrips(self):
        harness = relationships.RelationshipsTest()
        for update in (False, True):
            refs = [Ref(date=empty()), Ref(date=empty(True))]
            for _ in range(4):
                refs = harness.run_import(refs, [('parent', empty(True))]*2, update)
                self.assertEqual(len(refs), 1)
                refs[0].date = empty(True)  # manual clearing
                refs = copy.deepcopy(refs)
                refs[0].date = empty()  # database reload

    def test_other_targets_and_real_dates_remain(self):
        harness = relationships.RelationshipsTest()
        refs = [Ref('other', empty()), Ref(date=Date())]
        result = harness.run_import(refs, [('parent', empty(True))])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].ref, 'other')
        self.assertEqual(result[1].date.serialize(), refs[1].date.serialize())


if __name__ == '__main__':
    unittest.main()
