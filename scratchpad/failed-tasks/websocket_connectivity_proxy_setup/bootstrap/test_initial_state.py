import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/prefect-proxy"
NGINX_CONF = "/etc/nginx/sites-available/default"

def test_prefect_binary_available():
    assert shutil.which("prefect") is not None, "prefect binary not found in PATH."

def test_nginx_binary_available():
    assert shutil.which("nginx") is not None, "nginx binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_nginx_config_exists():
    assert os.path.isfile(NGINX_CONF), f"Nginx config {NGINX_CONF} does not exist."

def test_flow_script_exists():
    flow_path = os.path.join(PROJECT_DIR, "flow.py")
    assert os.path.isfile(flow_path), f"Flow script {flow_path} does not exist."

def test_nginx_is_running():
    result = subprocess.run(["service", "nginx", "status"], capture_output=True, text=True)
    assert result.returncode == 0, f"Nginx is not running: {result.stdout} {result.stderr}"

def test_prefect_server_is_running():
    # Prefect server typically listens on 4200
    result = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:4200/api/health"], capture_output=True, text=True)
    assert result.stdout == "200", f"Prefect server is not healthy or not running on port 4200. Got HTTP {result.stdout}"
