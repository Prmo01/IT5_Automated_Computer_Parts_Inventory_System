# gui/order_app.py
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import mysql.connector
from models.order import Order
from database.db_manager import DatabaseManager

class OrderApp:
    def __init__(self, root, create_mode=True, user=None, on_data_change=None):
        # Initialize window
        self.root = root
        self.root.title("Manage Orders")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f4f8")
        self.create_mode = create_mode
        self.user = user
        self.on_data_change = on_data_change  # Callback for data changes

        # Initialize database
        self.db = DatabaseManager()

        # Define fonts and colors
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
        self.bg_color = "#f0f4f8"
        self.accent_color = "#4a90e2"
        self.button_color = "#2ecc71"

        # Fetch parts and suppliers
        self.parts = self.db.fetch_parts()  # List of (id, name, category, quantity, price)
        self.suppliers = self.db.fetch_suppliers()
        self.temp_items = []  # Temporary list for items in the current order

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        title = "Create Order" if self.create_mode else "View Orders"
        ttk.Label(self.main_frame, text=title, font=self.title_font, background=self.bg_color).pack(pady=10)

        # Create order form (visible in create mode)
        if self.create_mode:
            # Input frame for supplier, part, and quantity
            self.input_frame = ttk.Frame(self.main_frame)
            self.input_frame.pack(fill="x", pady=10)

            # Supplier selection
            ttk.Label(self.input_frame, text="Select Supplier", font=self.label_font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
            self.supplier_var = tk.StringVar()
            supplier_names = [f"{s[1]} (ID: {s[0]})" for s in self.suppliers]
            self.supplier_menu = ttk.Combobox(self.input_frame, textvariable=self.supplier_var, values=supplier_names, state="readonly")
            self.supplier_menu.grid(row=0, column=1, padx=5, pady=16)

            # Part selection
            ttk.Label(self.input_frame, text="Select Part", font=self.label_font).grid(row=1, column=0, padx=5, pady=5, sticky="e")
            self.part_var = tk.StringVar()
            part_names = [f"{p[1]} (ID: {p[0]})" for p in self.parts]
            self.part_menu = ttk.Combobox(self.input_frame, textvariable=self.part_var, values=part_names, state="readonly")
            self.part_menu.grid(row=1, column=1, padx=5, pady=5)

            # Quantity input
            ttk.Label(self.input_frame, text="Quantity", font=self.label_font).grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.quantity_entry = ttk.Entry(self.input_frame, font=self.label_font)
            self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

            # Buttons for adding items and placing order
            self.button_frame = ttk.Frame(self.main_frame)
            self.button_frame.pack(fill="x", pady=10)

            tk.Button(self.button_frame, text="Add Item", command=self.add_item,
                      font=self.button_font, bg=self.accent_color, fg="white", relief="flat", width=12).pack(side="left", padx=5)
            tk.Button(self.button_frame, text="Place Order", command=self.place_order,
                      font=self.button_font, bg=self.button_color, fg="white", relief="flat", width=12).pack(side="left", padx=5)
            tk.Button(self.button_frame, text="Clear Items", command=self.clear_items,
                      font=self.button_font, bg="#e74c3c", fg="white", relief="flat", width=12).pack(side="left", padx=5)

            # Temporary items Treeview (shows items before placing order)
            self.temp_tree_frame = ttk.Frame(self.main_frame)
            self.temp_tree_frame.pack(fill="x", pady=10)
            self.temp_tree = ttk.Treeview(self.temp_tree_frame, columns=("Part Name", "Quantity"), show="headings", height=3)
            self.temp_tree.heading("Part Name", text="Part Name")
            self.temp_tree.heading("Quantity", text="Quantity")
            self.temp_tree.column("Part Name", width=300, anchor="w")
            self.temp_tree.column("Quantity", width=100, anchor="center")
            self.temp_tree.pack(fill="x")

        # Orders Treeview (shows all orders)
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill="both", expand=True, pady=10)

        columns = ("Order ID", "Supplier Name", "Order Date", "Status", "Items")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=10)
        self.tree.heading("Order ID", text="Order ID")
        self.tree.heading("Supplier Name", text="Supplier Name")
        self.tree.heading("Order Date", text="Order Date")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Items", text="Items")
        self.tree.column("Order ID", width=100, anchor="center")
        self.tree.column("Supplier Name", width=150, anchor="center")
        self.tree.column("Order Date", width=150, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Items", width=300, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar for orders Treeview
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Status update buttons (visible in view mode for logged-in users)
        if not self.create_mode and self.user is not None:
            self.status_frame = ttk.Frame(self.main_frame)
            self.status_frame.pack(fill="x", pady=5)
            tk.Button(self.status_frame, text="Mark Completed", command=self.mark_completed,
                      font=self.button_font, bg=self.button_color, fg="white", relief="flat", width=15).pack(side="left", padx=5)
            tk.Button(self.status_frame, text="Cancel Order", command=self.cancel_order,
                      font=self.button_font, bg="#e74c3c", fg="white", relief="flat", width=15).pack(side="left", padx=5)
            tk.Button(self.status_frame, text="View Details", command=self.view_details,
                      font=self.button_font, bg=self.accent_color, fg="white", relief="flat", width=15).pack(side="left", padx=5)

        # Load orders into Treeview
        self.load_orders()

    def add_item(self):
        try:
            part_id = int(self.part_var.get().split("ID: ")[-1].strip(")"))
            quantity = int(self.quantity_entry.get())
            part = next(p for p in self.parts if p[0] == part_id)
            part_name = part[1]
            available_qty = part[3]  # parts tuple: (id, name, category, quantity, price)
            part_price = part[4]
        except (ValueError, StopIteration):
            messagebox.showerror("Error", "Please select a part and enter a valid quantity!")
            return

        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be positive!")
            return
        if quantity > 1000:
            messagebox.showerror("Error", "Quantity too large! Max 1000 per item.")
            return

        # Check for duplicate part and merge quantities
        for item in self.temp_items:
            if item['part_id'] == part_id:
                new_quantity = item['quantity'] + quantity
                if new_quantity > 1000:
                    messagebox.showerror("Error", f"Total quantity for {part_name} exceeds 1000!")
                    return
                item['quantity'] = new_quantity
                # Update Treeview
                for tree_item in self.temp_tree.get_children():
                    if self.temp_tree.item(tree_item)['values'][0] == part_name:
                        self.temp_tree.item(tree_item, values=(part_name, new_quantity))
                        break
                self.quantity_entry.delete(0, "end")
                return

        # Add new item to temporary list
        self.temp_items.append({
            'part_id': part_id,
            'quantity': quantity,
            'price': part_price
        })
        self.temp_tree.insert("", "end", values=(part_name, quantity))
        self.quantity_entry.delete(0, "end")

    def clear_items(self):
        # Clear temporary items list and Treeview
        self.temp_items.clear()
        for item in self.temp_tree.get_children():
            self.temp_tree.delete(item)

    def load_orders(self):
        # Clear existing Treeview entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch orders with items
        orders = self.db.fetch_orders_with_items()
        for order in orders:
            order_id, supplier_name, order_date, status, items = order
            # Truncate items display for readability
            if items:
                items_str = f"{items[0]['part_name']} (Qty: {items[0]['quantity']})"
                if len(items) > 1:
                    items_str += f", +{len(items)-1} more..."
            else:
                items_str = "No items"
            self.tree.insert("", "end", values=(order_id, supplier_name, order_date, status, items_str))

    def view_details(self):
        # Get selected order
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an order to view details!")
            return

        # Fetch order details
        order_id = self.tree.item(selected)["values"][0]
        orders = self.db.fetch_orders_with_items()
        order = next((o for o in orders if o[0] == order_id), None)
        if not order:
            messagebox.showerror("Error", f"Order #{order_id} not found!")
            return

        print(f"Debug - Selected order: {order}")
        if not order[4]:
            messagebox.showerror("Error", f"No items found for order #{order_id}!")
            return

        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Order #{order_id} Details")
        popup.geometry("600x400")
        popup.configure(bg="#f0f4f8")

        # Main frame for popup
        popup_frame = ttk.Frame(popup, padding=20)
        popup_frame.pack(fill="both", expand=True)

        # Order summary
        summary = f"Order #{order_id}\nSupplier: {order[1]}\nDate: {order[2]}\nStatus: {order[3]}"
        ttk.Label(popup_frame, text=summary, font=self.label_font, background="#f0f4f8").pack(anchor="w", pady=10)

        # Items Treeview in popup
        columns = ("Part Name", "Quantity", "Unit Price", "Total Price")
        details_tree = ttk.Treeview(popup_frame, columns=columns, show="headings", height=8)
        details_tree.heading("Part Name", text="Part Name")
        details_tree.heading("Quantity", text="Quantity")
        details_tree.heading("Unit Price", text="Unit Price")
        details_tree.heading("Total Price", text="Total Price")
        details_tree.column("Part Name", width=200, anchor="w")
        details_tree.column("Quantity", width=100, anchor="center")
        details_tree.column("Unit Price", width=100, anchor="center")
        details_tree.column("Total Price", width=150, anchor="center")
        details_tree.pack(fill="both", expand=True, pady=5)

        # Populate items
        total_cost = 0
        for item in order[4]:
            if 'part_name' not in item or 'quantity' not in item:
                print(f"Debug - Invalid item data: {item}")
                continue
            part_name = item['part_name']
            quantity = int(item.get('quantity', 0))
            price = float(item.get('price', next((p[4] for p in self.parts if p[1] == part_name), 0.0)))
            total_price = price * quantity
            total_cost += total_price
            details_tree.insert("", "end", values=(
                part_name,
                quantity,
                f"${price:.2f}",
                f"${total_price:.2f}"
            ))

        # Total cost label
        ttk.Label(popup_frame, text=f"Total Cost: ${total_cost:.2f}", font=self.label_font,
                  background="#f0f4f8").pack(anchor="w", pady=5)

        # Close button
        tk.Button(popup_frame, text="Close", command=popup.destroy,
                  font=self.button_font, bg="#e74c3c", fg="white", relief="flat", width=10).pack(pady=10)

    def place_order(self):
        if not self.temp_items:
            messagebox.showerror("Error", "Add at least one item to the order!")
            return

        try:
            supplier_id = int(self.supplier_var.get().split("ID: ")[-1].strip(")"))
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Please select a supplier!")
            return

        # Check total quantity
        total_quantity = sum(item['quantity'] for item in self.temp_items)
        if total_quantity > 5000:
            messagebox.showerror("Error", "Total quantity exceeds maximum order limit of 5000!")
            return

        # Calculate total cost
        total_cost = sum(item['quantity'] * item['price'] for item in self.temp_items)

        # Create and validate order
        order = Order(supplier_id=supplier_id, items=self.temp_items)
        is_valid, error_message = order.validate()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        # Confirmation dialog
        items_str = "\n".join([f"- {self.db.get_part_name(item['part_id'])}: {item['quantity']} units (${item['quantity'] * item['price']:.2f})" for item in self.temp_items])
        confirm_message = (
            f"Place order from {self.supplier_var.get()} on {order.order_date.strftime('%Y-%m-%d %H:%M:%S')}?\n\n"
            f"Items:\n{items_str}\n\n"
            f"Total Quantity: {total_quantity}\n"
            f"Total Cost: ${total_cost:.2f}"
        )
        if messagebox.askyesno("Confirm Order", confirm_message):
            try:
                user_id = self.user.id if self.user else None
                if self.db.create_order(order, user_id=user_id):
                    self.load_orders()
                    self.clear_items()
                    self.supplier_var.set("")
                    messagebox.showinfo("Success", "Order placed successfully!")
                    if self.on_data_change:
                        self.on_data_change()  # Trigger dashboard refresh
                else:
                    messagebox.showerror("Error", "Failed to place order!")
            except mysql.connector.Error as e:
                error_msg = str(e)
                if "foreign key constraint" in error_msg.lower():
                    messagebox.showerror("Error", "Invalid supplier or part selected!")
                else:
                    messagebox.showerror("Error", f"Database error: {error_msg}")
            except AttributeError:
                messagebox.showerror("Error", "No user logged in! Please log in to place an order.")

    def mark_completed(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an order to mark as completed!")
            return
        order_id = self.tree.item(selected)["values"][0]
        status = self.tree.item(selected)["values"][3]
        if status != "Pending":
            messagebox.showerror("Error", "Only Pending orders can be marked as Completed!")
            return
        if messagebox.askyesno("Confirm", f"Mark order #{order_id} as Completed?"):
            user_id = self.user.id if self.user else None
            if self.db.update_order_status(order_id, "Completed", user_id):
                self.load_orders()
                messagebox.showinfo("Success", "Order marked as Completed!")
                if self.on_data_change:
                    self.on_data_change()  # Trigger dashboard refresh
            else:
                messagebox.showerror("Error", "Failed to update order status!")

    def cancel_order(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an order to cancel!")
            return
        order_id = self.tree.item(selected)["values"][0]
        status = self.tree.item(selected)["values"][3]
        if status != "Pending":
            messagebox.showerror("Error", "Only Pending orders can be cancelled!")
            return
        if messagebox.askyesno("Confirm", f"Cancel order #{order_id}?"):
            user_id = self.user.id if self.user else None
            if self.db.update_order_status(order_id, "Cancelled", user_id):
                self.load_orders()
                messagebox.showinfo("Success", "Order cancelled!")
                if self.on_data_change:
                    self.on_data_change()  # Trigger dashboard refresh
            else:
                messagebox.showerror("Error", "Failed to cancel order!")