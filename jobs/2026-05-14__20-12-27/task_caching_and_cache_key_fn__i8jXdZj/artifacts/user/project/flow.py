from prefect import task, flow


def cache_key_fn(context, parameters):
    """Cache key function for fetch_data task."""
    return "fetch-" + parameters["url"]


@task(cache_key_fn=cache_key_fn)
def fetch_data(url: str) -> str:
    """Fetch data from the given URL."""
    return "Data from " + url


@flow
def process_data():
    """Process data by fetching from example.com twice."""
    result1 = fetch_data("http://example.com")
    result2 = fetch_data("http://example.com")
    
    print(f"First call result: {result1}")
    print(f"Second call result: {result2}")
    
    return result1, result2


if __name__ == "__main__":
    process_data()