from datetime import datetime, timedelta
import os

class Product:

    def __init__(self, code, name, category, price, status="Available"):
        self.code = code
        self.name = name
        self.category = category

        self.price = float(price)
        self.status = status
        self.rating = 0.0
        self.rating_count = 0

    def __str__(self):
        rating_str = f" ⭐{self.rating:.1f}/5 ({self.rating_count} reviews)" if self.rating_count > 0 else ""
        return f"{self.code:<10} {self.name:<25} {self.category:<15} ${self.price:<8.2f} {self.status}{rating_str}"

    def update_price(self, new_price):
        self.price = float(new_price)

    def update_status(self, new_status):
        self.status = new_status

    def add_rating(self, rating):
        total_rating = self.rating * self.rating_count
        self.rating_count += 1
        self.rating = (total_rating + rating) / self.rating_count


class Addon:

    def __init__(self, code, name, price, status="Available"):
        self.code = code
        self.name = name
        self.price = float(price)
        self.status = status

    def __str__(self):
        return f"{self.code:<10} {self.name:<30} ${self.price:<8.2f} {self.status}"

    def update_price(self, new_price):
        self.price = float(new_price)

    def update_status(self, new_status):
        self.status = new_status


class Order:
    order_counter = 1

    def __init__(self, product, addon=None, customer_name="", recipient_name="",
                 message="", delivery_address="", delivery_date="", same_day=False,
                 is_delivery=True):
        self.order_id = f"BBO-25-{Order.order_counter:04d}"
        Order.order_counter += 1
        self.product = product
        self.addon = addon
        self.customer_name = customer_name
        self.recipient_name = recipient_name
        self.message = message
        self.delivery_address = delivery_address
        self.delivery_date = delivery_date
        self.same_day = same_day
        self.is_delivery = is_delivery
        self.status = "Open"
        self.created_date = datetime.now()

    def calculate_total(self):
        total = self.product.price
        if self.addon:
            total += self.addon.price

        if self.is_delivery:
            delivery_charge = 35
            if self.delivery_date:
                try:
                    delivery_dt = datetime.strptime(self.delivery_date, "%d/%m/%Y")
                    if delivery_dt.weekday() >= 5:
                        delivery_charge += 10
                except:
                    pass

            total += delivery_charge
            if self.same_day:
                total += 35

        return total

    def get_summary(self):
        summary = "=" * 60 + "\n"
        summary += f"{'ORDER SUMMARY':^60}\n"
        summary += "=" * 60 + "\n"
        summary += f"Order ID: {self.order_id}\n"
        summary += f"Status: {self.status}\n"
        summary += "-" * 60 + "\n"
        summary += f"Item: {self.product.name} ({self.product.code}) ${self.product.price:.2f}\n"

        if self.addon:
            summary += f"Add-on: {self.addon.name} ({self.addon.code}) ${self.addon.price:.2f}\n"

        summary += "-" * 60 + "\n"

        if self.is_delivery:
            summary += f"Delivery Date: {self.delivery_date}\n"
            delivery_charge = 35
            if self.delivery_date:
                try:
                    delivery_dt = datetime.strptime(self.delivery_date, "%d/%m/%Y")
                    if delivery_dt.weekday() >= 5:
                        delivery_charge = 45
                        summary += "Weekend Delivery: +$10\n"
                except:
                    pass

            summary += f"Same Day Delivery: {'Yes' if self.same_day else 'No'} ${35 if self.same_day else 0:.2f}\n"
            summary += f"Delivery Charges: ${delivery_charge:.2f}\n"
        else:
            summary += "Pickup: Store Pickup (No Delivery Charge)\n"

        summary += "-" * 60 + "\n"
        summary += f"Total: ${self.calculate_total():.2f}\n"
        summary += "=" * 60 + "\n"
        summary += f"Customer Name: {self.customer_name}\n"
        summary += f"Recipient Name: {self.recipient_name}\n"
        summary += f"Message: {self.message}\n"

        if self.is_delivery:
            summary += f"Delivery Address: {self.delivery_address}\n"

        summary += "=" * 60 + "\n"

        return summary

    def update_status(self, new_status):
        self.status = new_status


def load_products():
    products = {}
    try:
        with open("Products.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 5:
                        code, name, category, price, status = parts
                        products[code] = Product(code, name, category, price, status)
                    elif len(parts) == 4:
                        code, name, category, price = parts
                        products[code] = Product(code, name, category, price)
        print(f"✓ Loaded {len(products)} products successfully")
    except FileNotFoundError:
        print("⚠ Products.txt not found. Starting with empty inventory.")
    except Exception as e:
        print(f"⚠ Error loading products: {e}")

    return products


def save_products(products):
    try:
        with open("Products.txt", "w", encoding="utf-8") as file:
            for product in products.values():
                file.write(f"{product.code},{product.name},{product.category},{product.price},{product.status}\n")
        return True
    except Exception as e:
        print(f"⚠ Error saving products: {e}")
        return False


def load_addons():
    addons = {}
    try:
        with open("Addons.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 4:
                        code, name, price, status = parts
                        addons[code] = Addon(code, name, price, status)
                    elif len(parts) == 3:
                        code, name, price = parts
                        addons[code] = Addon(code, name, price)
        print(f"✓ Loaded {len(addons)} add-ons successfully")
    except FileNotFoundError:
        print("⚠ Addons.txt not found. Creating default add-ons.")
        addons = {
            "ADD001": Addon("ADD001", "Chocolates", 8),
            "ADD002": Addon("ADD002", "Customized Handwritten card", 12),
            "ADD003": Addon("ADD003", "Soft Toy", 16)
        }
        save_addons(addons)
    except Exception as e:
        print(f"⚠ Error loading add-ons: {e}")

    return addons


def save_addons(addons):
    try:
        with open("Addons.txt", "w", encoding="utf-8") as file:
            for addon in addons.values():
                file.write(f"{addon.code},{addon.name},{addon.price},{addon.status}\n")
        return True
    except Exception as e:
        print(f"⚠ Error saving add-ons: {e}")
        return False


def save_orders(orders):
    try:
        with open("Orders.txt", "w", encoding="utf-8") as file:
            for order in orders.values():
                addon_code = order.addon.code if order.addon else "NONE"
                file.write(f"{order.order_id}|{order.product.code}|{addon_code}|")
                file.write(f"{order.customer_name}|{order.recipient_name}|{order.message}|")
                file.write(f"{order.delivery_address}|{order.delivery_date}|")
                file.write(f"{order.same_day}|{order.is_delivery}|{order.status}\n")
        return True
    except Exception as e:
        print(f"⚠ Error saving orders: {e}")
        return False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def print_menu(title, options):
    print_header(title)
    for key, value in options.items():
        print(f"{key}. {value}")
    print("-" * 60)


def get_valid_input(prompt, valid_options=None, input_type=str):
    while True:
        try:
            user_input = input(prompt).strip()

            if input_type == int:
                user_input = int(user_input)
            elif input_type == float:
                user_input = float(user_input)

            if valid_options and user_input not in valid_options:
                print(f"⚠ Invalid option. Please choose from {valid_options}")
                continue

            return user_input
        except ValueError:
            print(f"⚠ Invalid input. Please enter a valid {input_type.__name__}")
        except KeyboardInterrupt:
            print("\n⚠ Operation cancelled by user")
            return None


def generate_unique_code(prefix, existing_codes):
    counter = 1
    while True:
        code = f"{prefix}{counter:03d}"
        if code not in existing_codes:
            return code
        counter += 1

def view_update_blooms(products):
    print_header("VIEW / UPDATE BLOOMS")

    if not products:
        print("⚠ No products available")
        input("\nPress Enter to continue...")
        return

    print(f"\n{'Code':<10} {'Name':<25} {'Category':<15} {'Price':<10} {'Status'}")
    print("-" * 80)
    for product in products.values():
        print(product)

    print("\n" + "-" * 60)
    code = input("To update an item, enter the item code (or 0 to go back): ").strip().upper()

    if code == "0":
        return

    if code not in products:
        print(f"⚠ Product code '{code}' not found!")
        input("\nPress Enter to continue...")
        return

    product = products[code]
    print(f"\nCurrent details for {product.name}:")
    print(f"Price: ${product.price:.2f}")
    print(f"Status: {product.status}")

    new_price_input = input(f"\nEnter new price (or press Enter to keep ${product.price:.2f}): ").strip()
    if new_price_input:
        try:
            new_price = float(new_price_input)
            if new_price > 0:
                product.update_price(new_price)
                print(f"✓ Price updated to ${new_price:.2f}")
            else:
                print("⚠ Price must be positive")
        except ValueError:
            print("⚠ Invalid price format")

    print("\nStatus options: Available, Unavailable")
    new_status = input(f"Enter new status (or press Enter to keep '{product.status}'): ").strip()
    if new_status:
        if new_status in ["Available", "Unavailable"]:
            product.update_status(new_status)
            print(f"✓ Status updated to '{new_status}'")
        else:
            print("⚠ Invalid status")

    if save_products(products):
        print("\n✓ Changes saved successfully!")
    else:
        print("\n⚠ Failed to save changes")

    input("\nPress Enter to continue...")


def add_new_bloom(products):
    print_header("ADD NEW BLOOM")

    name = input("Enter product name: ").strip()
    if not name:
        print("⚠ Product name cannot be empty")
        input("\nPress Enter to continue...")
        return

    print("\n1. Auto-generate code")
    print("2. Manually enter code")
    choice = get_valid_input("Choose option: ", ["1", "2"])

    if choice == "1":
        code = None
    else:
        code = input("Enter product code: ").strip().upper()
        if code in products:
            print(f"⚠ Code '{code}' already exists!")
            input("\nPress Enter to continue...")
            return

    try:
        price = float(input("Enter price: $").strip())
        if price <= 0:
            print("⚠ Price must be positive")
            input("\nPress Enter to continue...")
            return
    except ValueError:
        print("⚠ Invalid price format")
        input("\nPress Enter to continue...")
        return

    categories = ["Romantic", "Birthday", "Grand Opening", "Condolence", "Anniversary"]
    print("\nSelect category:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    cat_choice = get_valid_input("Enter choice (1-5): ", [str(i) for i in range(1, 6)])
    if cat_choice is None:
        return

    category = categories[int(cat_choice) - 1]

    if choice == "1":
        prefix_map = {
            "Romantic": "R",
            "Birthday": "B",
            "Grand Opening": "GO",
            "Condolence": "C",
            "Anniversary": "A"
        }
        prefix = prefix_map[category]
        code = generate_unique_code(prefix, products.keys())
        print(f"\n✓ Generated code: {code}")

    new_product = Product(code, name, category, price, "Available")
    products[code] = new_product

    if save_products(products):
        print(f"\n✓ Product '{name}' ({code}) added successfully!")
    else:
        print("\n⚠ Failed to save product")

    input("\nPress Enter to continue...")


def view_update_addons(addons):
    print_header("VIEW / UPDATE ADD-ONS")

    if not addons:
        print("⚠ No add-ons available")
        input("\nPress Enter to continue...")
        return

    print(f"\n{'Code':<10} {'Name':<30} {'Price':<10} {'Status'}")
    print("-" * 60)
    for addon in addons.values():
        print(addon)

    print("\n" + "-" * 60)
    code = input("To update an item, enter the item code (or 0 to go back): ").strip().upper()

    if code == "0":
        return

    if code not in addons:
        print(f"⚠ Add-on code '{code}' not found!")
        input("\nPress Enter to continue...")
        return

    addon = addons[code]
    print(f"\nCurrent details for {addon.name}:")
    print(f"Price: ${addon.price:.2f}")
    print(f"Status: {addon.status}")

    new_price_input = input(f"\nEnter new price (or press Enter to keep ${addon.price:.2f}): ").strip()
    if new_price_input:
        try:
            new_price = float(new_price_input)
            if new_price > 0:
                addon.update_price(new_price)
                print(f"✓ Price updated to ${new_price:.2f}")
            else:
                print("⚠ Price must be positive")
        except ValueError:
            print("⚠ Invalid price format")

    print("\nStatus options: Available, Unavailable")
    new_status = input(f"Enter new status (or press Enter to keep '{addon.status}'): ").strip()
    if new_status:
        if new_status in ["Available", "Unavailable"]:
            addon.update_status(new_status)
            print(f"✓ Status updated to '{new_status}'")
        else:
            print("⚠ Invalid status")

    if save_addons(addons):
        print("\n✓ Changes saved successfully!")
    else:
        print("\n⚠ Failed to save changes")

    input("\nPress Enter to continue...")


def add_new_addon(addons):
    print_header("ADD NEW ADD-ON")

    name = input("Enter add-on name: ").strip()
    if not name:
        print("⚠ Add-on name cannot be empty")
        input("\nPress Enter to continue...")
        return

    print("\n1. Auto-generate code")
    print("2. Manually enter code")
    choice = get_valid_input("Choose option: ", ["1", "2"])

    if choice == "1":
        code = generate_unique_code("ADD", addons.keys())
        print(f"\n✓ Generated code: {code}")
    else:
        code = input("Enter add-on code: ").strip().upper()
        if code in addons:
            print(f"⚠ Code '{code}' already exists!")
            input("\nPress Enter to continue...")
            return

    try:
        price = float(input("Enter price: $").strip())
        if price <= 0:
            print("⚠ Price must be positive")
            input("\nPress Enter to continue...")
            return
    except ValueError:
        print("⚠ Invalid price format")
        input("\nPress Enter to continue...")
        return

    new_addon = Addon(code, name, price, "Available")
    addons[code] = new_addon

    if save_addons(addons):
        print(f"\n✓ Add-on '{name}' ({code}) added successfully!")
    else:
        print("\n⚠ Failed to save add-on")

    input("\nPress Enter to continue...")


def inventory_management_menu(products, addons):
    while True:
        print_menu("@@@@ INVENTORY MANAGEMENT @@@@", {
            "1": "View / Update Blooms",
            "2": "Add New Bloom",
            "3": "View / Update Add-ons",
            "4": "Add New Add-on",
            "5": "Back to Main Menu"
        })

        choice = get_valid_input("Enter option: ",


                                 ["1", "2", "3", "4", "5"])

        if choice == "1":
            view_update_blooms(products)
        elif choice == "2":
            add_new_bloom(products)
        elif choice == "3":
            view_update_addons(addons)
        elif choice == "4":
            add_new_addon(addons)
        elif choice == "5":
            break

def display_products(products, category_filter=None, sort_by_price=False, sort_by_rating=False):
    filtered_products = [p for p in products.values() if p.status == "Available"]

    if category_filter:
        filtered_products = [p for p in filtered_products if p.category == category_filter]

    if sort_by_price:
        filtered_products.sort(key=lambda x: x.price)
    elif sort_by_rating:
        filtered_products.sort(key=lambda x: x.rating, reverse=True)

    if not filtered_products:
        print("\n⚠ No products available")
        return False

    print(f"\n{'Code':<10} {'Name':<25} {'Category':<15} {'Price':<10} {'Status'}")
    print("-" * 80)
    for product in filtered_products:
        print(product)

    return True


def create_order(products, addons, orders):
    print_header("CREATE ORDER")

    selected_product = None

    while True:
        has_products = display_products(products)

        if not has_products:
            input("\nPress Enter to continue...")
            return

        print("\n" + "-" * 60)
        print("1. Filter products by category")
        print("2. Sort products by price")
        print("3. Sort products by rating (BONUS)")
        print("4. Order item")
        print("0. Back to main menu")

        choice = get_valid_input("\nEnter option: ", ["0", "1", "2", "3", "4"])

        if choice == "0":
            return
        elif choice == "1":
            categories = ["Romantic", "Birthday", "Grand Opening", "Condolence", "Anniversary"]
            print("\nSelect category:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            print("0. Go back")

            cat_choice = get_valid_input("Select filter category: ",
                                         [str(i) for i in range(0, 6)])

            if cat_choice == "0":
                continue

            category = categories[int(cat_choice) - 1]
            display_products(products, category_filter=category)

            print("\n1. Order item")
            print("2. Back to filter category")
            print("3. Back to main menu")

            sub_choice = get_valid_input("\nEnter option: ", ["1", "2", "3"])

            if sub_choice == "1":
                choice = "4"
            elif sub_choice == "3":
                return
            else:
                continue

        elif choice == "2":
            display_products(products, sort_by_price=True)

            print("\n1. Order item")
            print("2. Back to main menu")

            sub_choice = get_valid_input("\nEnter option: ", ["1", "2"])

            if sub_choice == "1":
                choice = "4"
            else:
                return

        elif choice == "3":
            display_products(products, sort_by_rating=True)

            print("\n1. Order item")
            print("2. Back to main menu")

            sub_choice = get_valid_input("\nEnter option: ", ["1", "2"])

            if sub_choice == "1":
                choice = "4"
            else:
                return

        if choice == "4":
            item_code = input("\nPlease enter item code: ").strip().upper()

            if item_code not in products:
                print(f"⚠ Invalid item code '{item_code}'")
                input("\nPress Enter to continue...")
                continue

            if products[item_code].status != "Available":
                print(f"⚠ Item '{item_code}' is not available")
                input("\nPress Enter to continue...")
                continue

            selected_product = products[item_code]
            break

    print("\nAvailable add-ons:")
    print(f"{'Code':<10} {'Name':<30} {'Price'}")
    print("-" * 50)
    for addon in addons.values():
        if addon.status == "Available":
            print(f"{addon.code:<10} {addon.name:<30} ${addon.price:.2f}")

    addon_code = input("\nEnter item code for addon (or 0 to skip): ").strip().upper()
    selected_addon = None

    if addon_code != "0":
        if addon_code in addons and addons[addon_code].status == "Available":
            selected_addon = addons[addon_code]
        else:
            print("⚠ Invalid addon code. Proceeding without addon.")

    print("\n" + "=" * 60)
    customer_name = input("Customer name: ").strip()
    recipient_name = input("Recipient's name: ").strip()
    message = input("Message for recipient (max 300 characters): ").strip()[:300]

    delivery_choice = input("\nStore pickup or Delivery? (Enter 'P' for pickup, 'D' for delivery): ").strip().upper()
    is_delivery = delivery_choice == "D"

    delivery_address = ""
    delivery_date = ""
    same_day = False

    if is_delivery:
        delivery_address = input("Delivery address: ").strip()
        delivery_date = input("Delivery date (DD/MM/YYYY): ").strip()

        same_day_choice = input("Same day delivery? (Y/N): ").strip().upper()
        same_day = same_day_choice == "Y"

    new_order = Order(
        product=selected_product,
        addon=selected_addon,
        customer_name=customer_name,
        recipient_name=recipient_name,
        message=message,
        delivery_address=delivery_address,
        delivery_date=delivery_date,
        same_day=same_day,

        is_delivery=is_delivery
    )

    print("\n" + new_order.get_summary())

    confirm = input("Enter 1 to confirm, 2 to edit info, 0 to cancel: ").strip()

    if confirm == "1":
        orders[new_order.order_id] = new_order
        save_orders(orders)
        print(f"\n✓ Order {new_order.order_id} created successfully!")

        rate_choice = input("\nWould you like to rate this product? (Y/N): ").strip().upper()
        if rate_choice == "Y":
            try:
                rating = float(input("Enter rating (1-5): ").strip())
                if 1 <= rating <= 5:
                    selected_product.rating_count += 1
                    total = selected_product.rating * (selected_product.rating_count - 1) + rating
                    selected_product.rating = total / selected_product.rating_count
                    save_products(products)
                    print("✓ Thank you for your rating!")
            except:
                print("⚠ Invalid rating")

    elif confirm == "2":
        create_order(products, addons, orders)
    else:
        print("\n⚠ Order cancelled")

    input("\nPress Enter to continue...")


def view_orders(orders, products):
    print_header("VIEW ORDERS")

    if not orders:
        print("⚠ No orders found")
        input("\nPress Enter to continue...")
        return

    filter_status = "Open"

    while True:
        filtered_orders = [o for o in orders.values() if o.status == filter_status]

        if not filtered_orders:
            print(f"\n⚠ No orders with status '{filter_status}'")
        else:
            print(f"\nOrders with status: {filter_status}")
            print("-" * 80)
            for order in filtered_orders:
                print(f"Order ID: {order.order_id}")
                print(f"Customer: {order.customer_name} | Recipient: {order.recipient_name}")
                print(f"Product: {order.product.name} | Total: ${order.calculate_total():.2f}")
                print(f"Status: {order.status}")
                if order.is_delivery:
                    print(f"Delivery: {order.delivery_date} to {order.delivery_address}")
                print("-" * 80)

        print("\n1. Edit/Cancel order")
        print("2. Filter order by status")
        print("3. Back to main menu")

        choice = get_valid_input("\nEnter option: ", ["1", "2", "3"])

        if choice == "1":
            order_id = input("\nEnter order ID: ").strip().upper()

            if order_id not in orders:
                print(f"⚠ Order '{order_id}' not found!")
                input("\nPress Enter to continue...")
                continue

            order = orders[order_id]
            print(f"\nOrder ID: {order.order_id}")
            print(f"Current Status: {order.status}")

            status_options = {
                "Open": ["Cancel order", "Change to Preparing"],
                "Cancelled": ["Set back to Open"],
                "Preparing": ["Change to Ready"],
                "Ready": ["Change to Preparing", "Change to Closed"],
                "Closed": []
            }

            options = status_options.get(order.status, [])

            if not options:
                print("\n⚠ No status change options available for closed orders")
                input("\nPress Enter to continue...")
                continue

            print("\nAvailable actions:")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            print("0. Go back")

            action = get_valid_input("\nSelect action: ",
                                     [str(i) for i in range(0, len(options) + 1)])

            if action == "0":
                continue

            action_idx = int(action) - 1
            selected_action = options[action_idx]

            if "Cancel" in selected_action:
                order.update_status("Cancelled")
                print("✓ Order cancelled")
            elif "Preparing" in selected_action:
                order.update_status("Preparing")
                print("✓ Order status changed to Preparing")
            elif "Ready" in selected_action:
                order.update_status("Ready")
                print("✓ Order status changed to Ready")
            elif "Closed" in selected_action:
                order.update_status("Closed")
                print("✓ Order status changed to Closed")
            elif "Open" in selected_action:
                order.update_status("Open")
                print("✓ Order status changed to Open")


            if order.is_delivery and order.delivery_date:
                try:
                    delivery_dt = datetime.strptime(order.delivery_date, "%d/%m/%Y")
                    today = datetime.now().date()
                    if delivery_dt.date() == today and order.status != "Ready":
                        print("⚠ ALERT: This order is scheduled for delivery TODAY!")
                        auto_change = input("Change status to 'Deliver Today'? (Y/N): ").strip().upper()
                        if auto_change == "Y":
                            order.update_status("Deliver Today")
                            print("✓ Status updated to 'Deliver Today'")
                except:
                    pass

            save_orders(orders)
            input("\nPress Enter to continue...")

        elif choice == "2":
            print("\nFilter by status:")
            print("1. Open")
            print("2. Preparing")
            print("3. Ready")
            print("4. Closed")
            print("5. Cancelled")
            print("6. Deliver Today (BONUS)")

            status_choice = get_valid_input("Select status: ", ["1", "2", "3", "4", "5", "6"])

            status_map = {
                "1": "Open",
                "2": "Preparing",
                "3": "Ready",
                "4": "Closed",
                "5": "Cancelled",
                "6": "Deliver Today"
            }

            filter_status = status_map[status_choice]

        elif choice == "3":
            break


def sales_management_menu(products, addons, orders):
    while True:
        print_menu("@@@@ SALES MANAGEMENT @@@@", {
            "1": "Create Order",
            "2": "View Orders",
            "3": "Back to Main Menu"
        })

        choice = get_valid_input("Enter option: ", ["1", "2", "3"])

        if choice == "1":
            create_order(products, addons, orders)
        elif choice == "2":
            view_orders(orders, products)
        elif choice == "3":
            break

def main():
    print("=" * 60)
    print(f"{'BEAUTIFUL BLOOMS MANAGEMENT SYSTEM':^60}")
    print(f"{'Initializing...':^60}")
    print("=" * 60)

    products = load_products()
    addons = load_addons()
    orders = {}

    print("\n✓ System initialized successfully!")
    input("\nPress Enter to continue to main menu...")

    while True:
        print_menu("@@@@ BEAUTIFUL BLOOMS @@@@", {
            "1": "Inventory Management",
            "2": "Sales Management",
            "3": "Exit"
        })

        choice = get_valid_input("Enter option: ", ["1", "2", "3"])

        if choice == "1":
            inventory_management_menu(products, addons)
        elif choice == "2":
            sales_management_menu(products, addons, orders)
        elif choice == "3":
            print("\n" + "=" * 60)
            print(f"{'Thank you for using Beautiful Blooms!':^60}")
            print(f"{'Goodbye!':^60}")
            print("=" * 60)
            break


if __name__ == "__main__":
    main()