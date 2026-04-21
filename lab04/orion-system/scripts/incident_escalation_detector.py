#!/usr/bin/env python3

import subprocess
import sys
import time
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)

cpu_threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 50
error_threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 3
interval = 5

def get_classification():
    result = subprocess.run(["python3", "./incident_classifier.py", str(cpu_threshold), str(error_threshold)], capture_output=True, text=True)
    return result.stdout.strip()

ESCALATION_ORDER = {"NORMAL": 0, "WARNING": 1, "CRITICAL": 2}

print("Starting escalation monitoring...")
print("Press Ctrl+C to stop.")
print("-" * 40)

prev_status = get_classification()
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initial status: {prev_status}")

try:
    while True:
        time.sleep(interval)
        curr_status = get_classification()
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{curr_time}] Status: {curr_status}")

        if ESCALATION_ORDER.get(curr_status, 0) > ESCALATION_ORDER.get(prev_status, 0):
            print()
            print("ESCALATION DETECTED:")
            print(f"Time: {curr_time}")
            print(f"From: {prev_status}")
            print(f"To: {curr_status}")
            sys.exit(0)

        prev_status = curr_status

except KeyboardInterrupt:
    pass
