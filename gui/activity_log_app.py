import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkcalendar import DateEntry


class ActivityLogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Log - Computer Parts Inventory")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")

        # Define styles and fonts
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.bg_color = "#f0f4f8"
        self.card_bg = "#ffffff"
        self.accent_color = "#4a90e2"

        # Configure ttk styles
        style = ttk.Style()
        style.configure("Card.TFrame", background=self.card_bg, relief="raised")
        style.configure("Card.TLabel", background=self.card_bg)

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        ttk.Label(self.main_frame, text="Activity Log History", font=self.title_font,
                  style="Card.TLabel").pack(anchor="w", pady=(0, 20))

        # Search frame
        search_frame = ttk.Frame(self.main_frame, style="Card.TFrame", padding=10)
        search_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(search_frame, text="Filter by Date:", font=self.label_font,
                  style="Card.TLabel").pack(side="left", padx=(0, 10))

        self.date_entry = DateEntry(search_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2,
                                    date_pattern='yyyy-mm-dd')
        self.date_entry.pack(side="left", padx=(0, 10))

        tk.Button(search_frame, text="Search", command=self.search_activities,
                  font=self.button_font, bg=self.accent_color, fg="white",
                  relief="flat").pack(side="left", padx=(0, 10))

        tk.Button(search_frame, text="Clear Filter", command=self.clear_filter,
                  font=self.button_font, bg=self.accent_color, fg="white",
                  relief="flat").pack(side="left")

        # Treeview for activity log
        columns = ("Date", "Description", "User")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings",
                                 height=15)
        self.tree.pack(fill="both", expand=True, pady=(0, 20))

        # Configure treeview columns
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")
        self.tree.heading("User", text="User")
        self.tree.column("Date", width=150)
        self.tree.column("Description", width=400)
        self.tree.column("User", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical",
                                  command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'inventory_db'
        }
        self.conn = None
        self.connect_db()
        self.load_activities()

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            if self.conn.is_connected():
                print("Successfully connected to the database for ActivityLogApp")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def load_activities(self, date_filter=None):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.conn:
            print("No database connection for activity log")
            return

        try:
            cursor = self.conn.cursor()
            if date_filter:
                query = """
                    SELECT a.description, a.created_at, u.username
                    FROM activity_log a
                    LEFT JOIN users u ON a.user_id = u.id
                    WHERE DATE(a.created_at) = %s
                    ORDER BY a.created_at DESC
                """
                cursor.execute(query, (date_filter,))
            else:
                query = """
                    SELECT a.description, a.created_at, u.username
                    FROM activity_log a
                    LEFT JOIN users u ON a.user_id = u.id
                    ORDER BY a.created_at DESC
                """
                cursor.execute(query)

            for row in cursor.fetchall():
                date_str = row[1].strftime('%Y-%m-%d %H:%M:%S')
                self.tree.insert("", "end", values=(date_str, row[0],
                                                    row[2] or "Unknown"))
            cursor.close()
        except Error as e:
            print(f"Error fetching activity log: {e}")

    def search_activities(self):
        selected_date = self.date_entry.get_date().strftime('%Y-%m-%d')
        self.load_activities(selected_date)

    def clear_filter(self):
        self.date_entry.set_date(datetime.now())
        self.load_activities()

    def __del__(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("ActivityLogApp database connection closed.")