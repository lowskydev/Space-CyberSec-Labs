#!/usr/bin/env python3

import subprocess
import sys
import glob
import os
import time

cpu_threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 50
error_threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 10

WHITELIST = {"sleep", "bash", "zsh", "ps", "grep", "awk", "sed", "cat", "ls", "sh"}
LOGS_DIR = "../logs"

def get_state():
    # Top CPU process name (pid,%cpu,comm so cpu is always second field)
    result = subprocess.run("ps -eo pid,%cpu,comm --no-headers --sort=-%cpu | head -1", shell=True, capture_output=True, text=True)
    _, _, top_comm = result.stdout.strip().split(maxsplit=2)

    # Unauthorized count
    result = subprocess.run(["ps", "-eo", "pid,comm", "--no-headers"], capture_output=True, text=True)
    unauthorized = sum(1 for line in result.stdout.strip().splitlines() if line.split(maxsplit=1)[1] not in WHITELIST)

    # Incident classification
    result = subprocess.run(["python3", "./incident_classifier.py", str(cpu_threshold), str(error_threshold)], capture_output=True, text=True)
    classification = result.stdout.strip()

    return top_comm, unauthorized, classification

print("Taking snapshot 1...")
cpu1, unauth1, class1 = get_state()

print("Waiting 5 seconds...")
time.sleep(5)

print("Taking snapshot 2...")
cpu2, unauth2, class2 = get_state()

print()
print("STATE CHANGE DETECTED:")

cpu_changed = "YES" if cpu1 != cpu2 else "NO"
unauth_changed = f"YES ({unauth1} -> {unauth2})" if unauth1 != unauth2 else "NO"
class_changed = f"{class1} -> {class2}" if class1 != class2 else "NO"

print(f"Top CPU process changed: {cpu_changed}")
print(f"Unauthorized process count changed: {unauth_changed}")
print(f"Incident classification changed: {class_changed}")
