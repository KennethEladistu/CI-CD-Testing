"""
pusher.py — Run this on Laptop A (PH / Pusher machine)
This script updates the VERSION file and pushes it to GitHub.

Usage:
    python scripts/pusher.py --version v1.0.1 --message "your update message"
"""

import argparse
import subprocess
import sys


def run(command):
    """Run a shell command and print the output."""
    print(f"  >> {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="ARMOR Kit – Pusher Script")
    parser.add_argument("--version", required=True, help="Version tag e.g. v1.0.1")
    parser.add_argument("--message", required=True, help="Commit message e.g. 'update robot config'")
    args = parser.parse_args()

    print("=" * 50)
    print("  ARMOR Kit – Pusher")
    print(f"  Version : {args.version}")
    print(f"  Message : {args.message}")
    print("=" * 50)

    # Step 1 — Update VERSION file
    print("\n[STEP 1] Updating VERSION file...")
    with open("VERSION", "w") as f:
        f.write(args.version)
    print(f"  ✅ VERSION set to {args.version}")

    # Step 2 — Git add, commit, push
    print("\n[STEP 2] Committing and pushing to GitHub...")
    run("git add .")
    run(f'git commit -m "release: {args.version} - {args.message}"')
    code = run("git push origin main")

    if code == 0:
        print("\n" + "=" * 50)
        print(f"  ✅ Successfully pushed {args.version} to GitHub")
        print("=" * 50)
    else:
        print("\n  ❌ Push failed. Check your internet connection or GitHub credentials.")
        sys.exit(1)


if __name__ == "__main__":
    main()
