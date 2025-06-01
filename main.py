import subprocess

# Ensure the correct path for ipapatch (assuming it's in the current directory)
subprocess.run([
    "./ipapatch", "--noconfirm",
    "--input", "package/input.ipa",
    "--output", "package/patched.ipa"
], check=True)