#!/bin/bash

if [ -z "$1" ] 
then
    echo "No match argument"
    exit 1
fi

total=$(grep -o WARN logs/*.log | sort | uniq -c)
echo "total lines (mathing $1):"
echo "$total"

