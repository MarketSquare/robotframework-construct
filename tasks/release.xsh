import os

git_status = !(git status)
git_status = (str(git_status).split(os.linesep))
print(git_status)
assert "nothing to commit, working tree clean" in git_status[1], f"please commit all changes before releasing (nothing to commit) {git_status[1]}"

version= input("which version to release?\n")

version = version.split(".")
assert len(version) == 3, "version must be in format x.y.z"
assert version[0].isdigit(), "version must be in format x.y.z"
assert version[1].isdigit(), "version must be in format x.y.z"
assert version[2].isdigit(), "version must be in format x.y.z"

uv run libdoc f"--version={version}" src/robotframework_construct  docs/index.html
cp docs/index.html f"docs/robotframework_construct_{version}.html"
git add docs/index.html f"docs/robotframework_construct_{version}.html"
git commit -m f"release {version}"
uv build
