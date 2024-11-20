#release checklist
#- update docu.:

version="0.1.4"

uv run libdoc f"--version={version}" --name=robotframework_construct.reflector src/robotframework_construct/reflector.py  docs/robotframework-construct.reflector.html
uv run libdoc f"--version={version}" --name=robotframework_construct.regmap src/robotframework_construct/regmap.py  docs/robotframework-construct.regmap.html
uv run libdoc f"--version={version}" src/robotframework_construct  docs/robotframework-construct.html
