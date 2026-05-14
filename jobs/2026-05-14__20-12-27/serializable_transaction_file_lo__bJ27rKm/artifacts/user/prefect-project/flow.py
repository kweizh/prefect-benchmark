from prefect import flow, task
from prefect.transactions import transaction, ResultStore
from prefect.locking.filesystem import FileSystemLockManager
from pathlib import Path
import os

# Define the lock manager
lock_manager = FileSystemLockManager(
    lock_files_directory=Path("/home/user/prefect-project/locks")
)

# Create a result store with the lock manager
result_store = ResultStore(lock_manager=lock_manager)

# Define the data file path
DATA_FILE = "/home/user/prefect-project/counter.txt"


@task
def read_counter() -> int:
    """Read the current counter value from the file."""
    if not os.path.exists(DATA_FILE):
        return 0
    
    with open(DATA_FILE, 'r') as f:
        content = f.read().strip()
        if content:
            return int(content)
        return 0


@task
def write_counter(value: int) -> None:
    """Write the counter value to the file."""
    with open(DATA_FILE, 'w') as f:
        f.write(str(value))


@flow(name="concurrent_file_modifier")
def concurrent_file_modifier():
    """
    A flow that reads, increments, and writes a counter value.
    Uses a SERIALIZABLE transaction with FileSystemLockManager to prevent race conditions.
    """
    with transaction(
        key="counter_lock",
        isolation_level="SERIALIZABLE",
        store=result_store
    ):
        # Read the current counter value
        current_value = read_counter()
        
        # Increment the counter
        new_value = current_value + 1
        
        # Write the new counter value
        write_counter(new_value)
        
        return new_value