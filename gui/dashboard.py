import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from gui.inventory_app import InventoryApp
from gui.supplier_app import SupplierApp
from gui.order_app import OrderApp
from gui.category_app import CategoryApp
from gui.stock_out_app import StockOutApp
from gui.activity_log_app import ActivityLogApp
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from PIL import Image, ImageTk

class Dashboard:
    def __init__(self, root, user=None, on_logout=None):
        # Initialize window
        self.root = root
        self.root.title("Computer Parts Inventory")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f4f8")
        self.user = user
        self.on_logout = on_logout

        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'inventory_db'
        }
        self.conn = None
        self.low_stock_threshold = 10
        self.connect_db()

        # If no user is logged in, show login screen; otherwise, show dashboard
        if not self.user:
            self.show_login_screen()
        else:
            self.show_dashboard()

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            if self.conn.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def show_login_screen(self):
        # Clear existing content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set title for login screen
        self.root.title("Login - Computer Parts Inventory")

        # Main frame for login
        self.login_frame = ttk.Frame(self.root, padding=20)
        self.login_frame.pack(fill="both", expand=True)

        # Define fonts
        self.title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Title
        ttk.Label(self.login_frame, text="Login", font=self.title_font).pack(pady=20)

        # Username
        ttk.Label(self.login_frame, text="Username", font=self.label_font).pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame, font=self.label_font)
        self.username_entry.pack(pady=5)

        # Password
        ttk.Label(self.login_frame, text="Password", font=self.label_font).pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, font=self.label_font, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        tk.Button(self.login_frame, text="Login", command=self.handle_login,
                  font=self.button_font, bg="#4a90e2", fg="white", relief="flat", width=15).pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return

        if not self.conn or not self.conn.is_connected():
            messagebox.showerror("Error", "No database connection!")
            return

        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT id, username, role FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user_data = cursor.fetchone()
            cursor.close()

            if user_data:
                # Create user object (assuming user has id, username, role, and is_admin method)
                class User:
                    def __init__(self, id, username, role):
                        self.id = id
                        self.username = username
                        self.role = role

                    def is_admin(self):
                        return self.role.lower() == "admin"

                self.user = User(user_data['id'], user_data['username'], user_data['role'])
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        except Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def show_dashboard(self):
        # Clear existing content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reset title
        self.root.title("Dashboard - Computer Parts Inventory")

        # Define styles and fonts
        self.title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.card_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.bg_color = "#f0f4f8"
        self.card_bg = "#ffffff"
        self.nav_bg = "#2c3e50"
        self.accent_color = "#4a90e2"
        self.logout_color = "#e74c3c"
        self.nav_hover = "#34495e"

        # Configure ttk styles
        style = ttk.Style()
        style.configure("Card.TFrame", background=self.card_bg, relief="raised")
        style.configure("Card.TLabel", background=self.card_bg)
        style.configure("Header.TFrame", background=self.bg_color)
        style.configure("Header.TLabel", background=self.bg_color)
        style.configure("Hover.TFrame", background="#f8f9fa")
        style.configure("Hover.TLabel", background="#f8f9fa")

        # Main layout
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Navigation sidebar
        self.nav_frame = tk.Frame(self.main_frame, bg=self.nav_bg, width=200)
        self.nav_frame.pack(side="left", fill="y")

        # Load and display logo at the top of the nav frame
        try:
            logo_img = Image.open("images/logo.png")
            logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.nav_frame, image=self.logo_photo, bg=self.nav_bg)
            logo_label.pack(pady=10, padx=10, anchor="center")
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = tk.Label(self.nav_frame, text="Logo Not Found", bg=self.nav_bg, fg="white", font=self.label_font)
            logo_label.pack(pady=10, padx=10, anchor="center")

        # Title below logo
        tk.Label(self.nav_frame, text="MENU", font=self.title_font, bg=self.nav_bg, fg="white").pack(pady=(0, 20), padx=10, anchor="w")

        # Navigation buttons
        nav_buttons = [
            ("View Parts", self.view_parts),
            ("Manage Inventory", self.manage_inventory),
            ("View Orders", self.view_orders),
            ("Create Order", self.create_order),
            ("Stock Out", self.stock_out),
        ]
        if self.user.is_admin():
            nav_buttons.extend([
                ("Activity Log", self.view_activity_log),
                ("Manage Suppliers", self.manage_suppliers),
                ("Manage Categories", self.manage_categories),
            ])
        nav_buttons.append(("Logout", self.logout))

        for text, command in nav_buttons:
            btn_color = self.logout_color if text == "Logout" else self.accent_color
            btn = tk.Button(self.nav_frame, text=text, command=command, font=self.button_font,
                           bg=btn_color, fg="white", relief="flat", width=15)
            btn.pack(pady=5, padx=10, anchor="w")
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.nav_hover))
            btn.bind("<Leave>", lambda e, b=btn, c=btn_color: b.configure(bg=c))

        # Content area
        self.content_frame = ttk.Frame(self.main_frame, style="Header.TFrame")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header with Welcome message
        self.header_frame = ttk.Frame(self.content_frame, style="Header.TFrame")
        self.header_frame.pack(fill="x", pady=(0, 20))
        self.header_label = ttk.Label(self.header_frame, text=f"Welcome, {self.user.username} ({self.user.role})!",
                                     font=self.title_font, style="Header.TLabel")
        self.header_label.pack(side="left", padx=10)

        # Cards layout
        self.cards_frame = ttk.Frame(self.content_frame)
        self.cards_frame.pack(fill="both", expand=True)

        # Initialize cards
        self.refresh_dashboard()

    def refresh_dashboard(self):
        # Clear existing cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Fetch dashboard data
        total_parts = self.get_total_parts()
        low_stock = self.get_low_stock()
        total_categories = self.get_total_categories()
        pending_orders = self.get_pending_orders()
        suppliers = self.get_suppliers()
        if self.user.is_admin():
            recent_activities = self.get_recent_activities()
        else:
            recent_activities = None

        # Card 1: Total Parts
        total_parts_frame = ttk.Frame(self.cards_frame, style="Card.TFrame", padding=20)
        total_parts_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        total_parts_frame.bind("<Enter>", lambda e: total_parts_frame.configure(style="Hover.TFrame"))
        total_parts_frame.bind("<Leave>", lambda e: total_parts_frame.configure(style="Card.TFrame"))
        ttk.Label(total_parts_frame, text="Total Parts", font=self.card_font, style="Card.TLabel").pack(anchor="w")
        ttk.Label(total_parts_frame, text=f"{total_parts}", font=self.label_font, style="Card.TLabel").pack(anchor="w", pady=5)
        tk.Button(total_parts_frame, text="View", command=self.view_parts, font=self.button_font,
                 bg=self.accent_color, fg="white", relief="flat").pack(anchor="w", pady=5)

        # Card 2: Low Stock
        low_stock_frame = ttk.Frame(self.cards_frame, style="Card.TFrame", padding=20)
        low_stock_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        low_stock_frame.bind("<Enter>", lambda e: low_stock_frame.configure(style="Hover.TFrame"))
        low_stock_frame.bind("<Leave>", lambda e: low_stock_frame.configure(style="Card.TFrame"))
        ttk.Label(low_stock_frame, text="Low Stock", font=self.card_font, style="Card.TLabel").pack(anchor="w")
        ttk.Label(low_stock_frame, text=f"{low_stock} Items", font=self.label_font, style="Card.TLabel").pack(anchor="w", pady=5)
        tk.Button(low_stock_frame, text="Manage Inventory", command=self.manage_inventory, font=self.button_font,
                 bg=self.accent_color, fg="white", relief="flat").pack(anchor="w", pady=5)

        # Card 3: Total Categories
        total_categories_frame = ttk.Frame(self.cards_frame, style="Card.TFrame", padding=20)
        total_categories_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        total_categories_frame.bind("<Enter>", lambda e: total_categories_frame.configure(style="Hover.TFrame"))
        total_categories_frame.bind("<Leave>", lambda e: total_categories_frame.configure(style="Card.TFrame"))
        ttk.Label(total_categories_frame, text="Total Categories", font=self.card_font, style="Card.TLabel").pack(anchor="w")
        ttk.Label(total_categories_frame, text=f"{total_categories}", font=self.label_font, style="Card.TLabel").pack(anchor="w", pady=5)
        tk.Button(total_categories_frame, text="Manage", command=self.manage_categories, font=self.button_font,
                 bg=self.accent_color, fg="white", relief="flat").pack(anchor="w", pady=5)

        # Card 4: Pending Orders
        pending_orders_frame = ttk.Frame(self.cards_frame, style="Card.TFrame", padding=20)
        pending_orders_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        pending_orders_frame.bind("<Enter>", lambda e: pending_orders_frame.configure(style="Hover.TFrame"))
        pending_orders_frame.bind("<Leave>", lambda e: pending_orders_frame.configure(style="Card.TFrame"))
        ttk.Label(pending_orders_frame, text="Pending Orders", font=self.card_font, style="Card.TLabel").pack(anchor="w")
        ttk.Label(pending_orders_frame, text=f"{pending_orders} Orders", font=self.label_font, style="Card.TLabel").pack(anchor="w", pady=5)
        tk.Button(pending_orders_frame, text="View", command=self.view_orders, font=self.button_font,
                 bg=self.accent_color, fg="white", relief="flat").pack(anchor="w", pady=5)

        # Card 5: Suppliers (Admin only)
        if self.user.is_admin():
            suppliers_frame = ttk.Frame(self.cards_frame, style="Card.TFrame", padding=20)
            suppliers_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
            suppliers_frame.bind("<Enter>", lambda e: suppliers_frame.configure(style="Hover.TFrame"))
            suppliers_frame.bind("<Leave>", lambda e: suppliers_frame.configure(style="Card.TFrame"))
            ttk.Label(suppliers_frame, text="Suppliers", font=self.card_font, style="Card.TLabel").pack(anchor="w")
            ttk.Label(suppliers_frame, text=f"{suppliers} Active", font=self.label_font, style="Card.TLabel").pack(anchor="w", pady=5)
            tk.Button(suppliers_frame, text="Manage", command=self.manage_suppliers, font=self.button_font,
                     bg=self.accent_color, fg="white", relief="flat").pack(anchor="w", pady=5)

        # Card 6: Recent Activity (Admin only)
        if self.user.is_admin() and recent_activities:
            recent_activity_frame = ttk.Frame(self.cards_frame, style="Card.TFrame", padding=20)
            recent_activity_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
            recent_activity_frame.bind("<Enter>", lambda e: recent_activity_frame.configure(style="Hover.TFrame"))
            recent_activity_frame.bind("<Leave>", lambda e: recent_activity_frame.configure(style="Card.TFrame"))
            ttk.Label(recent_activity_frame, text="Recent Activity", font=self.card_font, style="Card.TLabel").pack(anchor="w")
            activity_list = tk.Listbox(recent_activity_frame, font=self.label_font, height=5, width=50,
                                      relief="flat", bg=self.card_bg)
            activity_list.pack(anchor="w", pady=5)
            for activity in recent_activities:
                activity_list.insert(tk.END, activity)

        # Configure grid weights
        self.cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        # Adjust row weights based on admin status
        if self.user.is_admin():
            self.cards_frame.grid_rowconfigure((0, 1, 2), weight=1)
        else:
            self.cards_frame.grid_rowconfigure((0, 1), weight=1)

    def get_total_parts(self):
        if not self.conn:
            print("No database connection for total parts")
            return "N/A"
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM parts")
            result = cursor.fetchone()
            cursor.close()
            count = result[0] if result else 0
            print(f"Total parts: {count}")
            return count
        except Error as e:
            print(f"Error fetching total parts: {e}")
            return "N/A"

    def get_low_stock(self):
        if not self.conn:
            print("No database connection for low stock")
            return "N/A"
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM parts WHERE quantity <= {self.low_stock_threshold}")
            result = cursor.fetchone()
            cursor.close()
            count = result[0] if result else 0
            print(f"Low stock items: {count}")
            return count
        except Error as e:
            print(f"Error fetching low stock: {e}")
            return "N/A"

    def get_total_categories(self):
        if not self.conn:
            print("No database connection for total categories")
            return "N/A"
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM categories")
            result = cursor.fetchone()
            cursor.close()
            count = result[0] if result else 0
            print(f"Total categories: {count}")
            return count
        except Error as e:
            print(f"Error fetching total categories: {e}")
            return "N/A"

    def get_pending_orders(self):
        if not self.conn:
            print("No database connection for pending orders")
            return "N/A"
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Pending'")
            result = cursor.fetchone()
            count = result[0] if result else 0
            cursor.execute("SELECT id, order_date, status, supplier_id FROM orders WHERE status = 'Pending'")
            orders = cursor.fetchall()
            print(f"Pending orders: {count}")
            print(f"Pending orders details: {orders}")
            cursor.close()
            return count
        except Error as e:
            print(f"Error fetching pending orders: {e}")
            return "N/A"

    def get_suppliers(self):
        if not self.conn:
            print("No database connection for suppliers")
            return "N/A"
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM suppliers")
            result = cursor.fetchone()
            cursor.close()
            count = result[0] if result else 0
            print(f"Suppliers: {count}")
            return count
        except Error as e:
            print(f"Error fetching suppliers: {e}")
            return "N/A"

    def get_recent_activities(self):
        if not self.conn:
            print("No database connection for recent activities")
            return ["No activities available"]
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT a.description, a.created_at, u.username
                FROM activity_log a
                LEFT JOIN users u ON a.user_id = u.id
                ORDER BY a.created_at DESC
                LIMIT 5
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            activities = [
                f"{row[1].strftime('%Y-%m-%d %H:%M:%S')}: {row[0]} by {row[2] or 'Unknown'}"
                for row in results
            ]
            print(f"Recent activities: {activities}")
            return activities if activities else ["No recent activities"]
        except Error as e:
            print(f"Error fetching recent activities curva: {e}")
            return ["Error loading activities"]

    def view_parts(self):
        inventory_window = tk.Toplevel(self.root)
        InventoryApp(inventory_window, self.user, view_only=True)
        inventory_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(inventory_window))

    def manage_inventory(self):
        inventory_window = tk.Toplevel(self.root)
        InventoryApp(inventory_window, self.user, view_only=not self.user.is_admin())
        inventory_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(inventory_window))

    def manage_suppliers(self):
        supplier_window = tk.Toplevel(self.root)
        SupplierApp(supplier_window)
        supplier_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(supplier_window))

    def manage_categories(self):
        category_window = tk.Toplevel(self.root)
        CategoryApp(category_window)
        category_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(category_window))

    def create_order(self):
        order_window = tk.Toplevel(self.root)
        OrderApp(order_window, create_mode=True, user=self.user)
        order_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(order_window))

    def view_orders(self):
        order_window = tk.Toplevel(self.root)
        OrderApp(order_window, create_mode=False, user=self.user)
        order_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(order_window))

    def stock_out(self):
        stock_out_window = tk.Toplevel(self.root)
        StockOutApp(stock_out_window, self.user)
        stock_out_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(stock_out_window))

    def view_activity_log(self):
        activity_log_window = tk.Toplevel(self.root)
        ActivityLogApp(activity_log_window)
        activity_log_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(activity_log_window))

    def on_window_close(self, window):
        window.destroy()
        self.refresh_dashboard()

    def logout(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Database connection closed.")
        if self.on_logout:
            self.on_logout()
        self.user = None
        self.show_login_screen()