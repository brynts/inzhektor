#!/usr/bin/env python3

import subprocess

subprocess.run([
    "ipapatch", "--noconfirm",
    "--input", "package/input.ipa",
    "--output", "package/patched.ipa"
], check=True)