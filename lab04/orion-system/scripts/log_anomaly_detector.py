#!/usr/bin/env python3

import subprocess
import sys
import glob
import os

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <ERROR_THRESHOLD>")
    sys.exit(1)

threshold = int(sys.argv[1])
logs_dir = "../logs"

print("Processing log files...")

max_errors = 0
max_file = ""

for log_file in sorted(glob.glob(os.path.join(logs_dir, "*.log"))):
    filename = os.path.basename(log_file)

    result = subprocess.run(
        ["grep", "-c", "ERROR", log_file],
        capture_output=True, text=True
    )
    count = int(result.stdout.strip()) if result.stdout.strip() else 0

    print(f"{filename}: {count} ERROR entries")

    if count > threshold:
        print(f"ALERT: log anomaly detected in {filename}")

    if count > max_errors:
        max_errors = count
        max_file = filename

print(f"Most unstable log file: {max_file} ({max_errors} ERROR entries)")
