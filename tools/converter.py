#!/usr/bin/env python3

import argparse
import re
import sys
import os
import urllib.request

def convert_google_drive_link(url):
    match = re.search(r'/file/d/([^/]+)', url)
    if match:
        file_id = match.group(1).split('?')[0]
        return f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Konversi link Google Drive dan download sebagai IPA.")
    parser.add_argument("gdrive_url", help="Google Drive URL")
    parser.add_argument("-o", "--output", help="Path file output (.ipa)", required=True)
    args = parser.parse_args()

    direct_url = convert_google_drive_link(args.gdrive_url)
    if not direct_url:
        print(f"Error: URL Google Drive tidak valid: '{args.gdrive_url}'", file=sys.stderr)
        sys.exit(1)

    try:
        urllib.request.urlretrieve(direct_url, args.output)
        if not os.path.exists(args.output) or os.path.getsize(args.output) == 0:
            raise Exception("File kosong atau tidak terunduh.")
    except Exception as e:
        print(f"Error saat mengunduh file: {e}", file=sys.stderr)
        sys.exit(1)