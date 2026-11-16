import csv
import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("restaurant-mcp")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCTS_CSV = os.path.join(BASE_DIR, "products.csv")
STOCK_CSV = os.path.join(BASE_DIR, "stock.csv")
TASKS_JSON = os.path.join(BASE_DIR, "tasks.json")

ALTERNATIVE_PRODUCTS = [
    "Chicken Grazelette",
    "Chicken Chad"
]

# SHARED FUNCTIONS

def normalize_name(name):
    return str(name or "").strip().casefold()


def load_products():
    if not os.path.exists(PRODUCTS_CSV):
        return []

    with open(PRODUCTS_CSV, mode="r", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def load_stock():
    if not os.path.exists(STOCK_CSV):
        return None

    with open(STOCK_CSV, mode="r", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def find_stock(product_name, stock_rows):
    if stock_rows is None:
        return None

    target = normalize_name(product_name)

    # Exact match first
    for row in stock_rows:
        name = normalize_name(row.get("product_name"))

        if name == target:
            return row

    # Partial match fallback
    for row in stock_rows:
        name = normalize_name(row.get("product_name"))

        if target and (target in name or name in target):
            return row

    return None


def get_availability(product_name, stock_rows):
    row = find_stock(product_name, stock_rows)

    if row is None:
        return None, "Unknown"

    try:
        quantity = float(row.get("stock_quantity", 0))
    except (ValueError, TypeError):
        return None, "Unknown"

    if quantity <= 0:
        return quantity, "Not Available"

    return quantity, "Available"


def get_alternatives(products, stock_rows):
    alternatives = []

    for alternative_name in ALTERNATIVE_PRODUCTS:

        for product in products:
            name = product.get("name", "")

            if normalize_name(name) == normalize_name(alternative_name):

                quantity, status = get_availability(name, stock_rows)

                if status == "Available":
                    alternatives.append(
                        f"{name} (Stock: {quantity:g})"
                    )

    return alternatives


# TOOL 1: GET PRODUCT

@mcp.tool()
def get_product(product_name: str) -> str:
    """
    Search for a product by English or Arabic name.
    Return the full menu when requested.
    Always verify actual stock before reporting availability.
    """

    try:
        products = load_products()
        stock_rows = load_stock()

    except OSError as error:
        return f"Error reading restaurant data: {error}"

    if not products:
        return "The restaurant menu is empty or products.csv is missing."

    if stock_rows is None:
        return "Cannot verify availability: stock.csv was not found."

    search = normalize_name(product_name)

    all_keywords = [
        "all", "all products", "all items", "everything",
        "full menu", "entire menu", "show menu",
        "list products", "menu",
        "كل المنتجات", "جميع المنتجات", "المنيو",
        "القائمة كاملة"
    ]

    if search in all_keywords:
        results = products
    else:
        results = [
            row for row in products
            if search in normalize_name(row.get("name"))
            or search in normalize_name(row.get("name_ar"))
        ]

    if not results:
        return f"Product '{product_name}' was not found."

    output = []

    for row in results:

        name = row.get("name", "")

        quantity, status = get_availability(name, stock_rows)

        stock_info = (
            f"Stock Quantity: {quantity:g}"
            if quantity is not None
            else "Stock Quantity: Unknown"
        )

        product_info = (
            f"Product: {name}\n"
            f"Arabic Name: {row.get('name_ar')}\n"
            f"Price: {row.get('price_lbp')} {row.get('currency')}\n"
            f"Description: {row.get('description')}\n"
            f"{stock_info}\n"
            f"Availability: {status}"
        )

        if status == "Not Available":

            alternatives = get_alternatives(products, stock_rows)

            if alternatives:
                product_info += (
                    "\nSuggested Alternatives:\n"
                    + "\n".join(alternatives)
                )
            else:
                product_info += "\nNo available alternatives found."

        output.append(product_info)

    return (
        f"SAHTEIN RESTAURANT MENU\n"
        f"Total Products: {len(results)}\n\n"
        + "\n\n".join(output)
    )


# TOOL 2: CHECK STOCK

@mcp.tool()
def check_stock(item_name: str) -> str:
    """Check actual stock quantity and availability."""

    try:
        stock_rows = load_stock()
    except OSError as error:
        return f"Error reading stock: {error}"

    if stock_rows is None:
        return "stock.csv was not found."

    row = find_stock(item_name, stock_rows)

    if row is None:
        return f"'{item_name}' was not found in the stock."

    try:
        quantity = float(row.get("stock_quantity", 0))
    except (ValueError, TypeError):
        return "Invalid stock quantity in stock.csv."

    status = "Available" if quantity > 0 else "Not Available"

    return (
        f"Product: {row.get('product_name')}\n"
        f"Stock Quantity: {quantity:g}\n"
        f"Unit: {row.get('unit')}\n"
        f"Availability: {status}"
    )


# TOOL 3: CREATE TASK

@mcp.tool()
def create_task(task_description: str) -> str:
    """Create a new task and save it to tasks.json."""

    tasks = []

    if os.path.exists(TASKS_JSON):
        try:
            with open(TASKS_JSON, mode="r", encoding="utf-8") as file:
                tasks = json.load(file)

            if not isinstance(tasks, list):
                return "Invalid tasks.json format."

        except (json.JSONDecodeError, OSError):
            return "Could not read tasks.json."

    new_task = {
        "id": max(
            (
                task.get("id", 0)
                for task in tasks
                if isinstance(task, dict)
                and isinstance(task.get("id"), int)
            ),
            default=0
        ) + 1,
        "task": task_description,
        "completed": False
    }

    tasks.append(new_task)

    try:
        with open(TASKS_JSON, mode="w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)

    except OSError as error:
        return f"Could not save task: {error}"

    return f"Task successfully created: {task_description}"


if __name__ == "__main__":
    mcp.run()
