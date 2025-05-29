import subprocess
import sys
import os
import platform
import shutil
import socket

MIN_PYTHON = (3, 9)
REQUIREMENTS_FILE = "requirements.txt"
ENTRY_POINT = "main.py"

def fail(message: str):
    print(f"[ERROR] {message}")
    sys.exit(1)

def info(message: str):
    print(f"[INFO] {message}")

def check_python_version():
    if sys.version_info < MIN_PYTHON:
        fail(f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required. You are using {platform.python_version()}.")

def check_requirements_file():
    if not os.path.exists(REQUIREMENTS_FILE):
        fail(f"Missing '{REQUIREMENTS_FILE}'.")

def has_internet(timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        return False

def install_dependencies():
    info("Installing required Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])
    except subprocess.CalledProcessError:
        fail("Failed to install Python dependencies.")

def detect_linux_distro():
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"').lower()
    except FileNotFoundError:
        return "unknown"

def install_package_linux(package):
    distro = detect_linux_distro()
    try:
        if shutil.which("sudo") is None:
            fail("Missing 'sudo' command. Cannot install system packages automatically.")

        if distro in ["debian", "ubuntu", "pop", "linuxmint"]:
            subprocess.check_call(["sudo", "apt", "update"])
            subprocess.check_call(["sudo", "apt", "install", "-y", package])
        elif distro in ["arch", "manjaro"]:
            subprocess.check_call(["sudo", "pacman", "-Sy", package, "--noconfirm"])
        elif distro in ["fedora", "rhel", "centos"]:
            subprocess.check_call(["sudo", "dnf", "install", "-y", package])
        elif distro == "alpine":
            subprocess.check_call(["sudo", "apk", "add", package])
        else:
            fail(f"Unsupported Linux distribution for auto-install: {distro}")
    except subprocess.CalledProcessError:
        fail(f"Failed to install system package: {package}")

def ensure_alsa_installed():
    if not shutil.which("aplay"):
        info("ALSA not found. Attempting to install alsa-utils...")
        install_package_linux("alsa-utils")

def ensure_gcc_installed():
    if not shutil.which("gcc"):
        info("GCC not found. Attempting to install gcc...")
        install_package_linux("build-essential" if detect_linux_distro() in ["debian", "ubuntu", "pop", "linuxmint"] else "gcc")

def try_imports():
    try:
        import textual
        import simpleaudio
    except ImportError:
        info("Python packages not found. Attempting to install them.")
        install_dependencies()
        try:
            import textual
            import simpleaudio
        except ImportError:
            fail("Failed to import required Python packages after installation.")

def run_game():
    if not os.path.exists(ENTRY_POINT):
        fail(f"Entry point '{ENTRY_POINT}' not found.")
    info("Launching the game...")
    try:
        subprocess.run([sys.executable, ENTRY_POINT], check=True)
    except subprocess.CalledProcessError as e:
        fail(f"Game exited with error: {e}")

def main():
    check_python_version()
    check_requirements_file()

    if platform.system() == "Linux":
        if not has_internet():
            fail("No internet connection. Cannot install required system packages.")
        ensure_gcc_installed()
        ensure_alsa_installed()

    try_imports()
    run_game()

if __name__ == "__main__":
    main()
