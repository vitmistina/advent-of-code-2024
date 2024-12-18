import os
import time
import subprocess
import sys


def measure_execution_time(script):
    start_time = time.time()
    subprocess.run([sys.executable, script], check=True)
    end_time = time.time()
    return end_time - start_time


def find_scripts(directory):
    scripts = []
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                file.startswith("aoc_")
                and file.endswith(".py")
                and file != os.path.basename(__file__)
            ):
                scripts.append(os.path.join(root, file))
    return scripts


def main():
    scripts = find_scripts(".")
    results = []

    for script in scripts:
        try:
            exec_time = measure_execution_time(script)
            results.append((script, exec_time))
        except subprocess.CalledProcessError as e:
            results.append((script, f"Error: {e}"))

    print("Execution Times:")
    for script, exec_time in results:
        print(f"{script}: {exec_time} seconds")


if __name__ == "__main__":
    main()
