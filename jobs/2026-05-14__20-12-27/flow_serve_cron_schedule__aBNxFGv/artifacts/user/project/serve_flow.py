from prefect import flow, serve
from prefect.blocks.system import Secret


@flow(name="my_flow")
def my_flow():
    """Flow that loads and prints the API key secret."""
    api_key_secret = Secret.load("my-api-key")
    api_key_value = api_key_secret.get()
    print(f"API Key: {api_key_value}")
    return api_key_value


if __name__ == "__main__":
    # Serve the flow with deployment name and cron schedule
    # Cron schedule "0 9 * * *" means: At 09:00 AM every day
    serve(
        my_flow.to_deployment(
            name="my-deployment",
            cron="0 9 * * *"
        )
    )