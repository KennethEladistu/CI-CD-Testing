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
[ Laptop A – Pusher (PH Team) ]
        |
        |  python scripts/pusher.py
        v
[ GitHub Repository ]
        |
        |  auto pull every 30 seconds
        v
[ Laptop B – Receiver (Customer Site) ]
        |
        |  runs robot_task.py automatically
        v
[ Updated robot behavior visible on screen ]
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

### Laptop A (Pusher)
```bash
git clone https://github.com/KennethEladistu/CI-CD-Testing.git
cd CI-CD-Testing
```

### Laptop B (Receiver)
```bash
git clone https://github.com/KennethEladistu/CI-CD-Testing.git
cd CI-CD-Testing
python3 scripts/receiver.py
```

---

## Usage

### Pushing an Update (Laptop A)

1. Edit `robot_task.py` — change arm speed, delay, message, etc.
2. Run the pusher:
```bash
python scripts/pusher.py --version v1.0.5 --message "increase arm speed to 100"
```
3. Laptop B picks up the update automatically within 30 seconds.

### What the Pusher Does
1. Updates the `VERSION` file
2. Runs `robot_task.py` locally to verify it works
3. Commits and pushes to GitHub

### What the Receiver Does
1. Polls GitHub every 30 seconds
2. Detects a new version
3. Pulls the update
4. Runs `robot_task.py` automatically

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
