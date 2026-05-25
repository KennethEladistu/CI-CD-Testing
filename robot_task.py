"""
robot_task.py — Simulates the ARMOR Kit robot actions
This is the file that will be updated and pushed to the receiver.
"""

# ── Configuration ──────────────────────────────────────────────────────────────
ARM_SPEED        = 90       # Robot arm speed (mm/s)
EXTRACTION_DELAY = 1.0      # Delay between actions (seconds)
TASK_MESSAGE     = "Picking up mail item and placing on letter opener"

# ── Read Version ───────────────────────────────────────────────────────────────
import time

with open("VERSION", "r") as f:
    VERSION = f.read().strip()

# ── Simulate Robot Actions ─────────────────────────────────────────────────────
print("=" * 50)
print("  ARMOR Kit – Robot Task Runner")
print(f"  Version         : {VERSION}")
print(f"  Arm Speed       : {ARM_SPEED} mm/s")
print(f"  Extraction Delay: {EXTRACTION_DELAY}s")
print("=" * 50)

print("\n[ROBOT] Starting task...")
time.sleep(EXTRACTION_DELAY)

print(f"[ROBOT] {TASK_MESSAGE}")
time.sleep(EXTRACTION_DELAY)

print("[ROBOT] Presenting mail to downdraft table...")
time.sleep(EXTRACTION_DELAY)

print("[ROBOT] Extraction complete. Returning to home position...")
time.sleep(EXTRACTION_DELAY)

print("\n[ROBOT] ✅ Task finished successfully.")