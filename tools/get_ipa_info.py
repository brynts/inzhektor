#!/usr/bin/env python3
import plistlib
import zipfile
import sys
import argparse
import os

def extract_info_from_ipa(ipa_path):
    try:
        with zipfile.ZipFile(ipa_path, 'r') as ipa_zip:
            info_plist_path = None
            # Cari Info.plist di dalam direktori Payload/*.app/
            for member in ipa_zip.namelist():
                if member.startswith('Payload/') and member.endswith('.app/Info.plist'):
                    info_plist_path = member
                    break

            if not info_plist_path:
                print("Error: Info.plist tidak ditemukan di dalam file IPA.", file=sys.stderr)
                sys.exit(1)

            with ipa_zip.open(info_plist_path) as info_file:
                info_data = plistlib.load(info_file)

                bundle_display_name = info_data.get('CFBundleDisplayName', '')
                bundle_name = info_data.get('CFBundleName', 'UnknownApp')
                short_version = info_data.get('CFBundleShortVersionString', '1.0')

                # Prioritaskan CFBundleDisplayName, fallback ke CFBundleName jika kosong
                app_name = bundle_display_name if bundle_display_name else bundle_name

                print(f"APP_NAME={app_name}")
                print(f"APP_VERSION={short_version}")

    except FileNotFoundError:
        print(f"Error: File IPA tidak ditemukan di '{ipa_path}'.", file=sys.stderr)
        sys.exit(1)
    except zipfile.BadZipFile:
        print(f"Error: File '{ipa_path}' bukan file ZIP yang valid atau rusak.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error saat memproses IPA: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ekstrak CFBundleDisplayName dan CFBundleShortVersionString dari Info.plist di dalam file IPA.")
    parser.add_argument("ipa_file", help="Path menuju file .ipa")
    args = parser.parse_args()
    extract_info_from_ipa(args.ipa_file)
