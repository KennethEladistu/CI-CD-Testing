"""
pusher.py — Run this on Laptop A (PH / Pusher machine)
This script updates the VERSION file, pushes to GitHub,
and runs robot_task.py locally to confirm the update looks correct.

Usage:
    python scripts/pusher.py --version v1.0.3 --message "your update message"
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
    parser.add_argument("--version", required=True, help="Version tag e.g. v1.0.3")
    parser.add_argument("--message", required=True, help="Commit message")
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

    # Step 2 — Run robot_task.py locally to confirm it works
    print("\n[STEP 2] Running robot_task.py locally to verify...")
    print("-" * 50)
    code = run("python3 robot_task.py")
    print("-" * 50)
    if code != 0:
        print("  ❌ robot_task.py failed. Fix the error before pushing.")
        sys.exit(1)
    print("  ✅ Local run successful.")

    # Step 3 — Git add, commit, push
    print("\n[STEP 3] Committing and pushing to GitHub...")
    run("git add .")
    run(f'git commit -m "release: {args.version} - {args.message}"')
    code = run("git push origin main")

    if code == 0:
        print("\n" + "=" * 50)
        print(f"  ✅ Successfully pushed {args.version} to GitHub")
        print(f"  Laptop B will pick this up within 30 seconds")
        print("=" * 50)
    else:
        print("\n  ❌ Push failed. Check your internet connection or GitHub credentials.")
        sys.exit(1)


if __name__ == "__main__":
    main()