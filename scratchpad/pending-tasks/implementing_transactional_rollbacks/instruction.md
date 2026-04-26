Prefect 3.0 introduces transactional semantics to ensure that side effects are properly reverted when a downstream failure occurs in an atomic unit of work.

You need to implement a Prefect flow containing a `with transaction():` block that writes a local file, simulates a downstream failure, and rolls back the file creation. 

**Constraints:**
- Inside the transaction block, create a file named `temp_data.txt`, and immediately following it, raise a `ValueError` to simulate failure.
- You must define and register an `on_rollback` hook that deletes `temp_data.txt` when the transaction fails.
- The `temp_data.txt` file must not exist on the filesystem after the flow completes its run.