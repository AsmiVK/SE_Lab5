"""
Inventory Management System
---------------------------
This program allows adding and removing items from stock,
maintains logs, and displays the inventory using proper logging.
"""

import json
import logging
from datetime import datetime

# Fix #5: Proper logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global stock data
stock_data = {}


# Fix #1, #4, #6: Mutable default argument, input validation, f-strings
def add_item(item="default", qty=0, logs=None):
    """Add an item to stock and update logs."""
    if logs is None:
        logs = []

    # Input validation
    if not isinstance(item, str):
        raise ValueError("Item must be a string.")
    if not isinstance(qty, int) or qty < 0:
        raise ValueError("Quantity must be a non-negative integer.")

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info(f"Added {qty} of '{item}', new quantity: {stock_data[item]}")
    return logs


# Fix #2, #4, #6: Bare except replaced, input validation, f-strings
def remove_item(item, qty):
    """Remove an item from stock."""
    try:
        if not isinstance(item, str):
            raise ValueError("Item must be a string.")
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("Quantity must be a positive integer.")

        if stock_data[item] > qty:
            stock_data[item] -= qty
            logging.info(f"Removed {qty} of '{item}', remaining: {stock_data[item]}")
        else:
            del stock_data[item]
            logging.info(f"Removed '{item}' completely from stock.")

    except KeyError:
        logging.error(f"Item '{item}' not found in stock.")
    except ValueError as e:
        logging.error(str(e))


# Fix #4: Input validation for quantity retrieval
def get_qty(item):
    """Return quantity of the given item."""
    if not isinstance(item, str):
        raise ValueError("Item must be a string.")
    try:
        return stock_data[item]
    except KeyError:
        logging.error(f"Item '{item}' not found in stock.")
        return 0


# Fix #5, #6: Safe file handling + logging
def load_data(file="inventory.json"):
    """Load stock data from a file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
            logging.info(f"Loaded data from {file}")
    except FileNotFoundError:
        logging.warning(f"{file} not found. Starting with empty stock.")
    except json.JSONDecodeError:
        logging.error(f"Failed to parse JSON in {file}. Starting with empty stock.")


# Fix #5, #6: Safe file handling + logging
def save_data(file="inventory.json"):
    """Save stock data to a file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, ensure_ascii=False, indent=4)
            logging.info(f"Saved data to {file}")
    except Exception as e:
        logging.error(f"Failed to save data to {file}: {e}")


# Fix #6: f-strings
def print_data():
    """Print all stock items."""
    logging.info("Items Report:")
    for i in stock_data:
        logging.info(f"{i} -> {stock_data[i]}")


# Fix #4: Input validation for threshold
def check_low_items(threshold=5):
    """Return items with quantity below threshold."""
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("Threshold must be a non-negative integer.")

    result = [i for i in stock_data if stock_data[i] < threshold]
    return result


# Fix #3: Removed unsafe eval, added logging
def main():
    """Main execution loop."""
    load_data()
    add_item("apple", 10)
    add_item("banana", 5)
    try:
        add_item(123, "ten")  # Will raise ValueError now
    except ValueError as e:
        logging.error(f"AddItem error: {e}")

    remove_item("apple", 3)
    remove_item("orange", 1)

    logging.info(f"Apple stock: {get_qty('apple')}")
    logging.info(f"Low items: {check_low_items()}")
    save_data()
    print_data()
    logging.info("Finished inventory operations.")


if __name__ == "__main__":
    main()
