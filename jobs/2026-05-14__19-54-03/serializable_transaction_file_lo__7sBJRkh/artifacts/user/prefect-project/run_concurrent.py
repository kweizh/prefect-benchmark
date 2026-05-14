"""
run_concurrent.py

Launches 5 concurrent instances of the `concurrent_file_modifier` flow to
demonstrate that the SERIALIZABLE FileSystemLockManager transaction prevents
lost updates.

Expected result: counter.txt contains 5 after all runs complete.
"""

import asyncio
import sys


async def run_flow_subprocess(run_id: int) -> int:
    """Spawn a separate Python process for each flow run."""
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-c",
        "from flow import concurrent_file_modifier; concurrent_file_modifier()",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd="/home/user/prefect-project",
    )
    stdout, stderr = await proc.communicate()

    if stdout:
        print(f"[run {run_id}] stdout: {stdout.decode().strip()}")
    if stderr:
        print(f"[run {run_id}] stderr: {stderr.decode().strip()}")
    if proc.returncode != 0:
        print(f"[run {run_id}] FAILED with return code {proc.returncode}")
    else:
        print(f"[run {run_id}] completed successfully")

    return proc.returncode


async def main() -> None:
    num_runs = 5
    print(f"Launching {num_runs} concurrent flow runs...\n")

    tasks = [run_flow_subprocess(i + 1) for i in range(num_runs)]
    return_codes = await asyncio.gather(*tasks)

    failures = sum(1 for rc in return_codes if rc != 0)

    print(f"\nAll {num_runs} runs finished. Failures: {failures}")

    with open("/home/user/prefect-project/counter.txt") as f:
        final_value = int(f.read().strip())

    print(f"Final counter value: {final_value}")

    if final_value == num_runs and failures == 0:
        print("SUCCESS: counter matches the number of concurrent runs — no updates were lost.")
    else:
        print("FAILURE: counter value does not match expected result.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
