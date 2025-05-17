import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from models.part import Part
from database.db_manager import DatabaseManager

class InventoryApp:
    def __init__(self, root, user, view_only=False, on_data_change=None):
        self.root = root
        self.root.title("Inventory Management")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f4f8")
        self.user = user
        self.view_only = view_only
        self.on_data_change = on_data_change  # Callback for data changes

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
        title = "View Computer Parts" if self.view_only else "Manage Inventory"
        ttk.Label(self.main_frame, text=title, font=self.title_font, background=self.bg_color).pack(pady=10)

        # Search frame
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill="x", pady=5)
        ttk.Label(self.search_frame, text="Search:", font=self.label_font).pack(side="left")
        self.search_entry = ttk.Entry(self.search_frame, font=self.label_font, width=20)
        self.search_entry.pack(side="left", padx=5)
        ttk.Label(self.search_frame, text="Category:", font=self.label_font).pack(side="left", padx=5)
        self.category_search_var = tk.StringVar()
        self.category_search_combobox = ttk.Combobox(self.search_frame, textvariable=self.category_search_var, font=self.label_font, width=15, state="readonly")
        categories = self.db.fetch_category_names()  # [(1, "Electronics"), (2, "Tools")]
        self.category_search_map = {name: id for id, name in categories}  # {"Electronics": 1, "Tools": 2}
        self.category_search_combobox['values'] = ["All Categories"] + list(self.category_search_map.keys())
        self.category_search_combobox.set("All Categories")  # Default to all categories
        self.category_search_combobox.pack(side="left", padx=5)
        tk.Button(self.search_frame, text="Search", command=self.search_parts,
                  font=self.button_font, bg=self.accent_color, fg="white", relief="flat").pack(side="left")

        if not self.view_only:
            # Input frame
            self.input_frame = ttk.Frame(self.main_frame)
            self.input_frame.pack(fill="x", pady=10)

            # Labels and Entries/Combobox
            labels = ["Part Name", "Category", "Price ($)"]
            self.entries = {}
            self.category_map = {}  # To map category names to IDs
            for i, label in enumerate(labels):
                ttk.Label(self.input_frame, text=label, font=self.label_font).grid(row=i, column=0, padx=5, pady=5, sticky="e")
                if label == "Category":
                    # Populate Combobox with categories
                    self.category_combobox = ttk.Combobox(self.input_frame, font=self.label_font, width=22, state="readonly")
                    self.category_map = {name: id for id, name in categories}
                    self.category_combobox['values'] = list(self.category_map.keys())
                    if categories:  # Set default value if categories exist
                        self.category_combobox.set(categories[0][1])  # Default to first category
                    self.category_combobox.grid(row=i, column=1, padx=5, pady=5)
                else:
                    entry = ttk.Entry(self.input_frame, font=self.label_font, width=25)
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    self.entries[label] = entry

            # Buttons frame
            self.button_frame = ttk.Frame(self.main_frame)
            self.button_frame.pack(fill="x", pady=10)

            # Buttons
            buttons = [
                ("Add Part", self.add_part, self.button_color),
                ("Update Part", self.update_part, self.accent_color),
                ("Delete Part", self.delete_part, self.delete_color),
            ]
            for text, command, color in buttons:
                btn = tk.Button(self.button_frame, text=text, command=command, font=self.button_font,
                                bg=color, fg="white", relief="flat", width=12)
                btn.pack(side="left", padx=5)

        # Treeview for parts display
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill="both", expand=True, pady=10)

        columns = ("ID", "Name", "Category", "Quantity", "Price")
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

        # Load parts
        self.load_parts()

    def load_parts(self, search_query="", category_id=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        parts = self.db.fetch_parts(search_query, category_id)
        for part in parts:
            self.tree.insert("", "end", values=part)

    def search_parts(self):
        search_query = self.search_entry.get()
        category_name = self.category_search_var.get()
        category_id = self.category_search_map.get(category_name) if category_name != "All Categories" else None
        self.load_parts(search_query, category_id)

    def add_part(self):
        try:
            category_name = self.category_combobox.get()
            category_id = self.category_map.get(category_name)
            if category_id is None:
                messagebox.showerror("Error", "Please select a valid category!")
                return
            part_name = self.entries["Part Name"].get()
            exists, existing_id = self.db.part_exists(part_name, category_id)
            if exists:
                messagebox.showerror("Error", f"A part with this name and category already exists! (ID: {existing_id})")
                return
            part = Part(
                name=part_name,
                category_id=category_id,
                price=float(self.entries["Price ($)"].get()),
                quantity=0  # Default quantity for new parts
            )
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number!")
            return

        is_valid, error_message = part.validate()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        if self.db.add_part(part):
            self.load_parts()
            self.clear_fields()
            messagebox.showinfo("Success", "Part added successfully!")
            if self.on_data_change:
                self.on_data_change()

    def update_part(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a part to update!")
            return

        try:
            category_name = self.category_combobox.get()
            category_id = self.category_map.get(category_name)
            if category_id is None:
                messagebox.showerror("Error", "Please select a valid category!")
                return
            part = Part(
                id=self.tree.item(selected)["values"][0],
                name=self.entries["Part Name"].get(),
                category_id=category_id,
                price=float(self.entries["Price ($)"].get()),
                quantity=self.tree.item(selected)["values"][3]  # Preserve existing quantity
            )
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number!")
            return

        is_valid, error_message = part.validate()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        if self.db.update_part(part):
            self.load_parts()
            self.clear_fields()
            messagebox.showinfo("Success", "Part updated successfully!")
            if self.on_data_change:
                self.on_data_change()

    def delete_part(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a part to delete!")
            return

        id = self.tree.item(selected)["values"][0]
        if self.db.delete_part(id):
            self.load_parts()
            self.clear_fields()
            messagebox.showinfo("Success", "Part deleted successfully!")
            if self.on_data_change:
                self.on_data_change()

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        if hasattr(self, 'category_combobox'):
            self.category_combobox.set('')  # Clear Combobox selection

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected and not self.view_only:
            values = self.tree.item(selected)["values"]
            self.entries["Part Name"].delete(0, "end")
            self.entries["Part Name"].insert(0, values[1])
            # Set Combobox to the category name from the Treeview
            category_name = values[2]  # Category name from Treeview
            if category_name in self.category_map:
                self.category_combobox.set(category_name)
            self.entries["Price ($)"].delete(0, "end")
            self.entries["Price ($)"].insert(0, values[4])