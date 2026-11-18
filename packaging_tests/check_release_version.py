"""Check that release assets match the version encoded in the built wheel."""

import sys
import zipfile
from email import message_from_bytes
from pathlib import Path

release_tag, distribution_dir = sys.argv[1:3]
expected_version = release_tag.removeprefix("v")
distribution_path = Path(distribution_dir)
wheels = list(distribution_path.glob("pvade-*.whl"))
sdists = list(distribution_path.glob("pvade-*.tar.gz"))

if len(wheels) != 1 or len(sdists) != 1:
    raise SystemExit("Expected exactly one pvade wheel and one source distribution")

with zipfile.ZipFile(wheels[0]) as wheel:
    metadata_path = next(
        name for name in wheel.namelist() if name.endswith(".dist-info/METADATA")
    )
    metadata = message_from_bytes(wheel.read(metadata_path))

package_version = metadata["Version"]
if metadata["Name"].lower() != "pvade":
    raise SystemExit(f"Built distribution has unexpected name: {metadata['Name']}")
if package_version != expected_version:
    raise SystemExit(
        f"Release tag {release_tag!r} does not match package version {package_version!r}"
    )
if not sdists[0].name.startswith(f"pvade-{package_version}."):
    raise SystemExit(f"Source distribution version does not match {package_version}")

print(f"Release tag {release_tag} matches pvade {package_version}")
