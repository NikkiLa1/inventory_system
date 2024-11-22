import sys
import os

sys.path.append("/Users/psorm/inventory_system")

from Inventory.inventory import Inventory

def test_add_item():
    inventory = Inventory()
    
    ### arguments: item ID, item type, item brand, item price, item quantity, item add date
    inventory.add_item("LAP001", "LAPTOP", "BRANDX", 1200, 5, "2024-10-11")  # Manually assigned Item ID
    assert inventory.get_item("LAP001")['quantity'] == 5

def test_update_price():
    inventory = Inventory()
    inventory.add_item("LAP001", "LAPTOP", "BRANDX", 1200, 5, "2024-10-11")
    
    ### arguments: item ID, item price
    inventory.update_price("LAP001", 1300)
    assert inventory.get_item("LAP001")['price'] == 1300

def test_purchase_item():
    inventory = Inventory()
    inventory.add_item("LAP001", "LAPTOP", "BRANDX", 1200, 5, "2024-10-11")
    ### item ID, purchase quantity, customer name, customer ID
    inventory.purchase_item("LAP001", 2, "John Doe", "john@example.com")  
    assert inventory.get_item("LAP001")['quantity'] == 3

def test_low_stock():
    inventory = Inventory()
    inventory.add_item("LAP001", "LAPTOP", "BRANDX", 1200, 2, "2024-10-11")
    assert inventory.get_item("LAP001")['quantity'] == 2
    assert inventory.get_item("LAP001")['quantity'] < 3  

def test_top_customers():
    inventory = Inventory()
    inventory.add_item("LAP001", "LAPTOP", "BRANDX", 1200, 10, "2024-10-11")
    inventory.purchase_item("LAP001", 5, "John Doe", "john@example.com")  
    inventory.purchase_item("LAP001", 1, "Jane Doe", "jane@example.com")
    top_customers = inventory.customers.get_top_customers("store_data/purchase_history.csv", min_spent=5000)
    assert len(top_customers) == 1
    assert top_customers[0]["name"] == "John Doe"
    assert top_customers[0]["email"] == "john@example.com"
    assert top_customers[0]["total_spent"] == 6000

# test functions
test_add_item()
test_update_price()
test_purchase_item()
test_low_stock()
test_top_customers()
