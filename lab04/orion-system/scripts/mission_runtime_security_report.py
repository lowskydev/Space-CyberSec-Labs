#!/usr/bin/env python3

import subprocess
import sys
import glob
import os
from datetime import datetime

cpu_threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 50
error_threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 3

WHITELIST = {"sleep", "bash", "zsh", "ps", "grep", "awk", "sed", "cat", "ls", "sh"}
LOGS_DIR = "../logs"

gen_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"../reports/mission_runtime_security_report_{gen_time}.txt"

# Count log files
log_files = sorted(glob.glob(os.path.join(LOGS_DIR, "*.log")))

# Active processes
result = subprocess.run("ps -eo pid --no-headers | wc -l", shell=True, capture_output=True, text=True)
active_procs = result.stdout.strip()

# Unauthorized processes
result = subprocess.run(["ps", "-eo", "pid,comm", "--no-headers"], capture_output=True, text=True)
unauthorized = sum(1 for line in result.stdout.strip().splitlines() if line.split(maxsplit=1)[1] not in WHITELIST)

# High CPU processes
result = subprocess.run(["ps", "-eo", "pid,%cpu", "--no-headers"], capture_output=True, text=True)
high_cpu = sum(1 for line in result.stdout.strip().splitlines() if float(line.split()[1]) > cpu_threshold)

# Log stats
total_errors = 0
max_errors = 0
max_file = ""
for log_file in log_files:
    result = subprocess.run(["grep", "-c", "ERROR", log_file], capture_output=True, text=True)
    count = int(result.stdout.strip()) if result.stdout.strip() else 0
    total_errors += count
    if count > max_errors:
        max_errors = count
        max_file = os.path.basename(log_file)

# Top CPU process
result = subprocess.run("ps -eo pid,%cpu,comm --no-headers --sort=-%cpu | head -1", shell=True, capture_output=True, text=True)
_, _, top_comm = result.stdout.strip().split(maxsplit=2)

# Incident classification
result = subprocess.run(["python3", "./incident_classifier.py", str(cpu_threshold), str(error_threshold)], capture_output=True, text=True)
classification = result.stdout.strip()

lines = [
    "MISSION RUNTIME SECURITY REPORT",
    f"Generated at: {gen_time}",
    f"Processed log files: {len(log_files)}",
    f"Active processes: {active_procs}",
    f"Unauthorized processes: {unauthorized}",
    f"High CPU processes: {high_cpu}",
    f"ERROR entries: {total_errors}",
    f"Most unstable log: {max_file}",
    f"Top CPU process: {top_comm}",
    f"Incident classification: {classification}",
]

output = "\n".join(lines)
print(output)
with open(output_file, "w") as f:
    f.write(output + "\n")
