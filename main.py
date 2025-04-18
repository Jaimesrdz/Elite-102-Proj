import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

# Connect to MySQL
connection = mysql.connector.connect(user='root', database='example', password='PassworD!1')
cursor = connection.cursor()

# Global variable to store logged-in user's email
logged_in_user_email = None

# Function to verify email
def verify_email(email):
    pattern = r"[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
    return re.match(pattern, email)

# Function to verify phone
def verify_phone(phone):
    pattern = r"^[1-9]\d{2}-\d{3}-\d{4}$"
    return re.match(pattern, phone)

# Function to create account
def create_acc():
    def submit():
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        password = password_entry.get()

        if not verify_email(email):
            messagebox.showerror("Error", "Invalid Email")
            return
        if not verify_phone(phone):
            messagebox.showerror("Error", "Invalid Phone Number")
            return

        try:
            cursor.execute(
                "INSERT INTO customers (user_name, user_email, phone_number, balance, password) VALUES (%s, %s, %s, %s, %s)",
                (name, email, phone, '0.00', password)
            )
            connection.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            acc_window.destroy()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Email already in use")

    acc_window = tk.Toplevel()
    acc_window.title("Create Account")
    
    tk.Label(acc_window, text="Name:").pack()
    name_entry = tk.Entry(acc_window)
    name_entry.pack()

    tk.Label(acc_window, text="Email:").pack()
    email_entry = tk.Entry(acc_window)
    email_entry.pack()

    tk.Label(acc_window, text="Phone:").pack()
    phone_entry = tk.Entry(acc_window)
    phone_entry.pack()

    tk.Label(acc_window, text="Password:").pack()
    password_entry = tk.Entry(acc_window, show="*")
    password_entry.pack()

    tk.Button(acc_window, text="Submit", command=submit).pack()

# Function to login
def login():
    def submit():
        global logged_in_user_email
        email = email_entry.get()
        password = password_entry.get()

        cursor.execute("SELECT user_name FROM customers WHERE user_email = %s AND BINARY password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", f"Welcome, {user[0]}")
            logged_in_user_email = email
            login_window.destroy()
            logged_in_menu()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    login_window = tk.Toplevel()
    login_window.title("Login")
    
    tk.Label(login_window, text="Email:").pack()
    email_entry = tk.Entry(login_window)
    email_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=submit).pack()

# Function to check balance
def check_balance():
    cursor.execute("SELECT balance FROM customers WHERE user_email = %s", (logged_in_user_email,))
    balance = cursor.fetchone()
    messagebox.showinfo("Balance", f"Your current balance is: ${balance[0]}")

# Function to deposit funds
def deposit():
    def submit():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Deposit amount must be greater than zero")
            else:
                cursor.execute("UPDATE customers SET balance = balance + %s WHERE user_email = %s", (amount, logged_in_user_email))
                connection.commit()
                messagebox.showinfo("Success", f"${amount:.2f} deposited successfully!")
                deposit_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit Funds")
    
    tk.Label(deposit_window, text="Deposit Amount:").pack()
    amount_entry = tk.Entry(deposit_window)
    amount_entry.pack()

    tk.Button(deposit_window, text="Submit", command=submit).pack()

# Function to withdraw funds
def withdraw():
    def submit():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Withdraw amount must be greater than zero")
            else:
                cursor.execute("UPDATE customers SET balance = balance - %s WHERE user_email = %s", (amount, logged_in_user_email))
                connection.commit()
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully!")
                withdraw_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    withdraw_window = tk.Toplevel()
    withdraw_window.title("Withdraw Funds")
    
    tk.Label(withdraw_window, text="Withdraw Amount:").pack()
    amount_entry = tk.Entry(withdraw_window)
    amount_entry.pack()

    tk.Button(withdraw_window, text="Submit", command=submit).pack()

# Function for logged-in menu
def logged_in_menu():
    menu_window = tk.Toplevel()
    menu_window.title("Main Menu")
    
    tk.Button(menu_window, text="Check Balance", command=check_balance).pack()
    tk.Button(menu_window, text="Deposit Funds", command=deposit).pack()
    tk.Button(menu_window, text="Withdraw Funds", command=withdraw).pack()

# Main menu function
def main_menu():
    root = tk.Tk()
    root.title("Elite-102-GUI")

    tk.Label(root, text="Welcome to Chase Bank").pack()
    tk.Button(root, text="Create Account", command=create_acc).pack()
    tk.Button(root, text="Login", command=login).pack()
    tk.Button(root, text="Exit", command=root.quit).pack()

    root.mainloop()

main_menu()
