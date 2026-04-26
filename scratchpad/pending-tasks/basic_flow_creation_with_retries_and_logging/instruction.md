Converting raw Python scripts to Prefect flows is the foundational step in functional data engineering orchestration.

You need to convert a provided three-step Python script (extract, transform, load) into a Prefect 3.0 flow in a local Python environment. 

**Constraints:**
- Use the `@task` decorator for the individual functional steps and `@flow` for the main execution function.
- Enable logging of print statements by setting `log_prints=True` on the main flow.
- Configure the `extract` task to automatically retry upon failure by setting exactly 2 retries using the `retries` parameter.