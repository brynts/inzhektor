import os
import zipfile
import plistlib

patched_ipa = "package/patched.ipa"
if not os.path.exists(patched_ipa):
    raise FileNotFoundError("patched.ipa not found.")

with zipfile.ZipFile(patched_ipa) as ipa:
    plist_path = next(x for x in ipa.namelist() if x.endswith("Info.plist") and x.startswith("Payload/"))
    with ipa.open(plist_path) as f:
        plist = plistlib.load(f)
        name = plist.get("CFBundleDisplayName") or plist.get("CFBundleName") or "App"
        version = plist.get("CFBundleShortVersionString") or "0.0"

# Create new name and sanitize spaces
new_name = f"{name}_v{version}.ipa".replace(" ", "_")
new_path = f"package/{new_name}"

# Rename the IPA file
os.rename(patched_ipa, new_path)

# Output the final IPA path for GitHub Actions
with open(os.environ['GITHUB_OUTPUT'], "a") as out:
    out.write(f"final_ipa_path={new_path}\n")