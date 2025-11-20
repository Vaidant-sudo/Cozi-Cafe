import time

# --- 1. SETUP: Menu and Rates ---

# MENU STRUCTURE: Key is Category ID (1, 2, 3, 4), Value is a dictionary containing the name and items.
MENU = {
    1:{"Indian": {
        1: {"name": "Butter Naan", "price": 100},
        2: {"name": "Chicken Tikka Masala", "price": 450},
        3: {"name": "Paneer Makhani", "price": 380},
        4: {"name": "Veg Biryani", "price": 320},},},
    2:{"Chinese": {
        1: {"name": "Veg Spring Rolls", "price": 220},
        2: {"name": "Hakka Noodles", "price": 280},
        3: {"name": "Chilli Paneer", "price": 350},
        4: {"name": "Manchurian Dry", "price": 300},},},
    3:{"Italian": {
        1: {"name": "Margherita Pizza", "price": 550},
        2: {"name": "Spaghetti Aglio e Olio", "price": 420},
        3: {"name": "Veg Lasagna", "price": 480},
        4: {"name": "Tiramisu (Dessert)", "price": 290},},},
    4:{"Beverages": {
        1: {"name": "Iced latte", "price": 150},
        2: {"name": "Cappuccino", "price": 220},
        3: {"name": "Americano", "price": 250},
        4: {"name": "Espresso", "price": 300},
        5: {"name": "Hot chocolate", "price": 220},},},}

SERVICE_CHARGE_RATE = 0.10     # 10% Service Charge
GST_RATE = 0.18                # 18% Tax
BULK_DISCOUNT_RATE = 0.10      # 10% Discount
BULK_DISCOUNT_THRESHOLD = 3500 # Discount applied for bills > Rs. 3500

# --- 2. DISPLAY MENU ---
def display_menu():
    """Displays the entire cafe menu categorized by cuisine."""
    print("=" * 50)
    print("      Welcome to The Beginner's Cafe!     ")
    print("=" * 50)
    
    # Iterate through the main category keys (1, 2, 3, 4)
    for category_id, category_data in MENU.items():
        # Get the category name and its items
        category_name = list(category_data.keys())[0] 
        category_items = category_data[category_name]

        print(f"\n--- [{category_id}] {category_name} Dishes ---")
        
        for item_num, item_details in category_items.items():
            name = item_details["name"]
            price = item_details["price"]
            print(f"[{item_num}] {name:<25} Rs. {price:>.2f}")


# --- 3. TAKE ORDER ---
def take_order():
    """Allows the user to select items and quantities, consolidating duplicate items."""
    order = []
    print("\n--- Placing Your Order ---")

    while True:
        print("\nAvailable Categories:")
        # Show category IDs and names for selection
        for category_id, data in MENU.items():
             print(f"[{category_id}] {list(data.keys())[0]}")
        
        print("\nEnter '0' to finish ordering.")
        category_choice_input = input("Enter category number to view: ").strip()

        if category_choice_input == "0":
            break

        try:
            category_id = int(category_choice_input)
            if category_id not in MENU:
                print("Invalid category number. Please try again.")
                continue
            
            # Get the category name and its items based on the chosen ID
            category_data = MENU[category_id]
            category_name = list(category_data.keys())[0]
            category_items = category_data[category_name]
            
        except ValueError:
            print("Invalid input. Please enter a number or '0'.")
            continue


        print(f"\n--- {category_name} Menu ---")
        for num, details in category_items.items():
            print(f"[{num}] {details['name']:<25} Rs. {details['price']:>.2f}")

        while True:
            item_input = input("Enter item number to add, or '0' to go back to categories: ").strip()

            if item_input == '0':
                break 

            try:
                item_num = int(item_input)
                if item_num in category_items:
                    item = category_items[item_num]
                    
                    while True:
                        try:
                            quantity_input = input(f"How many units of {item['name']} do you want? ").strip()
                            
                            if not quantity_input.isdigit():
                                print("Invalid quantity. Please enter a whole number (e.g., 1, 2, 3).")
                                continue
                            
                            quantity = int(quantity_input)
                            
                            if quantity > 0:
                                
                                # Logic to check if item already exists and update quantity (Fix for Consolidation)
                                item_name = item["name"]
                                item_exists = False
                                for ordered_item in order:
                                    # Check if the item name already exists in the order list
                                    if ordered_item['name'] == item_name:
                                        ordered_item['quantity'] += quantity
                                        item_exists = True
                                        break
                                
                                if not item_exists:
                                    # If not found, add a new entry
                                    order.append({
                                        "name": item_name,
                                        "price": item["price"],
                                        "quantity": quantity
                                    })
                                    
                                print(f"Added {quantity} x {item_name} to your order.")
                                break
                            else:
                                print("Quantity must be greater than zero.")
                        except ValueError:
                            print("Invalid quantity format. Please enter a number.") 
                else:
                    print("Invalid item number for this category. Please try again.")
            except ValueError:
                print("Invalid input. Please enter an item number or '0'.")
                
    return order


# --- 4. CALCULATE AND PRINT BILL ---

def calculate_bill(order):
    """Calculates the total bill including discounts, service charge, and GST."""
    
    if not order:
        # Return 7 values (including False for discount) if order is empty
        return 0, 0, 0, 0, 0, 0, False 

    # 1. Calculate the raw subtotal (Price * Quantity)
    subtotal = sum(item["price"] * item["quantity"] for item in order)

    # 2. Apply Discount (Bulk Discount)
    discount_amount = 0
    is_discount_applied = False 

    if subtotal > BULK_DISCOUNT_THRESHOLD:
        discount_amount = subtotal * BULK_DISCOUNT_RATE
        is_discount_applied = True 

    total_after_discount = subtotal - discount_amount

    # 3. Calculate Service Charge (applied after discount)
    service_charge = total_after_discount * SERVICE_CHARGE_RATE

    # 4. Total before GST
    subtotal_for_gst = total_after_discount + service_charge

    # 5. Calculate GST (applied to the subtotal + service charge)
    gst_amount = subtotal_for_gst * GST_RATE

    # 6. Final Grand Total
    grand_total = subtotal_for_gst + gst_amount

    # Returns 7 values (Fix for Unpacking Error)
    return subtotal, discount_amount, service_charge, gst_amount, grand_total, total_after_discount, is_discount_applied

def print_bill(order, subtotal, discount_amount, service_charge, gst_amount, grand_total, total_after_discount, is_discount_applied):
    """Prints the final detailed receipt."""
    print("\n" + "=" * 50)
    print("              FINAL RECEIPT              ")
    print("=" * 50)

    # Table Header
    print("{:<3} {:<25} {:>8} {:>10}".format("Qty", "Item", "Price", "Amount"))
    print("-" * 50)
    
    # Itemized List
    for item in order:
        item_total = item["price"] * item["quantity"]
        print("{:<3} {:<25} {:>8.2f} {:>10.2f}".format(
            item["quantity"],
            item["name"],
            item["price"],
            item_total
        ))
    
    print("-" * 50)
    
    # Summary Calculations
    print(f"{'SUBTOTAL (Items)':<40} Rs. {subtotal:>8.2f}")

    if is_discount_applied:
        # Discount message printed here
        print(f"\n*Congratulations! You qualified for the 10% discount.*")
        # Fixed formatting error in the print statement below
        print(f"{'DISCOUNT (10% on Rs. 3500.00+ )':<40} -Rs. {discount_amount:>8.2f}")
    
    # Display total after discount regardless of whether discount was applied
    print(f"{'TOTAL AFTER DISCOUNT':<40} Rs. {total_after_discount:>8.2f}")
    
    print("-" * 50)
    
    # Charges and Taxes
    print(f"{'Service Charge (10%)':<40} +Rs. {service_charge:>8.2f}")
    
    total_before_gst = total_after_discount + service_charge
    print(f"{'Total Before GST':<40} Rs. {total_before_gst:>8.2f}")
    
    print(f"{'GST (18%)':<40} +Rs. {gst_amount:>8.2f}")

    print("=" * 50)
    print(f"{'GRAND TOTAL TO PAY':<40} Rs. {grand_total:>8.2f}")
    print("=" * 50)
    print("Thank you for dining with us! Please come again.")


# --- 5. RUN APPLICATION ---
if __name__ == "__main__":
    display_menu()
    customer_order = take_order()

    if not customer_order:
        print("\nNo items were ordered. Goodbye!")
    else:
        print("\nCalculating your bill...")
        time.sleep(1) 
        
        # Unpacks all 7 values correctly
        (subtotal, discount_amount, service_charge, gst_amount, grand_total, total_after_discount, is_discount_applied) = calculate_bill(customer_order)
        
        # Passes the order data and calculation results to the print function
        print_bill(customer_order, subtotal, discount_amount, service_charge, gst_amount, grand_total, total_after_discount, is_discount_applied)