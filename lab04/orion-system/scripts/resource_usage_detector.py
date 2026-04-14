#!/usr/bin/env python3

import subprocess
import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <CPU_THRESHOLD> <MEM_THRESHOLD>")
    sys.exit(1)

cpu_threshold = float(sys.argv[1])
mem_threshold = float(sys.argv[2])

result = subprocess.run(
    ["ps", "-eo", "pid,%cpu,%mem,comm", "--no-headers"],
    capture_output=True, text=True
)

for line in result.stdout.strip().splitlines():
    pid, cpu, mem, comm = line.split(maxsplit=3)
    if float(cpu) > cpu_threshold:
        print(f"WARNING: suspicious CPU usage: {comm} (PID: {pid})")
    if float(mem) > mem_threshold:
        print(f"WARNING: suspicious memory usage: {comm} (PID: {pid})")
