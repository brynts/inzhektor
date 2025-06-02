import subprocess

subprocess.run([
    "./ipapatch", "--noconfirm",
    "--input", "package/input.ipa",
    "--output", "package/patched.ipa"
], check=True)
