import logging
import sys
from prefect import flow

# ---------------------------------------------------------------------------
# Logging – write to both the output log file and to stdout so Prefect's
# console output is preserved alongside the file-based log.
# ---------------------------------------------------------------------------
LOG_FILE = "/home/user/project/output.log"

_file_handler = logging.FileHandler(LOG_FILE, mode="a")
_file_handler.setLevel(logging.INFO)
_file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

_stream_handler = logging.StreamHandler(sys.stdout)
_stream_handler.setLevel(logging.INFO)
_stream_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(_file_handler)
logger.addHandler(_stream_handler)


# ---------------------------------------------------------------------------
# Subflow
# ---------------------------------------------------------------------------

@flow(name="process_item")
def process_item(item: str, uppercase: bool) -> str:
    """
    Subflow that processes a single string item.

    Args:
        item:      The string to process.
        uppercase: If True, return the item uppercased; otherwise lowercased.

    Returns:
        The processed string.
    """
    result = item.upper() if uppercase else item.lower()
    logger.info("process_item: '%s' -> '%s' (uppercase=%s)", item, result, uppercase)
    return result


# ---------------------------------------------------------------------------
# Parent flow
# ---------------------------------------------------------------------------

@flow(name="main_flow")
def main_flow(items: list[str], uppercase: bool) -> list[str]:
    """
    Parent flow that iterates over a list of strings and delegates
    processing of each item to the process_item subflow.

    Args:
        items:     List of strings to process.
        uppercase: Flag passed through to each process_item subflow call.

    Returns:
        List of processed strings in the same order as the input.
    """
    processed = [process_item(item=item, uppercase=uppercase) for item in items]
    logger.info("main_flow result: %s", processed)
    return processed


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    result = main_flow(items=["apple", "Banana", "cherry"], uppercase=True)
    # Flush the file handler so every byte reaches disk before the process exits.
    _file_handler.flush()
    logger.info("Final output written to %s", LOG_FILE)
    # Write the final result line directly to the log file so it is always
    # present even if the logging infrastructure is flushed asynchronously.
    with open(LOG_FILE, "a") as fh:
        fh.write(f"Result: {result}\n")
    print(result)
