import os
import subprocess
import tempfile
import requests
from app_manager import load_programs


def download_file(url, destination):
    print(f"🔗 Downloading file from {url}...")
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ File saved: {destination}")
        return destination
    except requests.RequestException as e:
        print(f"❌ Download failed: {e}")
        return None


def install_program(program):
    name = program["name"]
    source = program["source"]
    args = program["install_args"]

    is_remote = source.startswith("http")
    temp_dir = tempfile.gettempdir()
    local_path = os.path.join(temp_dir, os.path.basename(source)) if is_remote else source

    try:
        if is_remote:
            print(f"🌐 '{name}' — remote URL. Starting download...")
            downloaded = download_file(source, local_path)
            if not downloaded:
                raise RuntimeError(f"Failed to download file for '{name}'.")
        else:
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"File not found: {local_path}")

        print(f"⚙️ Running installer: '{name}'")
        cmd = f'"{local_path}" {args}'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )

        print(f"🟢 Exit code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"🔴 STDERR:\n{result.stderr}")

    except Exception as e:
        print(f"💥 Installation error for '{name}': {e}")
    finally:
        if is_remote and os.path.exists(local_path):
            os.remove(local_path)
            print(f"🗑️ Temporary file removed: {local_path}")


def run_installer():
    print("\n🚀 Starting installer...\n")

    programs = sorted(load_programs(), key=lambda p: p.get("priority", float('inf')))

    if not programs:
        print("⚠️ No programs to install.")
        return

    for program in programs:
        name = program["name"]
        print(f"\n📦 Installing program: {name}")
        install_program(program)

    print("\n🎉 Installer has finished.")