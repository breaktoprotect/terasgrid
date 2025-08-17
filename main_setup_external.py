import os
import subprocess

TOOLS_DIR = "external_tools"
REPO_URL = "https://github.com/Octomany/cisbenchmarkconverter.git"
DEST_DIR = os.path.join(TOOLS_DIR, "cisbenchmarkconverter")

if not os.path.exists(TOOLS_DIR):
    os.makedirs(TOOLS_DIR)

if not os.path.exists(DEST_DIR):
    subprocess.check_call(["git", "clone", REPO_URL, DEST_DIR])
    print("[+] Cloned cisbenchmarkconverter into external_tools/")
    req_path = os.path.join(DEST_DIR, "requirements.txt")
else:
    print("[*] cisbenchmarkconverter already exists. Skipping clone.")
