from prefect import task, flow
from prefect.cache_policies import NONE


def cache_key_fn(context, parameters):
    return "fetch-" + parameters["url"]


@task(cache_key_fn=cache_key_fn)
def fetch_data(url: str) -> str:
    return "Data from " + url


@flow
def process_data():
    result1 = fetch_data("http://example.com")
    result2 = fetch_data("http://example.com")
    print(result1)
    print(result2)


if __name__ == "__main__":
    process_data()
