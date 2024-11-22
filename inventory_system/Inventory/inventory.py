import csv
import os
from collections import defaultdict
from datetime import datetime

# class to manage items in stock
class Inventory:
    def __init__(self, low_stock_min=3):
        self.items = {}
        self.customers = Customer_Management() # customer management instance / class
        self.purchases = Purchasing() # purchase instance / class
        self.low_stock_min = low_stock_min # getting the threshold for low stocks

    # error: cannot access local variable 'purchase_date' where it is not associated with a value
    # asked chatgpt for help with date variable in code
    def add_item(self, item_id, name, brand, price, quantity, date):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d") # current date
        self.items[item_id] = {"itemName": name, "itemBrand": brand,
                               "price": price, "quantity": quantity,
                               "date": date}

    def update_price(self, item_id, new_price):
        # updates price of existing item
        # returns success or none if item is non-existent
        if item_id in self.items:
            self.items[item_id]["price"] = new_price
            return "Price updated."
        return None

    def purchase_item(self, item_id, quantity, customer_name, customer_email):
        # aids purchase, updates quantity, and records the purchase
        if item_id not in self.items:
            raise ValueError("Item not found.")
        item = self.items[item_id]
        if item["quantity"] < quantity:
            # error if item low stocked or not found
            raise ValueError("Low stock.")
        # updates quantity stock
        item["quantity"] -= quantity

        # saves the purchase to the customer
        customer_id = self.customers.assign_customer_id(customer_name, customer_email)
        purchase_date = datetime.now().strftime("%Y-%m-%d")
        self.purchases.save_purchase(item_id, item["itemName"], customer_name, customer_email,
                                     item["price"] * quantity, purchase_date)

    # TypeError: string indices must be integers, not 'str' - asked perplexity.ai what to do
    # told me to create a copy of the item dict
    def get_item(self, item_id):
        # gets item details with a low stock warning
        item = self.items.get(item_id)
        if not item:
            return None # item has not been found
        item_copy = item.copy()
        if item["quantity"] < self.low_stock_min:
            item_copy["low_stock"] = True
            item_copy["low_stock_message"] = f"LOW STOCKED, {item['quantity']} remaining."
        else:
            item_copy["low_stock"] = False
        return item_copy


# bonus in attempt to make it more robust with separate class instead of 1 inventory class
# manages customers info with their IDs with class
class Customer_Management:
    def __init__(self):
        self.customers = {} # customer emails maping
        self.customer_count = 0 

    # assigns id to a customer
    # if email already in system, pulls it up
    def assign_customer_id(self, name, customer_email):
        if customer_email not in self.customers:
            self.customer_count += 1
            self.customers[customer_email] = {"id": self.customer_count, "name": name}
        return self.customers[customer_email]["id"]

    # gets customer name 
    def get_customer_name(self, email):
        return self.customers.get(email, {}).get("name")

    # chatgpt help here with reading in csv files
    def get_top_customers(self, file_path="store_data/purchase_history.csv", min_spent=5000):

        customer_spending = {}
        with open(file_path, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row["customer_email"]
                amount = float(row["amount"])
            
                # if customer is not in the dictionary - add them
                if email not in customer_spending:
                    customer_spending[email] = 0
            
                # add purchase amount to the customer's total spending
                customer_spending[email] += amount

        # list of top customers who spent more than $5000
        top_customers = []
        for email, spent in customer_spending.items():
            if spent >= min_spent:
                top_customers.append({
                    "email": email,
                    "name": self.get_customer_name(email),
                    "total_spent": spent
                })
        return top_customers
        
# bonus in attempt to make it more robust with separate class
# asked perplexity.ai about properly connecting csv to package and classes
# also got help on how to read them, since I had file_path issues
class Purchasing:
    def __init__(self, file_path="store_data/purchase_history.csv"):
        self.file_path = file_path
        self._ensure_file_exists()

    # chatgpt help with making sure the csv file exists correctly
    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow(["item_id", "item_name", "customer_name", 
                                 "customer_email", "amount", "purchase_date"])

    # makes sure to save purchases in csv
    def save_purchase(self, item_id, item_name, customer_name, customer_email, amount, purchase_date):        
        with open(self.file_path, "a", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow([item_id, item_name, customer_name, customer_email, amount, purchase_date])