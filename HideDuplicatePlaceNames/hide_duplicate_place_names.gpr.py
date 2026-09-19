register(
    GENERAL,
    id="hide-duplicate-place-names",
    name=_("Hide duplicate place names"),
    description=_(
        "Combines immediately consecutive identical place names for "
        "selected place types."
    ),
    version="1.0.1",
    gramps_target_version="6.0",
    fname="hide_duplicate_place_names_load.py",
    category=TOOL_UTILS,
    load_on_reg=True,
    status=STABLE,
    authors=["Sebastian Klossek"],
)
