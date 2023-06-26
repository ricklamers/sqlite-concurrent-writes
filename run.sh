#!/bin/bash

# Remove log_database.sqlite3 if it exists
if [ -f log_database.sqlite3 ]; then
    rm log_database.sqlite3
fi

# Define the range of the log entries
start=1
end=100

# Spawn 10 processes for log generation
python3 spawner.py $start $end &

# Start the verifier process
python3 verifier.py $start $end &

# Wait for all child processes to finish
wait
