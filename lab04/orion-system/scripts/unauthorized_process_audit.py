#!/usr/bin/env python3

import subprocess

WHITELIST = {"sleep", "bash", "zsh", "ps", "grep", "awk", "sed", "cat", "ls", "sh"}

result = subprocess.run(
    ["ps", "-eo", "pid,comm", "--no-headers"],
    capture_output=True, text=True
)

authorized = 0
unauthorized = 0

for line in result.stdout.strip().splitlines():
    pid, comm = line.split(maxsplit=1)
    if comm in WHITELIST:
        print(f"AUTHORIZED PROCESS: {comm} (PID: {pid})")
        authorized += 1
    else:
        print(f"UNAUTHORIZED PROCESS: {comm} (PID: {pid})")
        unauthorized += 1

print(f"TOTAL AUTHORIZED: {authorized}")
print(f"TOTAL UNAUTHORIZED: {unauthorized}")
