from prefect import flow


def notify_success(flow, flow_run, state):
    """Hook function to write success notification to log file."""
    with open("/home/user/project/success.log", "w") as f:
        f.write("Workflow succeeded")


def notify_failure(flow, flow_run, state):
    """Hook function to write failure notification to log file."""
    with open("/home/user/project/failure.log", "w") as f:
        f.write("Workflow failed")


@flow(name="data_pipeline", on_completion=[notify_success], on_failure=[notify_failure])
def data_pipeline(should_fail: bool):
    """A data pipeline flow that can succeed or fail based on parameter."""
    if should_fail:
        raise ValueError("Simulated failure")
    return "Success"


if __name__ == "__main__":
    # Run the flow twice: one success, one failure
    data_pipeline(should_fail=False, return_state=True)
    data_pipeline(should_fail=True, return_state=True)