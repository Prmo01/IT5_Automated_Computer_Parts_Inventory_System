# database/db_manager.py
import mysql.connector
from config.db_config import get_db_config
from tkinter import messagebox
from models.user import User
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.config = get_db_config()
        self.conn = None
        self.cursor = None
        self.connect()
        self.ensure_stock_outs_table()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            self.conn.autocommit = False
            self.cursor.execute(f"USE {self.config['database']}")
            print(f"Database connection established successfully to {self.config['database']}. Autocommit: {self.conn.autocommit}")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT PRIMARY KEY, test_value VARCHAR(50))")
            self.cursor.execute("INSERT INTO test_table (test_value) VALUES ('test')")
            self.conn.commit()
            self.cursor.execute("DROP TABLE test_table")
            print("Write test passed.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to MySQL: {e}")
            self.conn = None
            self.cursor = None
            print(f"Connection failed: {e}")
            raise

    def ensure_stock_outs_table(self):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_outs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    part_id INT NOT NULL,
                    quantity INT NOT NULL,
                    processed_date DATE NOT NULL,
                    user_id INT,
                    FOREIGN KEY (part_id) REFERENCES parts(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                    CONSTRAINT positive_quantity CHECK (quantity > 0)
                )
            """)
            self.conn.commit()
            print("Stock outs table ensured.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to create stock_outs table: {e}")
            self.conn.rollback()
            raise

    def authenticate_user(self, username, password):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("SELECT id, username, password, role FROM users WHERE username = %s", (username,))
            result = self.cursor.fetchone()
            if result:
                user = User(id=result[0], username=result[1], password=result[2], role=result[3])
                if user.verify_password(password):
                    return user
            return None
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Authentication failed: {e}")
            return None

    def fetch_category_names(self):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("SELECT id, name FROM categories ORDER BY name")
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch category names: {e}")
            return []

    def add_part(self, part):
        if not self.conn:
            self.connect()
        try:
            query = "INSERT INTO parts (name, category_id, quantity, price) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (part.name, part.category_id, part.quantity, part.price))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to add part: {e}")
            self.conn.rollback()
            return False

    def fetch_parts(self, search_query="", category_id=None):
        if not self.conn:
            self.connect()
        try:
            query = """
                SELECT p.id, p.name, c.name, p.quantity, p.price 
                FROM parts p
                JOIN categories c ON p.category_id = c.id
                WHERE (p.name LIKE %s OR c.name LIKE %s)
            """
            params = (f"%{search_query}%", f"%{search_query}%")
            if category_id is not None:
                query += " AND p.category_id = %s"
                params += (category_id,)
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch parts: {e}")
            return []

    def fetch_parts_for_stock_out(self):
        if not self.conn:
            self.connect()
        try:
            query = """
                SELECT p.id, p.name, c.name, p.quantity
                FROM parts p
                JOIN categories c ON p.category_id = c.id
                WHERE p.quantity > 0
                ORDER BY p.name
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()  # Returns (id, name, category_name, quantity)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch parts for stock out: {e}")
            return []

    def add_stock_out(self, part_id, quantity, processed_date, user_id=None):
        if not self.conn:
            self.connect()
        try:
            # Validate quantity against current stock
            self.cursor.execute("SELECT quantity FROM parts WHERE id = %s", (part_id,))
            result = self.cursor.fetchone()
            if not result:
                raise ValueError("Part does not exist.")
            current_quantity = result[0]
            if quantity > current_quantity:
                raise ValueError(f"Stock out quantity ({quantity}) exceeds current stock ({current_quantity}).")

            # Insert stock out record
            query = "INSERT INTO stock_outs (part_id, quantity, processed_date, user_id) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (part_id, quantity, processed_date, user_id))

            # Update part quantity
            new_quantity = current_quantity - quantity
            self.cursor.execute("UPDATE parts SET quantity = %s WHERE id = %s", (new_quantity, part_id))

            # Log activity
            self.cursor.execute("SELECT name FROM parts WHERE id = %s", (part_id,))
            part_name = self.cursor.fetchone()[0]
            self.log_activity(f"Stock out: {quantity} of {part_name}", user_id)

            self.conn.commit()
            return True
        except (mysql.connector.Error, ValueError) as e:
            messagebox.showerror("Database Error", f"Failed to record stock out: {str(e)}")
            self.conn.rollback()
            return False

    def fetch_stock_outs(self):
        if not self.conn:
            self.connect()
        try:
            query = """
                SELECT s.id, p.name, s.quantity, s.processed_date, u.username
                FROM stock_outs s
                JOIN parts p ON s.part_id = p.id
                LEFT JOIN users u ON s.user_id = u.id
                ORDER BY s.processed_date DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()  # Returns (id, part_name, quantity, processed_date, username)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch stock outs: {e}")
            return []

    def update_part(self, part):
        if not self.conn:
            self.connect()
        try:
            query = "UPDATE parts SET name = %s, category_id = %s, quantity = %s, price = %s WHERE id = %s"
            self.cursor.execute(query, (part.name, part.category_id, part.quantity, part.price, part.id))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to update part: {e}")
            self.conn.rollback()
            return False

    def delete_part(self, id):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("SELECT COUNT(*) FROM order_items WHERE part_id = %s", (id,))
            if self.cursor.fetchone()[0] > 0:
                response = messagebox.askyesno("Confirm Deletion",
                                               "This part is referenced in an order. Delete related order items and the part?")
                if response:
                    self.cursor.execute("DELETE FROM order_items WHERE part_id = %s", (id,))
                else:
                    return False
            self.cursor.execute("DELETE FROM parts WHERE id = %s", (id,))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete part: {e}")
            self.conn.rollback()
            return False

    def update_inventory_level(self, part_id, quantity):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("UPDATE parts SET quantity = %s WHERE id = %s", (quantity, part_id))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to update inventory: {e}")
            return False

    def add_supplier(self, supplier):
        if not self.conn:
            self.connect()
        try:
            query = "INSERT INTO suppliers (name, contact, address) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (supplier.name, supplier.contact, supplier.address))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to add supplier: {e}")
            self.conn.rollback()
            return False

    def fetch_suppliers(self):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("SELECT id, name, contact, address FROM suppliers")
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch suppliers: {e}")
            return []

    def update_supplier(self, supplier):
        if not self.conn:
            self.connect()
        try:
            query = "UPDATE suppliers SET name = %s, contact = %s, address = %s WHERE id = %s"
            self.cursor.execute(query, (supplier.name, supplier.contact, supplier.address, supplier.id))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to update supplier: {e}")
            self.conn.rollback()
            return False

    def delete_supplier(self, id):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("DELETE FROM suppliers WHERE id = %s", (id,))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete supplier: {e}")
            return False

    def fetch_categories(self):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("SELECT id, name, description FROM categories")
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch categories: {e}")
            return []

    def add_category(self, category):
        if not self.conn:
            self.connect()
        try:
            query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
            self.cursor.execute(query, (category.name, category.description))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            if e.errno == 1062:
                messagebox.showerror("Database Error", "Category name already exists!")
            else:
                messagebox.showerror("Database Error", f"Failed to add category: {e}")
            self.conn.rollback()
            return False

    def update_category(self, category):
        if not self.conn:
            self.connect()
        try:
            query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
            self.cursor.execute(query, (category.name, category.description, category.id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            if e.errno == 1062:
                messagebox.showerror("Database Error", "Category name already exists!")
            else:
                messagebox.showerror("Database Error", f"Failed to update category: {e}")
            self.conn.rollback()
            return False

    def delete_category(self, id):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("DELETE FROM categories WHERE id = %s", (id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            if e.errno == 1451:
                messagebox.showerror("Database Error", "Cannot delete category because it is used by parts.")
            else:
                messagebox.showerror("Database Error", f"Failed to delete category: {e}")
            self.conn.rollback()
            return False

    def create_order(self, order, user_id=None):
        if not self.conn:
            self.connect()
        print(f"Attempting to create order with supplier_id={order.supplier_id}, items={order.items}")
        try:
            self.cursor.execute("SELECT COUNT(*) FROM suppliers WHERE id = %s", (order.supplier_id,))
            if self.cursor.fetchone()[0] == 0:
                raise ValueError(f"Invalid supplier_id: {order.supplier_id}")
            print(f"Validated supplier_id={order.supplier_id}")

            for item in order.items:
                self.cursor.execute("SELECT COUNT(*) FROM parts WHERE id = %s", (item['part_id'],))
                if self.cursor.fetchone()[0] == 0:
                    raise ValueError(f"Invalid part_id: {item['part_id']}")
            print(f"Validated all part_ids")

            if not self.conn.is_connected():
                self.conn.ping(reconnect=True)
                if not self.conn.is_connected():
                    raise mysql.connector.Error("Connection lost and could not reconnect.")
            print("Connection is active.")

            query = "INSERT INTO orders (supplier_id, order_date, status) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (order.supplier_id, order.order_date, order.status))
            order_id = self.cursor.lastrowid
            print(f"Order inserted, order_id={order_id}")

            query = "INSERT INTO order_items (order_id, part_id, quantity) VALUES (%s, %s, %s)"
            for item in order.items:
                self.cursor.execute(query, (order_id, item['part_id'], item['quantity']))
                print(f"Added item: part_id={item['part_id']}, quantity={item['quantity']}")

            items_str = ", ".join([f"{self.get_part_name(item['part_id'])} (Qty: {item['quantity']})" for item in order.items if 'part_id' in item and 'quantity' in item])
            self.log_activity(f"Order #{order_id} placed: {items_str}", user_id)
            print(f"Activity logged for order #{order_id}")

            self.conn.commit()
            print("Transaction committed successfully.")
            return True
        except (mysql.connector.Error, ValueError) as e:
            messagebox.showerror("Database Error", f"Failed to create order: {str(e)}")
            print(f"Transaction failed: {str(e)}")
            if self.conn and self.conn.is_connected():
                self.conn.rollback()
                print("Transaction rolled back.")
            return False

    def fetch_orders_with_items(self):
        if not self.conn:
            self.connect()
        try:
            query = """
                SELECT o.id, s.name, o.order_date, o.status
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.id
                ORDER BY o.order_date DESC
            """
            self.cursor.execute(query)
            orders = self.cursor.fetchall()
            result = []
            for order in orders:
                order_id = order[0]
                query = """
                    SELECT p.name, oi.quantity
                    FROM order_items oi
                    JOIN parts p ON oi.part_id = p.id
                    WHERE oi.order_id = %s
                """
                self.cursor.execute(query, (order_id,))
                items = [{'part_name': item[0], 'quantity': item[1]} for item in self.cursor.fetchall()]
                result.append((order_id, order[1], order[2], order[3], items))
            return result
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch orders: {e}")
            return []

    def update_order_status(self, order_id, status, user_id=None):
        if not self.conn:
            self.connect()
        try:
            query = "UPDATE orders SET status = %s WHERE id = %s"
            self.cursor.execute(query, (status, order_id))
            if status == 'Completed':
                query = "SELECT part_id, quantity FROM order_items WHERE order_id = %s"
                self.cursor.execute(query, (order_id,))
                items = self.cursor.fetchall()
                for part_id, quantity in items:
                    query = "SELECT quantity FROM parts WHERE id = %s"
                    self.cursor.execute(query, (part_id,))
                    current_qty = self.cursor.fetchone()[0]
                    self.update_inventory_level(part_id, current_qty + quantity)
            self.log_activity(f"Order #{order_id} status updated to {status}", user_id)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to update order status: {e}")
            self.conn.rollback()
            return False

    def get_part_name(self, part_id):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("SELECT name FROM parts WHERE id = %s", (part_id,))
            result = self.cursor.fetchone()
            return result[0] if result else "Unknown Part"
        except mysql.connector.Error as e:
            print(f"Error fetching part name: {e}")
            return "Unknown Part"

    def get_part(self, part_id):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute("SELECT id, name, quantity, price FROM parts WHERE id = %s", (part_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch part: {e}")
            return None

    def log_activity(self, description, user_id=None):
        if not self.conn:
            self.connect()
        try:
            query = "INSERT INTO activity_log (description, created_at, user_id) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (description, datetime.now(), user_id))
            self.conn.commit()
            print(f"Activity logged: {description}")
        except mysql.connector.Error as e:
            print(f"Error logging activity: {e}")
            raise

    def part_exists(self, name, category_id, exclude_id=None):
        if not self.conn:
            self.connect()
        try:
            query = "SELECT id FROM parts WHERE LOWER(name) = LOWER(%s) AND category_id = %s"
            params = [name, category_id]
            if exclude_id is not None:
                query += " AND id != %s"
                params.append(exclude_id)
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return (True, result[0]) if result else (False, None)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to check part existence: {e}")
            return (False, None)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()