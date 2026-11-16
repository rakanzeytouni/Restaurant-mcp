import csv
import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("restaurant-mcp")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCTS_CSV = os.path.join(BASE_DIR, "products.csv")
STOCK_CSV = os.path.join(BASE_DIR, "stock.csv")
TASKS_JSON = os.path.join(BASE_DIR, "tasks.json")




# TOOL 1: Get Product
@mcp.tool()
def get_product(product_name: str) -> str:
    """
    Search for one product by English or Arabic name.
    If the user requests all products or the full menu,
    return the complete restaurant menu.
    """

    if not os.path.exists(PRODUCTS_CSV):
        return "products.csv was not found."

    with open(PRODUCTS_CSV, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        return "The restaurant menu is empty."

    search = product_name.strip().lower()

    all_keywords = [
        "all",
        "all products",
        "all items",
        "everything",
        "full menu",
        "entire menu",
        "show menu",
        "list products",
        "menu",
        "كل المنتجات",
        "جميع المنتجات",
        "المنيو",
        "القائمة كاملة"
    ]

    if search in all_keywords:
        results = rows
    else:
        results = [
            row for row in rows
            if search in row.get("name", "").lower()
            or product_name.strip() in row.get("name_ar", "")
        ]

    if not results:
        return f"Product '{product_name}' was not found."

    output = []

    for row in results:
        output.append(
            f"Product: {row.get('name')}\n"
            f"Arabic Name: {row.get('name_ar')}\n"
            f"Price: {row.get('price_lbp')} {row.get('currency')}\n"
            f"Description: {row.get('description')}\n"
            f"Available: {row.get('available')}"
        )

    return (
        f"SAHTEIN RESTAURANT MENU\n"
        f"Total Products: {len(results)}\n\n"
        + "\n\n".join(output)
    )



# TOOL 2: Check Stock
@mcp.tool()
def check_stock(item_name: str) -> str:
    """Check the available quantity of a restaurant product."""

    if not os.path.exists(STOCK_CSV):
        return "stock.csv was not found."

    with open(STOCK_CSV, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row.get("product_name", "")

            if item_name.lower() in name.lower():
                return (
                    f"Product: {name}\n"
                    f"Stock Quantity: {row.get('stock_quantity')}\n"
                    f"Unit: {row.get('unit')}"
                )

    return f"'{item_name}' was not found in the stock."


# TOOL 3: Create Task
@mcp.tool()
def create_task(task_description: str) -> str:
    """Create a new task for the restaurant owner and save it to tasks.json."""

    tasks = []

    if os.path.exists(TASKS_JSON):
        try:
            with open(TASKS_JSON, mode="r", encoding="utf-8") as file:
                tasks = json.load(file)

            if not isinstance(tasks, list):
                tasks = []

        except (json.JSONDecodeError, OSError):
            tasks = []

    new_task = {
        "id": max(
            (task.get("id", 0) for task in tasks
             if isinstance(task, dict)
             and isinstance(task.get("id"), int)),
            default=0
        ) + 1,
        "task": task_description,
        "completed": False
    }

    tasks.append(new_task)

    with open(TASKS_JSON, mode="w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

    return f"Task successfully created: {task_description}"


if __name__ == "__main__":
    mcp.run()
