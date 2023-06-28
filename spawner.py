import concurrent.futures
import os
import sys


def run_program(range_values):
    """system call"""
    start, end = range_values
    os.system(f"python log_generator.py {start} {end}")


def spawn_program(start, end):
    """Spawn processes"""
    n_processes = 20

    range_values = [
        (start + (i * (end - start) // n_processes), start + ((i + 1) * (end - start) // n_processes))
        for i in range(n_processes)
    ]

    # Use a ProcessPoolExecutor to run the processes in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_processes) as executor:
        executor.map(run_program, range_values)


def main():
    """Entry point"""
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    spawn_program(start, end)


if __name__ == "__main__":
    main()
