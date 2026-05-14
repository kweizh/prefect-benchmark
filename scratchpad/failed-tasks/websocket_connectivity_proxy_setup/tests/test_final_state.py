import os
import subprocess
import pytest
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/prefect-proxy"
NGINX_CONF = "/etc/nginx/sites-available/default"
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")

def test_nginx_config_has_websocket_headers():
    """Priority 3: Check that the Nginx config file has the required WebSocket upgrade headers."""
    with open(NGINX_CONF, "r") as f:
        content = f.read()
    
    assert "proxy_set_header Upgrade" in content, "Nginx config is missing 'proxy_set_header Upgrade'."
    assert "proxy_set_header Connection" in content, "Nginx config is missing 'proxy_set_header Connection'."
    assert "$http_upgrade" in content or '"upgrade"' in content.lower(), "Nginx config does not properly set the upgrade values."

def test_websocket_upgrade_accepted():
    """Priority 3: Test that Nginx actually accepts the WebSocket upgrade request."""
    # We use a simple curl command to simulate a websocket upgrade request
    result = subprocess.run(
        [
            "curl", "-i", "-N",
            "-H", "Connection: Upgrade",
            "-H", "Upgrade: websocket",
            "-H", "Host: 127.0.0.1:8080",
            "-H", "Origin: http://127.0.0.1:8080",
            "-H", "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==",
            "-H", "Sec-WebSocket-Version: 13",
            "http://127.0.0.1:8080/api/events/in"
        ],
        capture_output=True, text=True
    )
    
    assert "HTTP/1.1 101 Switching Protocols" in result.stdout, \
        f"Expected Nginx to return HTTP 101 Switching Protocols for WebSocket upgrade, but got: {result.stdout}"

def test_flow_output_log_exists():
    """Priority 3: Check that the flow ran and created the output log."""
    assert os.path.isfile(LOG_FILE), f"Flow output log not found at {LOG_FILE}. Did you run the flow and redirect output?"

def test_flow_completed_successfully():
    """Priority 3: Check the flow output log for successful completion."""
    with open(LOG_FILE, "r") as f:
        content = f.read()
    
    assert "Flow started" in content, "Log does not indicate the flow started."
    assert "Task completed" in content, "Log does not indicate the task completed."
    # Prefect usually logs state changes, so we can also check for a successful state or lack of errors
    assert "Traceback" not in content, "Log contains a traceback indicating an error during execution."
