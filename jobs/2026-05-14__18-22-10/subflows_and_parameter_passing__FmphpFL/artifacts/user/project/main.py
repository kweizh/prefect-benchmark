import os
from prefect import flow

@flow(name="process_item")
def process_item(item: str, uppercase: bool) -> str:
    if uppercase:
        return item.upper()
    else:
        return item.lower()

@flow(name="main_flow")
def main_flow(items: list, uppercase: bool) -> list:
    processed_items = []
    for item in items:
        processed_items.append(process_item(item, uppercase))
    return processed_items

if __name__ == "__main__":
    result = main_flow(items=["apple", "Banana", "cherry"], uppercase=True)
    
    os.makedirs("/home/user/project", exist_ok=True)
    with open("/home/user/project/output.log", "w") as f:
        f.write(str(result))
