import sys
from pathlib import Path
from prefect import flow, task
from prefect.transactions import transaction, IsolationLevel
from prefect.locking.filesystem import FileSystemLockManager
from prefect.results import ResultStore

LOCK_DIR = Path("/home/user/prefect-project/locks")
COUNTER_FILE = Path("/home/user/prefect-project/counter.txt")

lock_manager = FileSystemLockManager(lock_files_directory=LOCK_DIR)
store = ResultStore(lock_manager=lock_manager)

@task
def increment_counter():
    with open(COUNTER_FILE, "r") as f:
        val = int(f.read().strip())
    
    val += 1
    
    with open(COUNTER_FILE, "w") as f:
        f.write(str(val))
    return val

@flow
def concurrent_file_modifier():
    with transaction(key="counter_tx", isolation_level=IsolationLevel.SERIALIZABLE, store=store):
        increment_counter()

if __name__ == "__main__":
    concurrent_file_modifier()
