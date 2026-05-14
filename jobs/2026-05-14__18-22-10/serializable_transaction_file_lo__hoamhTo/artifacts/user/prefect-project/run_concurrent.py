import subprocess
import sys
from pathlib import Path

COUNTER_FILE = Path("/home/user/prefect-project/counter.txt")

def main():
    # Reset counter
    with open(COUNTER_FILE, "w") as f:
        f.write("0")
        
    procs = []
    for _ in range(5):
        procs.append(subprocess.Popen([sys.executable, "/home/user/prefect-project/flow.py"]))
        
    for p in procs:
        p.wait()
        
    with open(COUNTER_FILE, "r") as f:
        print("Final counter:", f.read().strip())

if __name__ == "__main__":
    main()
