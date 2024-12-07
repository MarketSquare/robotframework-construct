uv lock
uv sync --extra test

for target in ["regmap", "reflector", "base"]:
    uv run cosmic-ray init f"mutation_testing/mutation_{target}.toml" f"mutation_testing/mutation_{target}.toml.sqlite"
    uv run cosmic-ray --verbosity=INFO baseline f"mutation_testing/mutation_{target}.toml"
    uv run cosmic-ray exec f"mutation_testing/mutation_{target}.toml" f"mutation_testing/mutation_{target}.toml.sqlite"
    uv run cr-filter-pragma session.sqlite f"mutation_testing/mutation_{target}.toml.sqlite"
    uv run cr-html f"mutation_testing/mutation_{target}.toml.sqlite" > f"report_mutations_{target}.html"
    uv run cr-report f"mutation_testing/mutation_{target}.toml.sqlite"

for target in ["regmap", "reflector", "base"]:
    r = $(uv run cr-report f"mutation_testing/mutation_{target}.toml.sqlite")
    assert "surviving mutants: 0" in r
