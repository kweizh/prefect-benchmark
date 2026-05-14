FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages --ignore-installed prefect websockets

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Prefect environment with Nginx proxy stripping WebSocket headers."

RUN mkdir -p /home/user/prefect-proxy && \
    cd /home/user/prefect-proxy && \
    cat >flow.py <<'EOF'
import asyncio
from prefect import flow, task

@task
def my_task():
    return "Task completed"

@flow(log_prints=True)
def my_flow():
    print("Flow started")
    result = my_task()
    print(result)
    return result

if __name__ == "__main__":
    my_flow()
EOF

RUN cat >/etc/nginx/sites-available/default <<'EOF'
server {
    listen 8080;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:4200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        # Missing WebSocket headers intentionally
    }
}
EOF

# Container contents:
#   - prefect installed
#   - nginx installed and configured without WebSocket support
#   - /home/user/prefect-proxy: project directory with flow.py

ENV PREFECT_API_URL="http://127.0.0.1:8080/api"

CMD ["/bin/bash", "-c", "service nginx start && prefect server start --host 127.0.0.1 --port 4200 & sleep 10 && trap : TERM INT; sleep infinity & wait"]
