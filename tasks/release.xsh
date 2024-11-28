import os

git_status = (str(!(git status)).split(os.linesep))
assert "nothing to commit, working tree clean" in git_status[1], f"please commit all changes before releasing (nothing to commit) {git_status[1]}"

version= input("which version to release?\n")

version = version.split(".")
assert len(version) == 3, "version must be in format x.y.z"
for item in version:
    assert item.isdigit(), "version must be in format x.y.z"

version = ".".join(version)

uv run libdoc f"--version={version}" src/robotframework_construct  docs/index.html
cp docs/index.html f"docs/robotframework_construct_{version}.html"
git add docs/index.html f"docs/robotframework_construct_{version}.html"
git commit -m f"release {version}"
git tag f"v{version}" -m "release {version} release process"
uv build
uv publish
git push
