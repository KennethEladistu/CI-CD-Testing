"""
receiver.py — Run this on Laptop B (Customer Site / Receiver machine)
Polls GitHub every 30 seconds, detects new versions, pulls updates,
and runs robot_task.py automatically.

Usage:
    python3 scripts/receiver.py
"""

import subprocess
import time


POLL_INTERVAL = 30  # seconds


def run(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def get_local_version():
    try:
        with open("VERSION", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"


def get_remote_version():
    _, _, code = run("git fetch origin main")
    if code != 0:
        return None
    stdout, _, _ = run("git show origin/main:VERSION")
    return stdout.strip() if stdout else None


def main():
    print("=" * 50)
    print("  ARMOR Kit – Receiver")
    print(f"  Polling every {POLL_INTERVAL} seconds...")
    print("=" * 50)

    try:
        while True:
            local = get_local_version()
            remote = get_remote_version()

            if remote is None:
                print("\n[POLLING] ❌ Could not reach GitHub. Retrying...")
            else:
                print(f"\n[POLLING] Local: {local}  |  Remote: {remote}")

                if local == remote:
                    print("  ✅ Already up to date.")
                else:
                    print(f"  🔔 New version detected: {remote}")
                    print("  ⬇️  Pulling update...")
                    _, err, code = run("git pull origin main")
                    if code == 0:
                        new_version = get_local_version()
                        print(f"  ✅ Update applied successfully. Now on: {new_version}")
                        print("\n" + "-" * 50)
                        subprocess.run("python3 robot_task.py", shell=True)
                        print("-" * 50)
                    else:
                        print(f"  ❌ Pull failed: {err}")

            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n\n  🛑 Receiver stopped.")


if __name__ == "__main__":
    main()
