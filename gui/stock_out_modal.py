# gui/stock_out_modal.py
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from datetime import datetime
from database.db_manager import DatabaseManager

class StockOutModal:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.db = DatabaseManager()

        # Create modal window
        self.window = tk.Toplevel(parent)
        self.window.title("Record Stock Out")
        self.window.geometry("450x350")
        self.window.configure(bg="#f0f4f8")
        self.window.transient(parent)  # Make modal
        self.window.grab_set()  # Focus on modal

        # Fonts and colors
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
        self.bg_color = "#f0f4f8"
        self.accent_color = "#4a90e2"
        self.button_color = "#2ecc71"
        self.cancel_color = "#e74c3c"
        self.input_bg = "#ffffff"

        # Configure ttk style for inputs
        style = ttk.Style()
        style.configure("Custom.TEntry", fieldbackground=self.input_bg, background=self.bg_color, padding=5)
        style.configure("Custom.TCombobox", fieldbackground=self.input_bg, background=self.bg_color, padding=5)

        # Main frame with padding
        self.main_frame = ttk.Frame(self.window, padding="20 20 20 20", style="Custom.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(self.main_frame, text="Record Stock Out", font=self.title_font, background=self.bg_color).pack(pady=(0, 15))

        # Input frame for better organization
        self.input_frame = ttk.Frame(self.main_frame, padding="0 10", style="Custom.TFrame")
        self.input_frame.pack(fill="x")

        # Part selection
        ttk.Label(self.input_frame, text="Item:", font=self.label_font, background=self.bg_color).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.part_combobox = ttk.Combobox(self.input_frame, font=self.label_font, width=30, state="readonly", style="Custom.TCombobox")
        self.part_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.load_parts()

        # Quantity
        ttk.Label(self.input_frame, text="Quantity:", font=self.label_font, background=self.bg_color).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.quantity_entry = ttk.Entry(self.input_frame, font=self.label_font, width=10, style="Custom.TEntry")
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Date
        ttk.Label(self.input_frame, text="Date (YYYY-MM-DD):", font=self.label_font, background=self.bg_color).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = ttk.Entry(self.input_frame, font=self.label_font, width=15, style="Custom.TEntry")
        self.date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Buttons frame with centered alignment
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=20)
        tk.Button(self.button_frame, text="Submit", command=self.submit, font=self.button_font,
                  bg=self.button_color, fg="white", relief="flat", width=12, padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(self.button_frame, text="Cancel", command=self.cancel, font=self.button_font,
                  bg=self.cancel_color, fg="white", relief="flat", width=12, padx=10, pady=5).pack(side="left", padx=5)

    def load_parts(self):
        parts = self.db.fetch_parts_for_stock_out()
        print("Parts fetched for stock out:", parts)  # Debug
        self.part_map = {}  # Maps display text to part_id
        display_texts = []
        for part in parts:
            part_id, name, category, quantity = part
            display_text = f"{name} (Stock: {quantity})"
            self.part_map[display_text] = part_id
            display_texts.append(display_text)
        self.part_combobox['values'] = display_texts
        if not display_texts:
            messagebox.showwarning("No Parts", "No parts available for stock out. Please add parts with quantity > 0 to inventory.")
        elif display_texts:
            self.part_combobox.set(display_texts[0])

    def submit(self):
        try:
            # Get part ID
            display_text = self.part_combobox.get()
            if not display_text:
                messagebox.showerror("Error", "Please select an item!")
                return
            part_id = self.part_map.get(display_text)
            if part_id is None:
                messagebox.showerror("Error", "Invalid item selected!")
                return

            # Get quantity
            quantity_str = self.quantity_entry.get()
            if not quantity_str:
                messagebox.showerror("Error", "Please enter a quantity!")
                return
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive!")
                return

            # Get date
            date_str = self.date_entry.get()
            try:
                processed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
                return

            # Record stock out
            if self.db.add_stock_out(part_id, quantity, processed_date, self.user.id):
                messagebox.showinfo("Success", "Stock out recorded successfully!")
                self.window.destroy()
                # Refresh parent inventory if it's an InventoryApp instance
                if hasattr(self.parent, 'load_parts'):
                    self.parent.load_parts()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def cancel(self):
        self.window.destroy()