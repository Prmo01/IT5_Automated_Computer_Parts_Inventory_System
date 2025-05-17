import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from models.category import Category
from database.db_manager import DatabaseManager

class CategoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Categories")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f4f8")

        self.db = DatabaseManager()

        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
        self.bg_color = "#f0f4f8"
        self.accent_color = "#4a90e2"
        self.button_color = "#2ecc71"
        self.delete_color = "#e74c3c"

        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        ttk.Label(self.main_frame, text="Manage Categories", font=self.title_font, background=self.bg_color).pack(pady=10)

        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill="x", pady=10)

        labels = ["Category Name", "Description"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(self.input_frame, text=label, font=self.label_font).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.input_frame, font=self.label_font, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", pady=10)

        buttons = [
            ("Add Category", self.add_category, self.button_color),
            ("Update Category", self.update_category, self.accent_color),
            ("Delete Category", self.delete_category, self.delete_color),
            ("Clear Fields", self.clear_fields, "#7f8c8d")
        ]
        for text, command, color in buttons:
            btn = tk.Button(self.button_frame, text=text, command=command, font=self.button_font,
                            bg=color, fg="white", relief="flat", width=12)
            btn.pack(side="left", padx=5)

        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill="both", expand=True, pady=10)

        columns = ("ID", "Name", "Description")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_categories()

    def load_categories(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        categories = self.db.fetch_categories()
        for category in categories:
            self.tree.insert("", "end", values=category)

    def add_category(self):
        category = Category(
            name=self.entries["Category Name"].get(),
            description=self.entries["Description"].get()
        )

        is_valid, error_message = category.validate()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        try:
            if self.db.add_category(category):
                self.load_categories()
                self.clear_fields()
                messagebox.showinfo("Success", "Category added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add category: {str(e)}")

    def update_category(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a category to update!")
            return

        category = Category(
            id=self.tree.item(selected)["values"][0],
            name=self.entries["Category Name"].get(),
            description=self.entries["Description"].get()
        )

        is_valid, error_message = category.validate()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return

        try:
            if self.db.update_category(category):
                self.load_categories()
                self.clear_fields()
                messagebox.showinfo("Success", "Category updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update category: {str(e)}")

    def delete_category(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a category to delete!")
            return

        id = self.tree.item(selected)["values"][0]
        try:
            if self.db.delete_category(id):
                self.load_categories()
                self.clear_fields()
                messagebox.showinfo("Success", "Category deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete category. It may be in use by parts.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete category: {str(e)}")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected)["values"]
            self.entries["Category Name"].delete(0, "end")
            self.entries["Category Name"].insert(0, values[1])
            self.entries["Description"].delete(0, "end")
            self.entries["Description"].insert(0, values[2] if values[2] else "")