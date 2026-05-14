from prefect import flow
from prefect.events import DeploymentEventTrigger


@flow(name="webhook-flow")
def webhook_flow(payload: dict = {}):
    """Flow that processes webhook events."""
    print("Received event payload")


if __name__ == "__main__":
    # Serve the flow with event trigger configuration
    webhook_flow.serve(
        name="event-deployment",
        triggers=[
            DeploymentEventTrigger(
                event="custom.webhook.received",
                match={"prefect.resource.id": "my.webhook.resource"},
            )
        ],
    )