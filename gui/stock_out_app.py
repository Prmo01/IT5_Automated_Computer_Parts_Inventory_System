# gui/stock_out_app.py
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from gui.stock_out_modal import StockOutModal
from database.db_manager import DatabaseManager

class StockOutApp:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Stock Out Management")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")
        self.user = user
        self.db = DatabaseManager()

        # Fonts and colors
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
        self.bg_color = "#f0f4f8"
        self.accent_color = "#4a90e2"
        self.button_color = "#2ecc71"

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(self.main_frame, text="Stock Out History", font=self.title_font, background=self.bg_color).pack(pady=10)

        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", pady=10)
        tk.Button(self.button_frame, text="Stock Out Part", command=self.open_stock_out_modal, font=self.button_font,
                  bg=self.button_color, fg="white", relief="flat", width=15).pack(side="left", padx=5)

        # Treeview for stock out history
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill="both", expand=True, pady=10)

        columns = ("ID", "Part Name", "Quantity", "Date", "User")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Load stock out history
        self.load_stock_outs()

    def load_stock_outs(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        stock_outs = self.db.fetch_stock_outs()
        for stock_out in stock_outs:

            stock_out_id, part_name, quantity, processed_date, username = stock_out
            date_str = processed_date.strftime("%Y-%m-%d") if processed_date else "N/A"
            username_str = username if username else "Unknown"
            self.tree.insert("", "end", values=(stock_out_id, part_name, quantity, date_str, username_str))

    def open_stock_out_modal(self):
        StockOutModal(self.root, self.user)

        self.load_stock_outs()