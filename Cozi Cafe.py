import time

MENU = {
    "Indian": {
        1: {"name": "Butter Naan", "price": 100},
        2: {"name": "Chicken Tikka Masala", "price": 450},
        3: {"name": "Paneer Makhani", "price": 380},
        4: {"name": "Veg Biryani", "price": 320},
        5: {"name": "Roti", "price": 30},
        6: {"name": "Paratha", "price": 40},
        7: {"name": "Rice", "price": 80},
    },
    "Chinese": {
        1: {"name": "Veg Spring Rolls", "price": 220},
        2: {"name": "Hakka Noodles", "price": 280},
        3: {"name": "Chilli Paneer", "price": 350},
        4: {"name": "Manchurian Dry", "price": 300},
    },
    "Italian": {
        1: {"name": "Margherita Pizza", "price": 550},
        2: {"name": "Spaghetti Aglio e Olio", "price": 420},
        3: {"name": "Veg Lasagna", "price": 480},
        4: {"name": "Tiramisu (Dessert)", "price": 290},
    },
    "Drinks": {
        1: {"name": "Water", "price": 20},
        2: {"name": "Cola", "price": 60},
        3: {"name": "Juice", "price": 80},
    },
    "Desserts": {
        1: {"name": "Gulab Jamun", "price": 120},
        2: {"name": "Ice Cream", "price": 150},
    },
}

SERVICE_CHARGE_RATE = 0.10
GST_RATE = 0.18
BULK_DISCOUNT_RATE = 0.10
BULK_DISCOUNT_THRESHOLD = 3500

def display_menu():
    """Displays the entire cafe menu categorized by cuisine."""
    print("=" * 50)
    print("         Welcome to The Beginner's Cafe!         ")
    print("=" * 50)
    for category_name, items in MENU.items():
        print(f"\n--- {category_name} Dishes ---")
        for item_num, item_details in items.items():
            name = item_details["name"]
            price = item_details["price"]
            print(f"[{item_num}] {name:<25} Rs. {price:>.2f}")

def take_order():
    """Allows the user to select items and quantities."""
    order = []
    print("\n--- Placing Your Order ---")

    category_names = list(MENU.keys())
    while True:
        print("\nAvailable Categories:")
        for i, category_name in enumerate(category_names):
            print(f"[{i+1}] {category_name}")
        print("Enter category number (or '0' to finish order): ")

        category_input = input("Your choice: ").strip()

        if category_input == '0':
            break

        try:
            category_num = int(category_input)
            if 1 <= category_num <= len(category_names):
                category_choice = category_names[category_num - 1]
            else:
                print("Invalid category number. Please try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number or '0' to finish.")
            continue

        print(f"\n--- {category_choice} Menu ---")
        category_items = MENU[category_choice]
        for num, details in category_items.items():
            print(f"[{num}] {details['name']:<25} Rs. {details['price']:>.2f}")

        while True:
            item_input = input("Enter item number to add, 'C' to change category, or 'F' to finish ordering: ").strip().upper()

            if item_input == 'C':
                break
            if item_input == 'F':
                return order

            try:
                item_num = int(item_input)
                if item_num in category_items:
                    item = category_items[item_num]
                    while True:
                        try:
                            quantity = int(input(f"How many units of {item['name']} do you want? "))
                            if quantity > 0:
                                order.append({
                                    "name": item["name"],
                                    "price": item["price"],
                                    "quantity": quantity
                                })
                                print(f"Added {quantity} x {item['name']} to your order.")
                                break
                            else:
                                print("Quantity must be greater than zero.")
                        except ValueError:
                            print("Invalid quantity. Please enter a number.")
                else:
                    print("Invalid item number for this category. Please try again.")
            except ValueError:
                print("Invalid input. Please enter an item number, 'C', or 'F'.")
    return order

def calculate_bill(order):
    """Calculates the total bill including discounts, service charge, and GST."""
    if not order:
        return 0, 0, 0, 0, 0, 0

    subtotal = sum(item["price"] * item["quantity"] for item in order)

    discount_amount = 0
    if subtotal > BULK_DISCOUNT_THRESHOLD:
        discount_amount = subtotal * BULK_DISCOUNT_RATE
        print(f"\n Applied 10% Discount: Rs. {discount_amount:.2f} (Order above Rs. {BULK_DISCOUNT_THRESHOLD})")

    total_after_discount = subtotal - discount_amount

    service_charge = total_after_discount * SERVICE_CHARGE_RATE

    subtotal_for_gst = total_after_discount + service_charge

    gst_amount = subtotal_for_gst * GST_RATE

    grand_total = subtotal_for_gst + gst_amount

    return subtotal, discount_amount, service_charge, gst_amount, grand_total, total_after_discount

def print_bill(order, subtotal, discount_amount, service_charge, gst_amount, grand_total, total_after_discount):
    """Prints the final detailed receipt."""
    print("\n" + "=" * 50)
    print("               FINAL RECEIPT              ")
    print("=" * 50)

    print("{:<3} {:<25} {:>8} {:>10}".format("Qty", "Item", "Price", "Amount"))
    print("-" * 50)
    for item in order:
        item_total = item["price"] * item["quantity"]
        print("{:<3} {:<25} {:>8.2f} {:>10.2f}".format(
            item["quantity"],
            item["name"],
            item["price"],
            item_total
        ))
    print("-" * 50)
    print(f"{'SUBTOTAL (Items)':<40} Rs. {subtotal:>8.2f}")

    if discount_amount > 0:
        print(f"{'DISCOUNT (10%)':<40} -Rs. {discount_amount:>8.2f}")
        print(f"{'TOTAL AFTER DISCOUNT':<40} Rs. {total_after_discount:>8.2f}")
        print("-" * 50)

    print(f"{'Service Charge (10%)':<40} +Rs. {service_charge:>8.2f}")
    print(f"{'Total Before GST':<40} Rs. {total_after_discount + service_charge:>8.2f}")
    print(f"{'GST (18%)':<40} +Rs. {gst_amount:>8.2f}")

    print("=" * 50)
    print(f"{'GRAND TOTAL TO PAY':<40} Rs. {grand_total:>8.2f}")
    print("=" * 50)
    print("Thank you for dining with us! Please come again.")

if __name__ == "__main__":
    display_menu()
    customer_order = take_order()

    if not customer_order:
        print("\nNo items were ordered. Goodbye!")
    else:
        print("\nCalculating your bill...")