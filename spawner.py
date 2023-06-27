import concurrent.futures
import os

def run_program(range_values):
    start, end = range_values
    os.system(f"python log_generator.py {start} {end}")

def spawn_program(start, end):
    # Create a list of range values
    range_values = [(start + (i * (end-start) // 10), start + ((i+1) * (end-start) // 10)) for i in range(10)]
    
    # Use a ProcessPoolExecutor to run the processes in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(run_program, range_values)

if __name__ == "__main__":
    spawn_program(1, 5000)
