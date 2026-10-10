"""Kekulé numbering along main parent families. GPL-2.0-or-later."""


def build_index(db, home_handle, max_depth=100, max_paths=100000, translate=None):
    """Return handle -> sorted numbers, plus notices for incomplete traversal.

    Path-local cycle detection preserves multiple paths to shared ancestors.
    Bounds protect the UI from erroneous cycles and exponential pedigree growth.
    """
    _ = translate if translate is not None else (lambda message: message)
    index = {}
    warnings = set()
    stack = [(home_handle, 1, 0, frozenset())]
    parents_cache = {}
    visited = 0
    while stack:
        if visited >= max_paths:
            warnings.add(_("Calculation limit reached; the list of numbers may be incomplete"))
            break
        handle, number, depth, path = stack.pop()
        if handle in path:
            warnings.add(_("Cyclic parent relationship skipped"))
            continue
        person = db.get_person_from_handle(handle)
        if person is None:
            warnings.add(_("Missing person record skipped"))
            continue
        visited += 1
        index.setdefault(handle, set()).add(number)
        if handle not in parents_cache:
            family_handle = person.get_main_parents_family_handle()
            family = db.get_family_from_handle(family_handle) if family_handle else None
            if family_handle and family is None:
                warnings.add(_("Missing parent family skipped"))
            parents_cache[handle] = (
                (family.get_father_handle(), family.get_mother_handle())
                if family else (None, None)
            )
        father, mother = parents_cache[handle]
        if depth >= max_depth:
            if father or mother:
                warnings.add(_("Generation limit reached; the list of numbers may be incomplete"))
            continue
        next_path = path | {handle}
        if mother:
            stack.append((mother, number * 2 + 1, depth + 1, next_path))
        if father:
            stack.append((father, number * 2, depth + 1, next_path))
    return {handle: sorted(numbers) for handle, numbers in index.items()}, sorted(warnings)
