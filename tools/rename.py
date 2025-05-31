#!/usr/bin/env python3

import zipfile
import plistlib
import os

ipa_path = "package/patched.ipa"

with zipfile.ZipFile(ipa_path, "r") as ipa:
    plist_path = next(x for x in ipa.namelist() if x.endswith("Info.plist") and "Payload/" in x)
    with ipa.open(plist_path) as f:
        plist = plistlib.load(f)
        name = plist.get("CFBundleDisplayName") or plist.get("CFBundleName")
        version = plist.get("CFBundleShortVersionString")

new_name = f"{name}_v{version}.ipa".replace(" ", "_")
new_path = f"package/{new_name}"

os.rename(ipa_path, new_path)

# Simpan nama file untuk release
with open("output_filename.txt", "w") as f:
    f.write(new_path)
