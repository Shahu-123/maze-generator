import sqlite3
import tkinter as tk
from tkinter import messagebox

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    db_password = cursor.fetchone()
    conn.close()
    if db_password and db_password[0] == password:
        return True
    return False

def login_register_page():
    account = None
    def on_login():
        nonlocal account
        username = entry_username.get()
        password = entry_password.get()
        if check_login(username, password):
            messagebox.showinfo("Success", "Login successful!")
            account = username
            root.quit()
            return True
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def on_register():
        nonlocal account
        username = entry_username.get().strip()  # Remove any leading or trailing spaces
        password = entry_password.get().strip()

        # Validation Checks:

        # 1. Check if the username and password are not empty
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return False

        # 2. Check the length of the username and password
        if len(username) < 5 or len(password) < 8:
            messagebox.showerror("Error",
                                 "Username must be at least 5 characters and password at least 8 characters long!")
            return False

        # 3. Ensure the password contains at least one number and one uppercase letter
        if not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
            messagebox.showerror("Error", "Password must contain at least one number and one uppercase letter!")
            return False

        # Registration Process:
        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            account = True
            account = username
            root.quit()
            return True
        else:
            messagebox.showerror("Error", "Username already exists!")

    # Function to toggle password visibility
    def toggle_password():
        if show_password_var.get():
            entry_password.config(show='')  # Show password as plain text
        else:
            entry_password.config(show='*')  # Mask password

    root = tk.Tk()
    root.geometry("450x600")
    root.title("Login/Register Page")

    frame = tk.Frame(root, bg="lightblue")
    frame.pack(expand=True, fill="both")

    lbl_title = tk.Label(frame, text="Login or Register", font=("Arial", 18), bg="lightblue")
    lbl_title.pack(pady=20)

    lbl_username = tk.Label(frame, text="Username:", bg="lightblue")
    lbl_username.pack(anchor="w", padx=10, pady=5)

    entry_username = tk.Entry(frame)
    entry_username.pack(padx=10, pady=5, fill="x")

    lbl_password = tk.Label(frame, text="Password:", bg="lightblue")
    lbl_password.pack(anchor="w", padx=10, pady=5)

    entry_password = tk.Entry(frame, show="*")
    entry_password.pack(padx=10, pady=20, fill="x")

    # Add a variable to hold the state of the checkbox
    show_password_var = tk.BooleanVar()
    show_password_var.set(False)

    # Create and place the checkbox for password peek feature
    chk_show_password = tk.Checkbutton(frame, text="Show Password", bg="lightblue", variable=show_password_var,
                                       command=toggle_password)
    chk_show_password.pack(anchor="w", padx=10, pady=5)

    btn_login = tk.Button(frame, text="Login", bg="blue", fg="black", command=on_login)
    btn_login.pack(padx=100, pady=20, fill="x")

    btn_register = tk.Button(frame, text="Register", bg="blue", fg="black", command=on_register)
    btn_register.pack(padx=100, pady=20, fill="x")

    root.mainloop()
    root.destroy()
    return account
