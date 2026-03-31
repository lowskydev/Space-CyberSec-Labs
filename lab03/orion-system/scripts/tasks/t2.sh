#!/bin/bash

total=$(grep $2 $1 | wc -l)
echo "total lines (mathing $2): $total"

