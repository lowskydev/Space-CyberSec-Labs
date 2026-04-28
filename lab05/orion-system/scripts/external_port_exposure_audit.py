#!/usr/bin/env python3
import subprocess
import sys

EXPECTED_PORTS = {1, 5000, 6000}
TARGET = "127.0.0.1"

result = subprocess.run(
    ["nmap", "-n", "-p-", TARGET],
    capture_output=True, text=True
)

open_ports = []
for line in result.stdout.splitlines():
    if "/tcp" in line and "open" in line:
        port = int(line.split("/")[0])
        open_ports.append(port)

unexpected_count = 0
for port in sorted(open_ports):
    if port not in EXPECTED_PORTS:
        print(f"EXPOSED PORT: {port}")
        unexpected_count += 1

if unexpected_count == 0:
    print("NO UNEXPECTED EXPOSED PORTS")
else:
    print(f"TOTAL UNEXPECTED EXPOSED PORTS: {unexpected_count}")
