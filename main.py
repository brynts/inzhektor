import subprocess
import zipfile
import plistlib
import os

# Jalankan ipapatch untuk mem-patch IPA
subprocess.run([
    "./ipapatch", "--noconfirm",
    "--input", "package/input.ipa",
    "--output", "package/patched.ipa"
], check=True)

# Ekstrak Info.plist dari Payload/*.app/Info.plist
def extract_plist(ipa_path):
    with zipfile.ZipFile(ipa_path, 'r') as ipa:
        for file in ipa.namelist():
            if file.endswith('Info.plist') and 'Payload/' in file:
                with ipa.open(file) as plist_file:
                    return plistlib.load(plist_file)
    raise Exception("Info.plist tidak ditemukan di IPA")

# Ambil metadata dari Info.plist
patched_ipa = "package/patched.ipa"
plist = extract_plist(patched_ipa)
display_name = plist.get("CFBundleDisplayName", "input")
version = plist.get("CFBundleShortVersionString", "0.0")

# Ganti nama file IPA
new_ipa_name = f"package/{display_name}_v{version}.ipa"
os.rename(patched_ipa, new_ipa_name)

# Cetak path baru untuk digunakan di workflow
print(f"final_ipa_path={new_ipa_name}")