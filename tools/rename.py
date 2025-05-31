import os
import zipfile
import plistlib

patched_ipa = "package/patched.ipa"
if not os.path.exists(patched_ipa):
    raise FileNotFoundError("patched.ipa not found.")

# Ekstrak Info.plist dari IPA
with zipfile.ZipFile(patched_ipa) as ipa:
    # Mencari Info.plist di dalam folder Payload
    plist_path = next(x for x in ipa.namelist() if x.endswith("Info.plist") and x.startswith("Payload/"))
    
    with ipa.open(plist_path) as f:
        plist = plistlib.load(f)
        
        # Cek apakah nilai ada di plist
        name = plist.get("CFBundleDisplayName") or plist.get("CFBundleName") or "App"
        version = plist.get("CFBundleShortVersionString") or "0.0"
        
        # Debug: Print nilai yang ditemukan
        print(f"CFBundleDisplayName: {name}")
        print(f"CFBundleShortVersionString: {version}")

# Tentukan nama baru untuk IPA
new_name = f"{name}_v{version}.ipa".replace(" ", "_")
new_path = f"package/{new_name}"

# Rename file IPA yang sudah di-patch
os.rename(patched_ipa, new_path)

# Outputkan path file IPA yang sudah di-rename ke GitHub Actions
print(new_path)  # Pastikan output hanya berupa path file IPA yang baru
with open(os.environ['GITHUB_OUTPUT'], "a") as out:
    out.write(f"final_ipa_path={new_path}\n")