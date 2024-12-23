import json
from pprint import pprint
import os
class GroceryList:
    """A class that represents a grocery list of items"""

    def __init__(self):
        """Initialize items dictionary"""
        self.db_path = "database.json"


    def add_item(self, item, category):
        """Add an item to the grocery list"""

        # create database file if the file doesn't exist or is empty 
        if os.path.getsize(self.db_path) == 0 or not os.path.exists(self.db_path): 
            with open(self.db_path, "w", encoding="utf-8") as db:
                data = {category: {item.item_name: item.item_info}}
                json.dump(data, db, indent=4) 
                return

        # Load the grocery list into memory   
        data = self.get_items() 
        
        # Create a dictionary if the category doesn't exist
        if category not in data: 
            data[category] = {}
        
        data[category][item.item_name] = item.item_info 

        with open(self.db_path, "w", encoding="utf-8") as db:
            json.dump(data, db, indent=4) 
        
        


    def update_item(self, item, category):
        """Update an existing item in the grocery list"""
        self.items[category].update({item.item_name: item.item_info})


    def remove_item(self, item_name, category):
        """Remove an item from the grocery list"""
        del self.items[category][item_name]


    def get_items(self):
        """View all items in the cart"""
        with open("database.json", "r", encoding="utf-8") as db:
            data = json.load(db)
            return data


class GroceryItem(GroceryList):
    """A subclass of GroceryList that represents a grocery item"""

    error_message = "Must be a valid number between 1 and 5"

    def __init__(self, item_name, item_info=None):
        super().__init__()

        self.item_name = item_name
        self.item_info = item_info if item_info else "" 
        self.categories = ["produce", "dairy", "snacks", "frozen", "other"]
    

    def add_category(self):
        """Adds a food item to a category"""

        print("Choose which category this item belongs to\n")
        for idx, category in enumerate(self.categories, start=1):
            print(f"{[idx]} {category}")

        while True:
            try:
                category_id = int(input(">>> "))
                if 0 < category_id < 6: # must be a number between 1-5
                    break
                else:
                    print(GroceryItem.error_message)
            except ValueError:          # if user doesn't type an int value
                print(GroceryItem.error_message)
    
        return self.categories[category_id - 1]

        
    def __str__(self):
        return f"{self.item_name}\n{self.item_info}"


def add_to_cart(cart):
    """Adds a grocery item to the cart"""
    item_name = input("Item name:\n>>> ")
    item_info = input("Add a note (optional):\n>>> ")

    cart_item = GroceryItem(item_name, item_info)
    item_category = cart_item.add_category()

    cart.add_item(cart_item, item_category)


def update_to_cart(cart):
    """Update existing item in the cart"""
    print("\nChoose an item you would like to update:")
    cart_items = cart.get_items()
    print(cart_items)

    item_name = input(">>> ").strip()
    
    # Find the item and save the category
    for category in cart_items:
        if item_name in cart_items[category]:
            item_info = input("Add a note (optional):\n>>> ")
            grocery_item = GroceryItem(item_name, item_info)
            cart.update_item(grocery_item, category)
            break
    
    print(f"{item_name} not in your cart")


def remove_from_cart(cart):
    """Remove an item from the cart"""
    print("\nChoose which item you would like to remove from your cart:")
    cart_items = cart.get_items()

    item_name = input(">>> ").strip()

    # Find the item and save the category
    for category in cart_items:
        if item_name in cart_items[category]:
            cart.remove_item(item_name, category)
            return
    
    print(f"{item_name} not in your cart")


def view_cart(cart):
    """View all items in the cart"""
    items = cart.get_items()
    pprint(items, indent=4)


def main():
    """Starting point for the grocery list program"""

    print("Welcome to Quick Cart!")
    print("What would you like to do?")

    cart = GroceryList()

    cart_options = {
        1: "Add item to cart",
        2: "Update item in cart",
        3: "Remove item in cart",
        4: "View cart",
        5: "Exit program"
    }
    
    while True:
        try:
            print("\n")
            for key, values in cart_options.items():
                print(f"[{key}] {values}")

            choice = int(input(">>> "))
            match choice:
                case 1:
                    add_to_cart(cart)
                case 2:
                    update_to_cart(cart)
                case 3:
                    remove_from_cart(cart)
                case 4:
                    view_cart(cart)
                case 5:
                    break
        except ValueError:
            print("Option must be a number between 1 and 5")
    
    print("Exiting program...")


if __name__ == "__main__":
    main()