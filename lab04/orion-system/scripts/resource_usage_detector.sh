#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <CPU_THRESHOLD> <MEM_THRESHOLD>"
    exit 1
fi

CPU_THRESHOLD=$1
MEM_THRESHOLD=$2

ps -eo pid,comm,%cpu,%mem --no-headers | while read pid comm cpu mem; do
    cpu_int=${cpu%.*}
    mem_int=${mem%.*}

    if [ "$cpu_int" -gt "$CPU_THRESHOLD" ] 2>/dev/null; then
        echo "WARNING: suspicious CPU usage: $comm (PID: $pid)"
    fi

    if [ "$mem_int" -gt "$MEM_THRESHOLD" ] 2>/dev/null; then
        echo "WARNING: suspicious memory usage: $comm (PID: $pid)"
    fi
done
