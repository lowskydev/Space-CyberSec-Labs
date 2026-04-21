#!/usr/bin/env python3

import subprocess
import sys
import time
import glob
import os
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)

cpu_threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 50
error_threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 3
interval = 5

WHITELIST = {"sleep", "bash", "zsh", "ps", "grep", "awk", "sed", "cat", "ls", "sh"}
LOGS_DIR = "../logs"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"../reports/runtime_monitor_{timestamp}.txt"

print("Starting monitoring loop...")
print(f"Interval: {interval}s")
print(f"Output: {output_file}")
print("Using: ./incident_classifier.py")
print("Press Ctrl+C to stop.")
print("-" * 40)

start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
header = f"===== Monitoring started: {start_time} ====="
print(header)
with open(output_file, "w") as f:
    f.write(header + "\n")

try:
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Top CPU process (pid,%cpu,comm so cpu is always second field)
        result = subprocess.run("ps -eo pid,%cpu,comm --no-headers --sort=-%cpu | head -1", shell=True, capture_output=True, text=True)
        top_pid, top_cpu, top_comm = result.stdout.strip().split(maxsplit=2)

        # Count unauthorized processes
        result = subprocess.run(["ps", "-eo", "pid,comm", "--no-headers"], capture_output=True, text=True)
        unauthorized = sum(1 for line in result.stdout.strip().splitlines() if line.split(maxsplit=1)[1] not in WHITELIST)

        # Check log anomaly
        log_anomaly = "NO"
        for log_file in sorted(glob.glob(os.path.join(LOGS_DIR, "*.log"))):
            result = subprocess.run(["grep", "-c", "ERROR", log_file], capture_output=True, text=True)
            count = int(result.stdout.strip()) if result.stdout.strip() else 0
            if count > error_threshold:
                log_anomaly = "YES"
                break

        # Get incident classification
        result = subprocess.run(["python3", "./incident_classifier.py", str(cpu_threshold), str(error_threshold)], capture_output=True, text=True)
        status = result.stdout.strip()

        line = f"[{now}] TOP_CPU: {top_comm} (PID={top_pid}, CPU={top_cpu}%) | UNAUTHORIZED: {unauthorized} | LOG_ANOMALY: {log_anomaly} | STATUS: {status}"
        print(line)
        with open(output_file, "a") as f:
            f.write(line + "\n")

        time.sleep(interval)

except KeyboardInterrupt:
    pass
