import os
import sys

from models import Log
from client import store

# Get process id
pid = os.getpid()


def write_log(start, end):
    """Write logs to database"""
    for i in range(start, end):
        log = Log(text=str(i))
        if store(log):
            print(f"Writing log {i} to database from PID {pid}", flush=True)
        else:
            raise RuntimeError(f"Failed to write log {i} to database from PID {pid}")


def main():
    """Entry point"""
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    write_log(start, end)


if __name__ == "__main__":
    main()
