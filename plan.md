### 1. Library Overview
*   **Description**: Prefect is a high-performance workflow orchestration tool designed for "functional" data engineering. It allows developers to transform any Python function into a unit of work that can be scheduled, monitored, and retried. Prefect 3.0 (the current major version) emphasizes event-driven automation, transactional semantics, and a highly decoupled hybrid execution model.
*   **Ecosystem Role**: It sits between raw Python scripts and complex infrastructure, acting as the control plane for data pipelines, ML workflows, and background jobs. It competes with Airflow and Dagster but focuses on a "code-as-workflows" approach with minimal boilerplate.
*   **Project Setup**:
    1.  **Install**: `pip install prefect` (or `uv add prefect`).
    2.  **Initialize**: `prefect init` to create a `prefect.yaml` configuration file.
    3.  **Local Server**: `prefect server start` to run the UI and API locally.
    4.  **Authentication**: `prefect cloud login` (if using Prefect Cloud).
    5.  **Environment**: Set `PREFECT_API_URL` and `PREFECT_API_KEY` for remote communication.
### 2. Core Primitives & APIs
*   **@flow**: The entry point of a workflow. It manages state, context, and execution strategy.
    ```python
    from prefect import flow
    @flow(log_prints=True, retries=2)
    def my_workflow(name: str):
        print(f"Hello {name}")
    ```
    [Flows Documentation](https://docs.prefect.io/v3/concepts/flows)
*   **@task**: The basic unit of work. Tasks can be retried, cached, and executed concurrently.
    ```python
    from prefect import task
    @task(cache_key_fn=lambda *args: "fixed_key")
    def compute_data():
        return 42
    ```
    [Tasks Documentation](https://docs.prefect.io/v3/concepts/tasks)
*   **Transactions**: A new 3.0 feature for atomic units of work with rollback hooks.
    ```python
    from prefect.transactions import transaction
    with transaction():
        do_something()
        # if failure occurs here, on_rollback hooks in do_something() trigger
    ```
    [Transactions Documentation](https://docs.prefect.io/v3/develop/transactions)
*   **Blocks & Variables**: Managed configuration and secrets.
    ```python
    from prefect.blocks.system import Secret
    secret_block = Secret.load("my-api-key")
    ```
    [Blocks Documentation](https://docs.prefect.io/v3/concepts/blocks)
*   **Deployments**: Server-side representations of flows.
    *   `flow.serve()`: For long-running local processes.
    *   `flow.deploy()`: For managed infrastructure (Docker, K8s).
### 3. Real-World Use Cases & Templates
*   **Event-Driven ETL**: Using **Triggers** to start a flow when a file arrives in S3 or a webhook is received.
*   **ML Pipelines**: Using **Work Pools** to spin up GPU-backed Kubernetes pods for training and then scaling to zero.
*   **Transactional Side Effects**: Managing database writes and file uploads where a failure in step B must roll back the changes in step A.
*   **Template Repository**: [Prefect Quickstart Repo](https://github.com/PrefectHQ/quickstart) contains examples for local processes, Docker, and GitHub integration.
### 4. Developer Friction Points
*   **WebSocket Connectivity**: Prefect 3.0 uses WebSockets for real-time task updates. In environments with strict proxies or old load balancers, task runs might "hang" in the UI even if the code executes successfully. [Issue #15274](https://github.com/PrefectHQ/prefect/issues/15274).
*   **Async/Sync Mixing**: Users often struggle with calling async tasks from sync flows or vice versa, leading to `RuntimeError: This event loop is already running`.
*   **Deployment Entrypoints**: Configuring `prefect.yaml` entrypoints (e.g., `path/to/file.py:flow_name`) often fails if the `path` or `PYTHONPATH` is not perfectly aligned with the worker's working directory.
### 5. Evaluation Ideas
*   **Simple**: Convert a multi-step Python script into a Prefect flow with retries and logging.
*   **Simple**: Create a flow that uses `.map()` to process a list of items in parallel.
*   **Moderate**: Set up a deployment using `flow.serve()` that includes a Cron schedule and a secret Block for an API key.
*   **Moderate**: Implement a transactional flow with an `on_rollback` hook that deletes a temporary file if a downstream quality check fails.
*   **Complex**: Configure an event-driven deployment in `prefect.yaml` that triggers only when a specific "External Event" is received.
*   **Complex**: Write a flow that uses a `SERIALIZABLE` transaction with a `FileSystemLockManager` to prevent race conditions between concurrent runs.
*   **Complex**: Debug a deployment where the worker cannot find the flow entrypoint due to a misconfigured `pull_step` in `prefect.yaml`.
### 6. Sources
1.  [Prefect 3.0 Documentation](https://docs.prefect.io/v3/): Official guide for all core concepts.
2.  [Prefect GitHub Repository](https://github.com/PrefectHQ/prefect): Source of truth for issues, release notes, and latest features.
3.  [Prefect Transactions Guide](https://docs.prefect.io/v3/develop/transactions.md): Detailed explanation of the new transactional semantics.
4.  [Prefect Deployment Triggers](https://docs.prefect.io/v3/how-to-guides/automations/creating-deployment-triggers.md): Documentation on event-driven orchestration.
5.  [Prefect Quickstart](https://docs.prefect.io/v3/get-started/quickstart.md): Instructions for initial setup and first runs.