import os
import zipfile
import plistlib
import sys

patched_ipa = "package/patched.ipa"
if not os.path.exists(patched_ipa):
    raise FileNotFoundError("patched.ipa not found.")

with zipfile.ZipFile(patched_ipa) as ipa:
    plist_path = next(
        x for x in ipa.namelist()
        if x.endswith("Info.plist") and x.startswith("Payload/")
    )
    with ipa.open(plist_path) as f:
        plist = plistlib.load(f)
        name = plist.get("CFBundleDisplayName") or plist.get("CFBundleName") or "App"
        version = plist.get("CFBundleShortVersionString") or "0.0"

# Logging ke stderr (supaya tidak masuk stdout)
print(f"CFBundleDisplayName: {name}", file=sys.stderr)
print(f"CFBundleShortVersionString: {version}", file=sys.stderr)

new_name = f"{name}_v{version}.ipa".replace(" ", "_")
new_path = f"package/{new_name}"

os.rename(patched_ipa, new_path)

# ONLY output path IPA di stdout
sys.stdout.write(new_path)