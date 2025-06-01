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
        name = plist.get("CFBundleDisplayName") or plist.get("CFBundleName") or os.path.basename("package/input.ipa").replace(".ipa", "")
        version = plist.get("CFBundleShortVersionString") or "0.0"

print(f"CFBundleDisplayName: {name}", file=sys.stderr)
print(f"CFBundleShortVersionString: {version}", file=sys.stderr)

new_name = f"{name}_v{version}.ipa".replace(" ", "_")
new_path = f"package/{new_name}"

os.rename(patched_ipa, new_path)

sys.stdout.write(new_path)