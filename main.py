import tkinter as tk
from gui.login import LoginWindow
from gui.dashboard import Dashboard

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Computer Parts Inventory")
        self.root.geometry("1000x600")
        self.current_window = None
        self.current_user = None
        self.show_login()
        self.root.withdraw()

    def show_login(self):
        if self.current_window and self.current_window != self.root:
            self.current_window.destroy()
        self.current_window = LoginWindow(self.root, self.on_login_success)
        self.root.withdraw()

    def on_login_success(self, user):
        self.current_user = user
        self.root.deiconify()  # Show the main window
        if hasattr(self.current_window, 'window'):
            self.current_window.window.destroy()
        else:
            print("Warning: LoginWindow has no 'window' attribute to destroy")
        self.current_window = self.root
        Dashboard(self.current_window, user, self.show_login)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()