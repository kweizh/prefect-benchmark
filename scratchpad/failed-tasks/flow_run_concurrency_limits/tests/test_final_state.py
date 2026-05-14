import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/project"
MAIN_PY = os.path.join(PROJECT_DIR, "main.py")

def test_gcl_exists_with_limit_3():
    """Priority 1: Use Prefect CLI to verify the global concurrency limit exists and has limit 3."""
    result = subprocess.run(
        ["prefect", "gcl", "inspect", "db-connections"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, \
        f"'prefect gcl inspect db-connections' failed: {result.stderr}"
    assert "3" in result.stdout, \
        f"Expected limit 3 in 'db-connections' inspection, got: {result.stdout}"

def test_main_py_exists():
    """Priority 3: basic file existence check."""
    assert os.path.isfile(MAIN_PY), \
        f"main.py not found at {MAIN_PY}"

def test_main_py_executes_successfully():
    """Priority 1: Use python to run the script and verify it exits with 0."""
    result = subprocess.run(
        ["python3", "main.py"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, \
        f"'python main.py' failed: {result.stderr}\nStdout: {result.stdout}"

def test_main_py_contains_concurrency_context_manager():
    """Priority 3: basic file content check."""
    with open(MAIN_PY, "r") as f:
        content = f.read()
    assert "concurrency(" in content or "concurrency (" in content, \
        "Expected 'concurrency' context manager usage in main.py"
    assert "db-connections" in content, \
        "Expected 'db-connections' to be used in main.py"

def test_amika_validation():
    """Priority 1: Use amika cli to validate the final state."""
    result = subprocess.run(
        ["amika", "validate", "--target", "prefect-gcl"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, \
        f"'amika validate' failed: {result.stderr}\nStdout: {result.stdout}"
