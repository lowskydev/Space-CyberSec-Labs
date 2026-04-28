#!/usr/bin/env python3
import subprocess

count = 0

# TCP listeners
tcp_result = subprocess.run(
    ["lsof", "-i", "TCP", "-P", "-n"],
    capture_output=True, text=True
)

seen_tcp = set()
for line in tcp_result.stdout.splitlines():
    if "(LISTEN)" not in line:
        continue
    parts = line.split()
    cmd, pid = parts[0], parts[1]
    addr = parts[-2]
    addr = addr.replace("*:", "0.0.0.0:")
    key = (cmd, pid, addr)
    if key in seen_tcp:
        continue
    seen_tcp.add(key)
    print(f"LISTENING SERVICE: tcp {addr} {cmd} {pid}")
    count += 1

# UDP listeners (no LISTEN state; detect by absence of ->)
udp_result = subprocess.run(
    ["lsof", "-i", "UDP", "-P", "-n"],
    capture_output=True, text=True
)

seen_udp = set()
for line in udp_result.stdout.splitlines():
    if line.startswith("COMMAND") or "->" in line:
        continue
    parts = line.split()
    if len(parts) < 9:
        continue
    cmd, pid = parts[0], parts[1]
    addr = parts[-1]
    addr = addr.replace("*:", "0.0.0.0:")
    key = (cmd, pid, addr)
    if key in seen_udp:
        continue
    seen_udp.add(key)
    print(f"LISTENING SERVICE: udp {addr} {cmd} {pid}")
    count += 1

print()
if count == 0:
    print("NO LISTENING SERVICES DETECTED")
else:
    print(f"TOTAL LISTENING SERVICES: {count}")
