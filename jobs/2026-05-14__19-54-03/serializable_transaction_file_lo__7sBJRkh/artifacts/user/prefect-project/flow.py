from pathlib import Path

from prefect import flow, task
from prefect.transactions import transaction, IsolationLevel
from prefect.locking.filesystem import FileSystemLockManager
from prefect.results import ResultStore

LOCK_DIR = Path("/home/user/prefect-project/locks")
COUNTER_FILE = Path("/home/user/prefect-project/counter.txt")


@task
def read_counter() -> int:
    """Read the current integer value from the counter file."""
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())


@task
def write_counter(value: int) -> None:
    """Write an integer value to the counter file."""
    with open(COUNTER_FILE, "w") as f:
        f.write(str(value) + "\n")


@flow(name="concurrent_file_modifier")
def concurrent_file_modifier() -> None:
    """
    Read the counter, increment it by 1, and write it back — protected by a
    SERIALIZABLE transaction backed by a FileSystemLockManager so that
    concurrent runs cannot interleave their read-modify-write cycles.
    """
    lock_manager = FileSystemLockManager(lock_files_directory=LOCK_DIR)
    store = ResultStore(lock_manager=lock_manager)

    with transaction(
        isolation_level=IsolationLevel.SERIALIZABLE,
        store=store,
        key="counter-file-lock",
    ):
        current = read_counter()
        write_counter(current + 1)


if __name__ == "__main__":
    concurrent_file_modifier()
