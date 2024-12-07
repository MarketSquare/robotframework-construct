uv lock
uv sync --extra test

uv run robot -L TRACE -e hardware -P atests/regmapmockup/ -P atests/bson/ atests/
uv run pytest -x tests/__init__.py
uv run ruff check src
