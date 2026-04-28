#!/usr/bin/env python3
import subprocess

count = 0

result = subprocess.run(
    ["lsof", "-i", "TCP", "-P", "-n"],
    capture_output=True, text=True
)

seen = set()
for line in result.stdout.splitlines():
    if "(ESTABLISHED)" not in line:
        continue
    parts = line.split()
    cmd, pid = parts[0], parts[1]
    conn = parts[-2]
    key = (cmd, pid, conn)
    if key in seen:
        continue
    seen.add(key)
    local, remote = conn.split("->")
    print(f"ESTABLISHED CONNECTION: {local} -> {remote} {cmd} {pid}")
    count += 1

print()
if count == 0:
    print("NO ESTABLISHED CONNECTIONS DETECTED")
else:
    print(f"TOTAL ESTABLISHED CONNECTIONS: {count}")
