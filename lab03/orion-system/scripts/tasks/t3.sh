#!/bin/bash

if [ -z "$1" ] 
then
    echo "No log file provided"
    exit 1
fi

if [ -z "$2" ] 
then
    echo "No match argument"
    exit 1
fi

total=$(grep $2 $1 | wc -l)
echo "total lines (mathing $2): $total"

