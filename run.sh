#!/bin/bash

# Remove log_database.sqlite3 if it exists
if [ -f log_database.sqlite3 ]; then
    rm log_database.sqlite3
fi

python3 flusher.py &

FLUSHED_PID=$!

# Block until 10000 accepts TCP connections
echo -n "Waiting for port 10000 to be open"
while ! nc -z -w1 localhost 10000
do
    echo -n .
    sleep 0.1
done

START=1
END=1000

# Spawn 10 processes for log generation
python3 spawner.py $START $END &

# Start the verifier process
python3 verifier.py $START $END

# Send interrupt signal to flusher process
kill -SIGINT $FLUSHED_PID

# Wait for all child processes to finish (flusher and spawner)
wait