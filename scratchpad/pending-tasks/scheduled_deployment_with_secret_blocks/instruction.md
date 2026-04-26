Long-running local processes often need access to managed configurations, secrets, and scheduled execution parameters without relying on complex external infrastructure.

You need to create a deployment script that schedules a flow to run every day at midnight and loads sensitive credentials securely in a local Python environment. 

**Constraints:**
- Use `flow.serve()` to create the deployment; do NOT use `flow.deploy()`.
- The deployment must be scheduled using a Cron string (`"0 0 * * *"`).
- The flow must load an API key at runtime using a Prefect `Secret` block named "my-api-key".