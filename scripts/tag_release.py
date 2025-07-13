import re
import subprocess
from pathlib import Path

# Path to your version file (adjust as needed)
version_file = Path(__file__).parent.parent / "comfyenv" / "version.py"
content = version_file.read_text()

# Extract version from __version__ = "..."
match = re.search(r'__version__\s*=\s*"(.+?)"', content)
if not match:
    raise RuntimeError("Version not found in version.py")

tag = match.group(1)

# Check if the tag already exists
existing_tags = subprocess.check_output(["git", "tag"], text=True).splitlines()
if tag in existing_tags:
    print(f"Tag {tag} already exists.")
else:
    # Create the tag
    subprocess.run(["git", "tag", tag])
    print(f"Created tag: {tag}")

    # Optional: push the tag
    push = input("Push tag to origin? (y/n): ").strip().lower()
    if push == "y":
        subprocess.run(["git", "push", "origin", tag])
