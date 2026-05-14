import asyncio
from concurrent.futures import ThreadPoolExecutor
from flow import concurrent_file_modifier


async def run_concurrent_flows():
    """
    Execute the concurrent_file_modifier flow 5 times concurrently.
    """
    print("Starting 5 concurrent flow executions...")
    
    # Run the flow 5 times concurrently using ThreadPoolExecutor
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [loop.run_in_executor(executor, concurrent_file_modifier) for _ in range(5)]
        results = await asyncio.gather(*tasks)
    
    print(f"Flow execution results: {results}")
    print(f"Final counter value should be: {len(results)}")


if __name__ == "__main__":
    # Run the concurrent flows
    asyncio.run(run_concurrent_flows())