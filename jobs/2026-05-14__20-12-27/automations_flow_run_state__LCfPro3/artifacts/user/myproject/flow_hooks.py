from prefect import flow


def on_success_hook(flow, flow_run, state):
    """Hook that runs when a flow completes successfully."""
    with open("/home/user/myproject/success.log", "w") as f:
        f.write("Success!")


def on_failure_hook(flow, flow_run, state):
    """Hook that runs when a flow fails."""
    with open("/home/user/myproject/failure.log", "w") as f:
        f.write("Failed!")


@flow(name="successful_flow", on_completion=[on_success_hook])
def successful_flow():
    """A flow that executes without errors."""
    print("Running successful flow...")
    return "Flow completed successfully!"


@flow(name="failing_flow", on_failure=[on_failure_hook])
def failing_flow():
    """A flow that raises a ValueError exception."""
    print("Running failing flow...")
    raise ValueError("This flow is designed to fail!")


if __name__ == "__main__":
    # Run the successful flow
    successful_flow()
    
    # Run the failing flow (catch the exception so the script finishes cleanly)
    try:
        failing_flow()
    except ValueError as e:
        print(f"Caught expected ValueError: {e}")