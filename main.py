import plistlib
import subprocess
import zipfile
import os

# Patch IPA
subprocess.run([
    "ipapatch", "--noconfirm",
    "--input", "package/input.ipa",
    "--output", "package/patched.ipa"
], check=True)

# Baca Info.plist
with zipfile.ZipFile("package/patched.ipa") as ipa:
    plist_path = next(x for x in ipa.namelist() if x.endswith("Info.plist") and "Payload/" in x)
    with ipa.open(plist_path) as f:
        plist = plistlib.load(f)
        name = plist.get("CFBundleDisplayName") or plist.get("CFBundleName")
        version = plist.get("CFBundleShortVersionString")

# Rename
new_name = f"{name}_v{version}.ipa".replace(" ", "_")
os.rename("package/patched.ipa", f"package/{new_name}")