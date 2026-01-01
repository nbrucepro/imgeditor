import tkinter as tk
from tkinter import messagebox
from database import connect, hash_password
from app import App


class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentication")
        self.root.geometry("380x420")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.is_login = True

        self.build_ui()

    def build_ui(self):
        # Main container
        self.card = tk.Frame(self.root, bg="#1e1e1e", padx=30, pady=30)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
                # Title
        self.title_label = tk.Label(
            self.card,
            text="Welcome Back",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        self.title_label.pack(pady=(0, 5))

        self.subtitle = tk.Label(
            self.card,
            text="Login to continue",
            font=("Segoe UI", 10),
            fg="#aaaaaa",
            bg="#1e1e1e"
        )
        self.subtitle.pack(pady=(0, 20))
                # Username
        self.username = tk.Entry(
            self.card,
            font=("Segoe UI", 11),
            bg="#2a2a2a",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=25
        )
        self.username.pack(ipady=8, pady=8)
                # Password
        self.password = tk.Entry(
            self.card,
            font=("Segoe UI", 11),
            bg="#2a2a2a",
            fg="white",
            insertbackground="white",
            relief="flat",
            show="*",
            width=25
        )
        self.password.pack(ipady=8, pady=8)

        # Show password toggle
        self.show_password = tk.BooleanVar(value=False)
        self.show_pass_cb = tk.Checkbutton(
        self.card,
        text="Show password",
        variable=self.show_password,
        command=self.toggle_password,
        bg="#1e1e1e",
        fg="white",
        activebackground="#1e1e1e",
        activeforeground="white",
        selectcolor="#1e1e1e",
        font=("Segoe UI", 9)
        )
        self.show_pass_cb.pack(anchor="w", pady=(0, 10))

        # Action Button
        self.action_btn = tk.Button(
            self.card,
            text="Login",
            command=self.login,
            bg="#4f46e5",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            width=20,
            pady=8,
            cursor="hand2"
        )
        self.action_btn.pack(pady=15)

        # Switch mode
        self.switch_btn = tk.Button(
            self.card,
            text="Don't have an account? Register",
            command=self.toggle_mode,
            bg="#1e1e1e",
            fg="#8b8bff",
            relief="flat",
            cursor="hand2"
        )
        self.switch_btn.pack()
    def toggle_password(self):
        if self.show_password.get():
            self.password.config(show="")
        else:
            self.password.config(show="*")


    def toggle_mode(self):
        self.is_login = not self.is_login

        if self.is_login:
            self.title_label.config(text="Welcome Back")
            self.subtitle.config(text="Login to continue")
            self.action_btn.config(text="Login", command=self.login)
            self.switch_btn.config(text="Don't have an account? Register")
        else:
            self.title_label.config(text="Create Account")
            self.subtitle.config(text="Register to get started")
            self.action_btn.config(text="Register", command=self.register)
            self.switch_btn.config(text="Already have an account? Login")
    def register(self):
        user = self.username.get()
        pwd = self.password.get()

        if not user or not pwd:
            messagebox.showerror("Error", "All fields are required")
            return

        conn = connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user, hash_password(pwd))
            )
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully")
            self.toggle_mode()
        except:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()
    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user, hash_password(pwd))
        )

        if cursor.fetchone():
            messagebox.showinfo("Success", "Login successful")
            self.root.destroy()
            App(user)  # Launch image editor
        else:
            messagebox.showerror("Error", "Invalid credentials")

        conn.close()
if __name__ == "__main__":
    root = tk.Tk()
    AuthApp(root)
    root.mainloop()