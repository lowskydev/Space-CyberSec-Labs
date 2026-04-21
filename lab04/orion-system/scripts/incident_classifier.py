#!/usr/bin/env python3

import subprocess
import sys
import glob
import os

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <CPU_THRESHOLD> <ERROR_THRESHOLD>")
    sys.exit(1)

cpu_threshold = float(sys.argv[1])
error_threshold = int(sys.argv[2])

WHITELIST = {"sleep", "bash", "zsh", "ps", "grep", "awk", "sed", "cat", "ls", "sh"}
LOGS_DIR = "../logs"

indicators = 0

# Check if any process exceeds CPU threshold
result = subprocess.run(["ps", "-eo", "pid,%cpu", "--no-headers"], capture_output=True, text=True)
for line in result.stdout.strip().splitlines():
    pid, cpu = line.split()
    if float(cpu) > cpu_threshold:
        indicators += 1
        break

# Check if any unauthorized process is present
result = subprocess.run(["ps", "-eo", "pid,comm", "--no-headers"], capture_output=True, text=True)
for line in result.stdout.strip().splitlines():
    pid, comm = line.split(maxsplit=1)
    if comm not in WHITELIST:
        indicators += 1
        break

# Check if any log file exceeds the ERROR threshold
for log_file in sorted(glob.glob(os.path.join(LOGS_DIR, "*.log"))):
    result = subprocess.run(["grep", "-c", "ERROR", log_file], capture_output=True, text=True)
    count = int(result.stdout.strip()) if result.stdout.strip() else 0
    if count > error_threshold:
        indicators += 1
        break

if indicators == 0:
    print("NORMAL")
elif indicators == 1:
    print("WARNING")
else:
    print("CRITICAL")
