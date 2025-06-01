#!/usr/bin/env python3

import os
import zipfile
import plistlib
import sys
import os

patched_ipa = "package/patched.ipa"
if not os.path.exists(patched_ipa):
    raise FileNotFoundError("patched.ipa not found.")

# Ambil dari variabel lingkungan jika ada, jika tidak gunakan fallback
name = os.getenv("ORIGINAL_DISPLAY_NAME", os.path.basename("package/input.ipa").replace(".ipa", ""))
version = os.getenv("ORIGINAL_VERSION", "0.0")

with zipfile.ZipFile(patched_ipa) as ipa:
    plist_path = next(
        x for x in ipa.namelist()
        if x.endswith("Info.plist") and x.startswith("Payload/")
    )
    with ipa.open(plist_path) as f:
        plist = plistlib.load(f)
        print(f"Full plist: {plist}", file=sys.stderr)  # Log isi lengkap untuk debug

print(f"CFBundleDisplayName: {name}", file=sys.stderr)
print(f"CFBundleShortVersionString: {version}", file=sys.stderr)

new_name = f"{name}_v{version}.ipa".replace(" ", "_").replace(".", "_")
new_path = f"package/{new_name}"

os.rename(patched_ipa, new_path)

# ONLY output path IPA di stdout
sys.stdout.write(new_path)