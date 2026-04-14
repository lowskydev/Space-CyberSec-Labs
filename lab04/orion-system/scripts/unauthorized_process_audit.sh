#!/bin/bash

WHITELIST=("sleep" "bash" "zsh" "ps" "grep" "awk" "sed" "cat" "ls" "sh")

AUTHORIZED=0
UNAUTHORIZED=0

while read -r pid comm; do
    found=0
    for allowed in "${WHITELIST[@]}"; do
        if [ "$comm" = "$allowed" ]; then
            found=1
            break
        fi
    done

    if [ "$found" -eq 1 ]; then
        echo "AUTHORIZED PROCESS: $comm (PID: $pid)"
        AUTHORIZED=$((AUTHORIZED + 1))
    else
        echo "UNAUTHORIZED PROCESS: $comm (PID: $pid)"
        UNAUTHORIZED=$((UNAUTHORIZED + 1))
    fi
done < <(ps -eo pid,comm --no-headers)

echo "TOTAL AUTHORIZED: $AUTHORIZED"
echo "TOTAL UNAUTHORIZED: $UNAUTHORIZED"
