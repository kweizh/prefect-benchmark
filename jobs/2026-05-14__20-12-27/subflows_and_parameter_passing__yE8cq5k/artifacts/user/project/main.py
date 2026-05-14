from prefect import flow
import logging

# Configure logging to write to a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/user/project/output.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@flow(name="process_item")
def process_item(item: str, uppercase: bool) -> str:
    """
    Subflow that processes a single item.
    
    Args:
        item: The string item to process
        uppercase: If True, returns uppercase; otherwise returns lowercase
    
    Returns:
        The processed string
    """
    if uppercase:
        return item.upper()
    else:
        return item.lower()


@flow(name="main_flow")
def main_flow(items: list[str], uppercase: bool) -> list[str]:
    """
    Parent flow that processes a list of items by calling the process_item subflow.
    
    Args:
        items: List of strings to process
        uppercase: Flag to determine if items should be uppercased or lowercased
    
    Returns:
        List of processed strings
    """
    processed_items = []
    
    for item in items:
        processed_item = process_item(item=item, uppercase=uppercase)
        processed_items.append(processed_item)
    
    return processed_items


if __name__ == "__main__":
    # Execute the main flow with the specified arguments
    result = main_flow(items=["apple", "Banana", "cherry"], uppercase=True)
    
    # Log the result
    logger.info(f"Processed items: {result}")
    
    # Also write the result directly to the output log file
    with open('/home/user/project/output.log', 'a') as f:
        f.write(f"Processed items: {result}\n")