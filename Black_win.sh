#!/bin/bash

pipe=$(find /dev/shm/ -maxdepth 1 -name '*.pipe' -type p | head -n 1)

if [[ -z "$pipe" ]]; then
    echo "No pipe found matching /dev/shm/*.pipe"
    exit 1
fi

echo "Starting cat /dev/random > $pipe in background"
cat /dev/random > "$pipe" &

python3 freeze_script.py
