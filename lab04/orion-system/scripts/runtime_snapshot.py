#!/usr/bin/env python3

import subprocess
import sys
import glob
import os
from datetime import datetime

cpu_threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 50
error_threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 10

WHITELIST = {"sleep", "bash", "zsh", "ps", "grep", "awk", "sed", "cat", "ls", "sh"}
LOGS_DIR = "../logs"

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
snapshot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"../reports/runtime_snapshot_{snapshot_time}.txt"

# Total active processes
result = subprocess.run("ps -eo pid --no-headers | wc -l", shell=True, capture_output=True, text=True)
total_procs = result.stdout.strip()

# Top CPU process (pid,%cpu,comm so cpu is always second field)
result = subprocess.run("ps -eo pid,%cpu,comm --no-headers --sort=-%cpu | head -1", shell=True, capture_output=True, text=True)
top_pid, top_cpu, top_comm = result.stdout.strip().split(maxsplit=2)

# Unauthorized processes
result = subprocess.run(["ps", "-eo", "pid,comm", "--no-headers"], capture_output=True, text=True)
unauth_list = [(line.split(maxsplit=1)[0], line.split(maxsplit=1)[1]) for line in result.stdout.strip().splitlines() if line.split(maxsplit=1)[1] not in WHITELIST]
unauthorized = len(unauth_list)

# Log stats
total_errors = 0
max_errors = 0
max_file = ""
log_summary = []
log_anomaly = False

for log_file in sorted(glob.glob(os.path.join(LOGS_DIR, "*.log"))):
    filename = os.path.basename(log_file)
    result = subprocess.run(["grep", "-c", "ERROR", log_file], capture_output=True, text=True)
    count = int(result.stdout.strip()) if result.stdout.strip() else 0
    log_summary.append((filename, count))
    total_errors += count
    if count > error_threshold:
        log_anomaly = True
    if count > max_errors:
        max_errors = count
        max_file = filename

# Incident classification
result = subprocess.run(["python3", "./incident_classifier.py", str(cpu_threshold), str(error_threshold)], capture_output=True, text=True)
classification = result.stdout.strip()

# Triggered indicators
triggered = []
if float(top_cpu) > cpu_threshold:
    triggered.append(f"- high CPU: top process {top_comm} (PID={top_pid}) uses {top_cpu}% > threshold {cpu_threshold}%")
if unauthorized > 0:
    triggered.append(f"- unauthorized processes detected: {unauthorized}")
if log_anomaly:
    triggered.append(f"- log anomaly: at least one mission log exceeds ERROR threshold {error_threshold}")

summary_map = {"NORMAL": "no suspicious indicators were observed", "WARNING": "exactly one suspicious indicator was observed", "CRITICAL": "at least two suspicious indicators were observed simultaneously"}

lines = [
    "========================================",
    "Runtime Security Snapshot",
    "========================================",
    f"Date and time: {now}",
    f"Total active processes: {total_procs}",
    f"Top CPU process: PID={top_pid} PROC={top_comm} CPU={top_cpu}%",
    f"Unauthorized processes: {unauthorized}",
    f"Total ERROR entries across all logs: {total_errors}",
    f"Incident classification: {classification}",
    f"Classification summary: {summary_map.get(classification, '')}",
    "-" * 40,
    "Thresholds:",
    f"- CPU threshold: {cpu_threshold}%",
    f"- ERROR threshold per log: {error_threshold}",
    "-" * 40,
    "Triggered indicators:",
]
lines += triggered if triggered else ["- none"]
lines += ["-" * 40, "Log summary:"]
lines += [f"- {name}: {count} ERROR entries" for name, count in log_summary]
lines += [f"Most unstable log: {max_file} ({max_errors} ERROR entries)", "-" * 40, "Unauthorized process details:"]
lines += [f"- PID={pid} PROC={comm}" for pid, comm in unauth_list] if unauth_list else ["- none"]

output = "\n".join(lines)
print(output)
with open(output_file, "w") as f:
    f.write(output + "\n")
