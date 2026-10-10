"""d'Aboville descendant paths in Gramps' stored order. GPL-2.0-or-later."""


def build_descendant_index(db, home_handle, max_depth=100, max_paths=100000, translate=None):
    """Return handle -> all path numbers, plus notices for incomplete traversal.

    Children are counted across a person's families in their stored order,
    as in Gramps' detailed descendant report. Only each current path is
    checked for cycles, so shared descendants retain every valid number.
    """
    _ = translate if translate is not None else (lambda message: message)
    index = {}
    warnings = set()
    children_cache = {}
    stack = [(home_handle, (1,), 0, frozenset())]
    visited = 0
    while stack:
        if visited >= max_paths:
            warnings.add(_("Calculation limit reached; the list of numbers may be incomplete"))
            break
        handle, number, depth, path = stack.pop()
        if handle in path:
            warnings.add(_("Cyclic child relationship skipped"))
            continue
        person = db.get_person_from_handle(handle)
        if person is None:
            warnings.add(_("Missing person record skipped"))
            continue
        visited += 1
        index.setdefault(handle, set()).add(number)
        if handle not in children_cache:
            children = []
            for family_handle in person.get_family_handle_list():
                family = db.get_family_from_handle(family_handle)
                if family is None:
                    warnings.add(_("Missing family skipped"))
                    continue
                children.extend(ref.get_reference_handle()
                                for ref in family.get_child_ref_list())
            children_cache[handle] = children
        children = children_cache[handle]
        if depth >= max_depth:
            if children:
                warnings.add(_("Generation limit reached; the list of numbers may be incomplete"))
            continue
        next_path = path | {handle}
        # Reverse stack insertion retains the stored family and child order.
        for position, child_handle in reversed(list(enumerate(children, 1))):
            if child_handle:
                stack.append((child_handle, number + (position,), depth + 1, next_path))
            else:
                warnings.add(_("Missing child reference skipped"))
    return {
        handle: [".".join(map(str, number)) for number in sorted(numbers)]
        for handle, numbers in index.items()
    }, sorted(warnings)
