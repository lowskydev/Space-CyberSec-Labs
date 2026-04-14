#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <ERROR_THRESHOLD>"
    exit 1
fi

THRESHOLD=$1
LOGS_DIR="../logs"

echo "Processing log files..."

MAX_ERRORS=0
MAX_FILE=""

for log_file in "$LOGS_DIR"/*.log; do
    filename=$(basename "$log_file")
    count=$(grep -c "ERROR" "$log_file" 2>/dev/null; true)
    echo "$filename: $count ERROR entries"

    if [ "$count" -gt "$THRESHOLD" ]; then
        echo "ALERT: log anomaly detected in $filename"
    fi

    if [ "$count" -gt "$MAX_ERRORS" ]; then
        MAX_ERRORS=$count
        MAX_FILE=$filename
    fi
done

echo "Most unstable log file: $MAX_FILE ($MAX_ERRORS ERROR entries)"
