# gui/login.py
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from database.db_manager import DatabaseManager
from PIL import Image, ImageTk

class LoginWindow:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success

        # Create a Toplevel window for the login dialog
        self.root = tk.Toplevel(self.parent)
        self.root.title("Login - Computer Parts Inventory")
        self.root.geometry("500x500")  # Increased height to accommodate logo
        self.root.configure(bg="#f0f4f8")

        # Fonts and colors
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
        self.bg_color = "#f0f4f8"
        self.accent_color = "#4a90e2"

        # Database
        self.db = DatabaseManager()

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # Load and display logo at the top
        try:
            logo_img = Image.open("images/logo.png")
            logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)  # Resize logo
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.main_frame, image=self.logo_photo, bg=self.bg_color)
            logo_label.pack(pady=10, padx=10, anchor="center")
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = tk.Label(self.main_frame, text="Logo Not Found", bg=self.bg_color, fg="black", font=self.label_font)
            logo_label.pack(pady=10, padx=10, anchor="center")

        # Title
        ttk.Label(self.main_frame, text="Login", font=self.title_font, background=self.bg_color).pack(pady=20)

        # Username
        ttk.Label(self.main_frame, text="Username", font=self.label_font).pack()
        self.username_entry = ttk.Entry(self.main_frame, font=self.label_font)
        self.username_entry.pack(pady=5)

        # Password
        ttk.Label(self.main_frame, text="Password", font=self.label_font).pack()
        self.password_entry = ttk.Entry(self.main_frame, font=self.label_font, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        tk.Button(self.main_frame, text="Login", command=self.login, font=self.button_font,
                  bg=self.accent_color, fg="white", relief="flat", width=12).pack(pady=20)

        # Ensure the Toplevel window is destroyed when closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not all([username, password]):
            messagebox.showerror("Error", "Username and password are required!")
            return

        user = self.db.authenticate_user(username, password)
        if user:
            self.on_login_success(user)
            self.root.destroy()  # Close the login window
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def on_close(self):
        self.root.destroy()  # Close the login window
        self.parent.quit()  # Exit the application if the login window is closed