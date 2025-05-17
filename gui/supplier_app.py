# gui/supplier_app.py
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from models.supplier import Supplier
from database.db_manager import DatabaseManager

class SupplierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Suppliers")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f4f8")

        # Initialize database
        self.db = DatabaseManager()

        # Fonts and colors
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
        self.bg_color = "#f0f4f8"
        self.accent_color = "#4a90e2"
        self.button_color = "#2ecc71"
        self.delete_color = "#e74c3c"

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(self.main_frame, text="Manage Suppliers", font=self.title_font, background=self.bg_color).pack(pady=10)

        # Input frame
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill="x", pady=10)

        # Labels and Entries
        labels = ["Supplier Name", "Contact", "Address"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(self.input_frame, text=label, font=self.label_font).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.input_frame, font=self.label_font, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        # Buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", pady=10)

        buttons = [
            ("Add Supplier", self.add_supplier, self.button_color),
            ("Update Supplier", self.update_supplier, self.accent_color),
            ("Delete Supplier", self.delete_supplier, self.delete_color),
            ("Clear Fields", self.clear_fields, "#7f8c8d")
        ]
        for text, command, color in buttons:
            btn = tk.Button(self.button_frame, text=text, command=command, font=self.button_font,
                            bg=color, fg="white", relief="flat", width=12)
            btn.pack(side="left", padx=5)

        # Treeview for suppliers display
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill="both", expand=True, pady=10)

        columns = ("ID", "Name", "Contact", "Address")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Load suppliers
        self.load_suppliers()

    def load_suppliers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        suppliers = self.db.fetch_suppliers()
        for supplier in suppliers:
            self.tree.insert("", "end", values=supplier)

    def add_supplier(self):
        supplier = Supplier(
            name=self.entries["Supplier Name"].get(),
            contact=self.entries["Contact"].get(),
            address=self.entries["Address"].get()
        )

        is_valid, error_message = supplier.validate()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        if self.db.add_supplier(supplier):
            self.load_suppliers()
            self.clear_fields()
            messagebox.showinfo("Success", "Supplier added successfully!")

    def update_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a supplier to update!")
            return

        supplier = Supplier(
            id=self.tree.item(selected)["values"][0],
            name=self.entries["Supplier Name"].get(),
            contact=self.entries["Contact"].get(),
            address=self.entries["Address"].get()
        )

        is_valid, error_message = supplier.validate()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        if self.db.update_supplier(supplier):
            self.load_suppliers()
            self.clear_fields()
            messagebox.showinfo("Success", "Supplier updated successfully!")

    def delete_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a supplier to delete!")
            return

        id = self.tree.item(selected)["values"][0]
        if self.db.delete_supplier(id):
            self.load_suppliers()
            self.clear_fields()
            messagebox.showinfo("Success", "Supplier deleted successfully!")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected)["values"]
            self.entries["Supplier Name"].delete(0, "end")
            self.entries["Supplier Name"].insert(0, values[1])
            self.entries["Contact"].delete(0, "end")
            self.entries["Contact"].insert(0, values[2])
            self.entries["Address"].delete(0, "end")
            self.entries["Address"].insert(0, values[3])