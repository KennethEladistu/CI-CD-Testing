# CI-CD-Testing
CI-CD Testing with 2 laptops for deployment

## Overview
This repository demonstrates a basic CI/CD pipeline using GitHub as the central 
source of truth between two machines — a **Pusher (Laptop A)** and a 
**Receiver (Laptop B)**. This simulates how the ARMOR Kit would receive remote 
updates from the PH team to a deployed unit at a customer site (e.g. Orlando).

---

## How It Works

```
┌──────────────────────────────────┐
│      Laptop A  (PH Team)         │
│                                  │
│  1. Edit robot_task.py           │
│  2. Run pusher.py                │
│     --version v1.0.6             │
│     --message "your change"      │
└────────────────┬─────────────────┘
                 │
                 │  git push
                 ▼
┌──────────────────────────────────┐
│         GitHub Repository        │
│                                  │
│   Stores latest code + VERSION   │
└────────────────┬─────────────────┘
                 │
                 │  git fetch every 30 sec
                 ▼
┌──────────────────────────────────┐
│   Laptop B  (Customer Site)      │
│                                  │
│  receiver.py running in loop:    │
│                                  │
│  New version? ──No──► wait 30s ─┐│
│       │                         ││
│      Yes                        ││
│       │                         ││
│  git pull                       ││
│       │                         ││
│  run robot_task.py              ││
│       │                         ││
│  wait 30s ──────────────────────┘│
└──────────────────────────────────┘
```

---

## Repository Structure

```
CI-CD-Testing/
├── robot_task.py          ← Simulates robot actions (this is what gets updated)
├── VERSION                ← Tracks the current deployed version
├── scripts/
│   ├── pusher.py          ← Run on Laptop A to push updates
│   └── receiver.py        ← Run on Laptop B to watch and pull updates
└── README.md
```

---

## Setup

### Requirements
Both laptops need:
- Python 3.8 or higher
- Git

---

## Laptop A (Pusher — PH Team)

### 1. Clone the repo (one-time setup)
```bash
git clone https://github.com/KennethEladistu/CI-CD-Testing.git
cd CI-CD-Testing
```

### 2. Edit `robot_task.py`
Change arm speed, delay, task message, or any robot behavior.

### 3. Push the update
```bash
python scripts/pusher.py --version v1.0.6 --message "your change here"
```

That's it — Laptop B will pick it up automatically within 30 seconds.

---

## Laptop B (Receiver — Customer Site)

### 1. Clone the repo (one-time setup)
```bash
git clone https://github.com/KennethEladistu/CI-CD-Testing.git
cd CI-CD-Testing
```

### 2. Start the receiver and leave it running
```bash
python3 scripts/receiver.py
```

No other commands needed. The receiver handles everything automatically.

---

## What Each Script Does

### `pusher.py` (Laptop A)
1. Updates the `VERSION` file with the new version
2. Runs `robot_task.py` locally to verify it works
3. Commits and pushes to GitHub if the local run succeeds

### `receiver.py` (Laptop B)
1. Polls GitHub every 30 seconds
2. Compares local version vs remote version
3. Pulls the update if a new version is detected
4. Runs `robot_task.py` automatically after pulling

---

## Expected Terminal Output

### Laptop A (Pusher)
```
==================================================
  ARMOR Kit – Pusher
  Version : v1.0.5
  Message : increase arm speed to 100
==================================================
[STEP 1] Updating VERSION file...
  ✅ VERSION set to v1.0.5
[STEP 2] Running robot_task.py locally to verify...
  ✅ Local run successful.
[STEP 3] Committing and pushing to GitHub...
  ✅ Successfully pushed v1.0.5 to GitHub
  Laptop B will pick this up within 30 seconds
==================================================
```

### Laptop B (Receiver)
```
[POLLING] Local: v1.0.4  |  Remote: v1.0.4
  ✅ Already up to date.

[POLLING] Local: v1.0.4  |  Remote: v1.0.5
  🔔 New version detected: v1.0.5
  ⬇️  Pulling update...
  ✅ Update applied successfully. Now on: v1.0.5

[ROBOT] Starting task...
[ROBOT] Arm Speed: 100 mm/s
[ROBOT] ✅ Task finished successfully.
```

---

## Future Plans

| Addition | Purpose |
|---|---|
| **Tailscale VPN** | Allows PH team to reach customer site over the internet |
| **GitHub Actions** | Runs automated tests on every push before deployment |
| **S3 model storage** | Stores large AI model files in cloud storage |
| **Deployment approval gate** | Requires maintenance mode before update is applied |
