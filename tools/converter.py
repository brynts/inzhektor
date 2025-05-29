#!/usr/bin/env python3

import argparse
import re

def convert_google_drive_link(url):
    match = re.search(r'/file/d/([^/]+)', url)
    
    if match:
        file_id = match.group(1)
        file_id = file_id.split('?')[0]
        
        new_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
        return new_url
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Konversi link Google Drive ke link download langsung.")
    parser.add_argument("gdrive_url", help="URL Google Drive yang akan dikonversi.")
    
    args = parser.parse_args()
    
    converted_url = convert_google_drive_link(args.gdrive_url)
    
    if converted_url:
        print(converted_url)
    else:
        import sys
        print(f"Error: Format URL Google Drive tidak valid atau File ID tidak ditemukan di '{args.gdrive_url}'.", file=sys.stderr)
        sys.exit(1)
