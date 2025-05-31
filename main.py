import subprocess
import os
import shutil
import plistlib
import zipfile
import argparse
import re

def sanitize_filename_component(component_str):
    """Membersihkan string untuk digunakan dalam nama file."""
    component_str = re.sub(r'[^\w\s.-]', '', component_str) # Hapus karakter tidak aman
    component_str = component_str.strip() # Hapus spasi di awal/akhir
    # Ganti spasi dengan underscore jika diinginkan, atau biarkan (tergantung preferensi)
    # component_str = component_str.replace(' ', '_') 
    return component_str if component_str else "Unknown"

def get_ipa_info(ipa_path):
    """Mengekstrak BundleDisplayName dan CFBundleShortVersionString dari Info.plist di dalam IPA."""
    bundle_display_name = "PatchedApp" # Default jika tidak ditemukan
    version_short = "1.0"       # Default jika tidak ditemukan
    payload_plist_path = None

    try:
        with zipfile.ZipFile(ipa_path, 'r') as ipa_zip:
            for name in ipa_zip.namelist():
                if name.startswith('Payload/') and name.endswith('.app/Info.plist'):
                    payload_plist_path = name
                    break
            
            if payload_plist_path:
                with ipa_zip.open(payload_plist_path) as plist_file:
                    plist_data = plistlib.load(plist_file)
                    bundle_display_name = plist_data.get('CFBundleDisplayName', plist_data.get('CFBundleName', bundle_display_name))
                    version_short = plist_data.get('CFBundleShortVersionString', version_short)
            else:
                print(f"::warning::Info.plist tidak ditemukan di dalam '{ipa_path}'. Menggunakan nama default.")
    except Exception as e:
        print(f"::warning::Gagal membaca Info.plist dari '{ipa_path}': {e}. Menggunakan nama default.")
    
    return sanitize_filename_component(bundle_display_name), sanitize_filename_component(version_short)

def main():
    parser = argparse.ArgumentParser(description="Patch IPA menggunakan ipapatch dan rename outputnya.")
    parser.add_argument("--ipapatch_tool", required=True, help="Path ke executable ipapatch.")
    parser.add_argument("--ipa_input_original", required=True, help="Path ke file input.ipa asli (sebelum masuk ke 'package').")
    # Argumen lain untuk ipapatch bisa ditambahkan di sini jika perlu, misal:
    # parser.add_argument("--ipapatch_options", default="", help="Opsi tambahan untuk ipapatch.")

    args = parser.parse_args()

    # 1. Buat direktori 'package' jika belum ada
    package_dir = "package"
    os.makedirs(package_dir, exist_ok=True)
    print(f"Direktori '{package_dir}' disiapkan.")

    # Salin file IPA input asli ke dalam package_dir sebagai 'input.ipa'
    # Ini karena command ipapatch yang diminta menggunakan 'package/input.ipa'
    packaged_input_ipa_path = os.path.join(package_dir, "input.ipa")
    shutil.copy(args.ipa_input_original, packaged_input_ipa_path)
    print(f"File IPA input '{args.ipa_input_original}' disalin ke '{packaged_input_ipa_path}'.")

    temp_patched_ipa_name = "patched.ipa" # Nama output sementara dari ipapatch
    temp_patched_ipa_path = os.path.join(package_dir, temp_patched_ipa_name)

    # 2. Jalankan command ipapatch
    # Contoh: ipapatch --noconfirm --input package/input.ipa --output package/patched.ipa
    cmd = [
        args.ipapatch_tool,
        "--noconfirm",
        "--input", packaged_input_ipa_path,
        "--output", temp_patched_ipa_path
    ]
    # Jika ada opsi tambahan:
    # if args.ipapatch_options:
    #     cmd.extend(args.ipapatch_options.split())

    print(f"Menjalankan: {' '.join(cmd)}")
    try:
        process_result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print("Output ipapatch (stdout):")
        print(process_result.stdout)
        if process_result.stderr:
            print("Output ipapatch (stderr):")
            print(process_result.stderr)
        print("ipapatch berhasil dijalankan.")
    except subprocess.CalledProcessError as e:
        print(f"::error::Gagal menjalankan ipapatch. Return code: {e.returncode}")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
        exit(1) # Keluar jika ipapatch gagal

    # 3. Rename patched.ipa ke {BundleDisplayName}_v{VersionShort}.ipa
    if not os.path.exists(temp_patched_ipa_path):
        print(f"::error::File output '{temp_patched_ipa_path}' tidak ditemukan setelah ipapatch.")
        exit(1)

    print(f"Mendapatkan info dari IPA yang telah dipatch: {temp_patched_ipa_path}")
    app_name, app_version = get_ipa_info(temp_patched_ipa_path)
    
    final_ipa_name = f"{app_name}_v{app_version}.ipa"
    # File final akan diletakkan di direktori kerja utama (luar 'package')
    # atau bisa juga di direktori 'package' jika diinginkan, atau di $GITHUB_WORKSPACE
    final_ipa_path = os.path.join(os.getcwd(), final_ipa_name) 

    print(f"Nama file final yang akan digunakan: {final_ipa_name}")
    shutil.move(temp_patched_ipa_path, final_ipa_path)
    print(f"File IPA telah direname dan dipindahkan ke: {final_ipa_path}")

    # Jika berjalan di GitHub Actions, set output untuk langkah selanjutnya
    github_output_file = os.getenv('GITHUB_OUTPUT')
    if github_output_file:
        with open(github_output_file, 'a') as f:
            f.write(f"final_ipa_path={final_ipa_path}\n") # Path absolut ke file IPA final
            f.write(f"final_ipa_filename={final_ipa_name}\n") # Hanya nama file IPA final
    else:
        # Jika tidak dalam GHA, cukup print path-nya untuk informasi.
        print(f"Path output file IPA final (non-GHA): {final_ipa_path}")


if __name__ == "__main__":
    main()
