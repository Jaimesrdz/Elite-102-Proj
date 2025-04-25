import tkinter as tk
import mysql.connector
import re

# Connect to SQL
connection = mysql.connector.connect(user='root', database='example', password='PassworD!1')
cursor = connection.cursor()

logged_in_user_email = None

# Make sure email and phone are valid
def verify_email(email):
    pattern = r"[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
    return re.match(pattern, email)

def verify_phone(phone):
    pattern = r"^[1-9]\d{2}-\d{3}-\d{4}$"
    return re.match(pattern, phone)


# Loads new frames every time the user clicks something
def show_frame(frame_function):
    # Remove widgets and create new content with frame_function()
    for widget in main_frame.winfo_children():
        widget.destroy()
    frame_function()


# Account (create) frame
def create_acc_frame():
    def submit():
        name = name_entry.get()  # Get info from user
        email = email_entry.get()
        phone = phone_entry.get()
        password = password_entry.get()

        error_text.config(text="")   # Clears error messages once process starts
        success_text.config(text="")

        if not verify_email(email):
            error_text.config(text="Invalid Email", fg="red")
            return
        if not verify_phone(phone):
            error_text.config(text="Invalid Phone Number", fg="red")
            return

        try:
            cursor.execute(
                "INSERT INTO customers (user_name, user_email, phone_number, balance, password) VALUES (%s, %s, %s, %s, %s)", 
                (name, email, phone, '0.00', password)
            )
            connection.commit()
            success_text.config(text="Account created successfully!", fg="green")
        except mysql.connector.IntegrityError:
            error_text.config(text="Email or Phone already in use", fg="red")

    tk.Label(main_frame, text="Create Account", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    
    tk.Label(main_frame, text="Name:", fg='#ffffff', bg="#005EB8").pack()
    name_entry = tk.Entry(main_frame)
    name_entry.pack()

    tk.Label(main_frame, text="Email:", fg='#ffffff', bg="#005EB8").pack()
    email_entry = tk.Entry(main_frame)
    email_entry.pack()

    tk.Label(main_frame, text="Phone (xxx-xxx-xxxx):", fg='#ffffff', bg="#005EB8").pack()
    phone_entry = tk.Entry(main_frame)
    phone_entry.pack()

    tk.Label(main_frame, text="Password:", fg='#ffffff', bg="#005EB8").pack()
    password_entry = tk.Entry(main_frame, show="*")
    password_entry.pack()

    error_text = tk.Label(main_frame, text="", fg="red", bg="#005EB8")
    error_text.pack()
    success_text = tk.Label(main_frame, text="", fg="green", bg="#005EB8")
    success_text.pack()

    tk.Button(main_frame, text="Submit", command=submit).pack()
    tk.Button(main_frame, text="Back", command=lambda: show_frame(main_menu_frame)).pack()


# Login menu frame
def login_frame():
    def submit():
        global logged_in_user_email
        email = email_entry.get()
        password = password_entry.get()

        error_text.config(text="")
        success_text.config(text="")

        cursor.execute("SELECT user_name FROM customers WHERE user_email = %s AND BINARY password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            success_text.config(text=f"Welcome, {user[0]}", fg="green")
            logged_in_user_email = email
            show_frame(logged_in_menu_frame)
        else:
            error_text.config(text="Invalid email or password", fg="red")

    tk.Label(main_frame, text="Login", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(padx=200, pady=10)
    
    tk.Label(main_frame, text="Email:", fg='#ffffff', bg="#005EB8").pack()
    email_entry = tk.Entry(main_frame)
    email_entry.pack()
    
    tk.Label(main_frame, text="Password:", fg='#ffffff', bg="#005EB8").pack()
    password_entry = tk.Entry(main_frame, show="*")
    password_entry.pack()

    error_text = tk.Label(main_frame, text="", fg="red", bg="#005EB8")
    error_text.pack()
    success_text = tk.Label(main_frame, text="", fg="green", bg="#005EB8")
    success_text.pack()
    
    tk.Button(main_frame, text="Login", command=submit).pack(pady=5)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(main_menu_frame)).pack(pady=10)


# Logged in menu frame
def logged_in_menu_frame():
    tk.Label(main_frame, text="Main Menu", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    check_balance_frame()
    tk.Button(main_frame, text="Deposit Funds", command=lambda: show_frame(deposit_frame)).pack(pady=5)
    tk.Button(main_frame, text="Withdraw Funds", command=lambda: show_frame(withdraw_frame)).pack(pady=5)
    tk.Button(main_frame, text="Account Details", command=lambda: show_frame(account_details_frame)).pack(pady=5)
    tk.Button(main_frame, text="Log Out", command=lambda: show_frame(main_menu_frame)).pack(pady=5)


# Check balance frame
def check_balance_frame():
    cursor.execute("SELECT balance FROM customers WHERE user_email = %s", (logged_in_user_email,))
    balance = cursor.fetchone()

    tk.Label(main_frame, text="Current Balance", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    tk.Label(main_frame, text=f"${balance[0]}", fg='#ffffff', bg="#005EB8", font='Frutiger, 20').pack(pady=5)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(logged_in_menu_frame)).pack(pady=5)


# Deposit funds frame
def deposit_frame():
    def submit():
        try:
            amount = float(entry.get())
            if amount <= 0:
                message_label.config(text="Deposit amount must be greater than zero.", fg="red")
                return
            cursor.execute("UPDATE customers SET balance = balance + %s WHERE user_email = %s", (amount, logged_in_user_email))
            connection.commit()
            message_label.config(text=f"${amount:.2f} deposited successfully!", fg="green")
            entry.delete(0, tk.END)
        except ValueError:
            message_label.config(text="Invalid amount", fg="red")
            
    tk.Label(main_frame, text="Deposit Funds", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    tk.Label(main_frame, text="Enter deposit amount:", fg='#ffffff', bg="#005EB8").pack()
    entry = tk.Entry(main_frame)
    entry.pack()
    message_label = tk.Label(main_frame, text="", fg="green", bg="#005EB8")
    message_label.pack()
    tk.Button(main_frame, text="Submit", command=submit).pack(pady=5)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(logged_in_menu_frame)).pack(pady=5)


# Withdraw funds frame
def withdraw_frame():
    def submit():
        try:
            amount = float(entry.get())
            if amount <= 0:
                message_label.config(text="Withdraw amount must be greater than zero.", fg="red")
                return
            cursor.execute("UPDATE customers SET balance = balance - %s WHERE user_email = %s", (amount, logged_in_user_email))
            connection.commit()
            message_label.config(text=f"${amount:.2f} withdrawn successfully!", fg="green")
        except ValueError:
            message_label.config(text="Invalid amount", fg="red")
            
    tk.Label(main_frame, text="Withdraw Funds", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    tk.Label(main_frame, text="Enter withdraw amount:", fg='#ffffff', bg="#005EB8").pack()
    entry = tk.Entry(main_frame)
    entry.pack()
    message_label = tk.Label(main_frame, text="", fg="green", bg="#005EB8")
    message_label.pack()
    tk.Button(main_frame, text="Submit", command=submit).pack(pady=5)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(logged_in_menu_frame)).pack(pady=5)


# Account details frame
def account_details_frame():
    cursor.execute("SELECT user_id FROM customers WHERE user_email = %s", (logged_in_user_email,))
    user_id = cursor.fetchone()
    cursor.execute("SELECT phone_number FROM customers WHERE user_email = %s", (logged_in_user_email,))
    phone_number = cursor.fetchone()
    cursor.execute("SELECT user_email FROM customers WHERE user_email = %s", (logged_in_user_email,))
    user_email = cursor.fetchone()
    cursor.execute("SELECT password FROM customers WHERE user_email = %s", (logged_in_user_email,))
    password = cursor.fetchone()

    tk.Label(main_frame, text="Account Details", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    tk.Label(main_frame, text=f"User ID: {user_id[0]}", fg='#ffffff', bg="#005EB8").pack(pady=2)
    tk.Label(main_frame, text=f"Phone Number: {phone_number[0]}", fg='#ffffff', bg="#005EB8").pack(pady=2)
    tk.Label(main_frame, text=f"Email: {user_email[0]}", fg='#ffffff', bg="#005EB8").pack(pady=2)
    tk.Label(main_frame, text=f"Password: {password[0]}", fg='#ffffff', bg="#005EB8").pack(pady=2)
    
    tk.Button(main_frame, text="Change Phone Number", command=lambda: show_frame(change_phone_frame)).pack(pady=2)
    tk.Button(main_frame, text="Change Email Address", command=lambda: show_frame(change_email_frame)).pack(pady=2)
    tk.Button(main_frame, text="Change Password", command=lambda: show_frame(change_password_frame)).pack(pady=2)
    tk.Button(main_frame, text="Delete Account", command=lambda: show_frame(delete_account_frame)).pack(pady=2)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(logged_in_menu_frame)).pack(pady=5)


# Change phone number frame
def change_phone_frame():
    def submit():
        new_phone = entry.get()
        if not verify_phone(new_phone):
            message_label.config(text="Invalid phone number", fg="red")
            return
        cursor.execute("UPDATE customers SET phone_number = %s WHERE user_email = %s", (new_phone, logged_in_user_email))
        connection.commit()
        message_label.config(text="Phone number changed successfully", fg="green")
    tk.Label(main_frame, text="Change Phone Number", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    tk.Label(main_frame, text="Enter new phone number (xxx-xxx-xxxx):", fg='#ffffff', bg="#005EB8").pack()
    entry = tk.Entry(main_frame)
    entry.pack()
    message_label = tk.Label(main_frame, text="", fg="green", bg="#005EB8")
    message_label.pack()
    tk.Button(main_frame, text="Submit", command=submit).pack(pady=5)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(account_details_frame)).pack(pady=5)


# Change email address frame
def change_email_frame():
    def submit():
        new_email = entry.get()
        if not verify_email(new_email):
            message_label.config(text="Invalid email", fg="red")
            return
        global logged_in_user_email
        cursor.execute("UPDATE customers SET user_email = %s WHERE user_email = %s", (new_email, logged_in_user_email))
        connection.commit()
        logged_in_user_email = new_email
        message_label.config(text="Email address changed successfully", fg="green")
    tk.Label(main_frame, text="Change Email Address", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    tk.Label(main_frame, text="Enter new email:", fg='#ffffff', bg="#005EB8").pack()
    entry = tk.Entry(main_frame)
    entry.pack()
    message_label = tk.Label(main_frame, text="", fg="green", bg="#005EB8")
    message_label.pack()
    tk.Button(main_frame, text="Submit", command=submit).pack(pady=5)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(account_details_frame)).pack(pady=5)


# Change password frame
def change_password_frame():
    def submit():
        new_password = entry.get()
        cursor.execute("UPDATE customers SET password = %s WHERE user_email = %s", (new_password, logged_in_user_email))
        connection.commit()
        message_label.config(text="Password changed successfully", fg="green")
    tk.Label(main_frame, text="Change Password", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    tk.Label(main_frame, text="Enter new password:", fg='#ffffff', bg="#005EB8").pack()
    entry = tk.Entry(main_frame, show="*")
    entry.pack()
    message_label = tk.Label(main_frame, text="", fg="green", bg="#005EB8")
    message_label.pack()
    tk.Button(main_frame, text="Submit", command=submit).pack(pady=5)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(account_details_frame)).pack(pady=5)


# Delete account frame
def delete_account_frame():
    def submit():
        global logged_in_user_email
        password_input = entry.get()
        cursor.execute("SELECT * FROM customers WHERE user_email = %s AND password = %s", (logged_in_user_email, password_input))
        user = cursor.fetchone()
        if user:
            cursor.execute("DELETE FROM customers WHERE user_email = %s", (logged_in_user_email,))
            connection.commit()
            logged_in_user_email = None
            message_label.config(text="Account deleted successfully!", fg="green")
            show_frame(main_menu_frame)
        else:
            message_label.config(text="Invalid password", fg="red")
    tk.Label(main_frame, text="Delete Account", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(pady=10)
    tk.Label(main_frame, text="Enter your password to confirm:", fg='#ffffff', bg="#005EB8").pack()
    entry = tk.Entry(main_frame, show="*")
    entry.pack()
    message_label = tk.Label(main_frame, text="", fg="green", bg="#005EB8")
    message_label.pack()
    tk.Button(main_frame, text="Delete", command=submit).pack(pady=5)
    tk.Button(main_frame, text="Back", command=lambda: show_frame(account_details_frame)).pack(pady=5)


# Main menu frame
def main_menu_frame():
    tk.Label(main_frame, text="Welcome to Chase Bank", font=('Frutiger', 18), fg='#ffffff', bg="#005EB8").pack(padx=75, pady=10)
    tk.Button(main_frame, text="Create Account", command=lambda: show_frame(create_acc_frame)).pack(pady=5)
    tk.Button(main_frame, text="Login", command=lambda: show_frame(login_frame)).pack(pady=5)
    tk.Button(main_frame, text="Exit", command=root.quit).pack(pady=10)


# Setting up tkinter
root = tk.Tk()
root.title("Banking System")

main_frame = tk.Frame(root, bg="#005EB8")  # The background color
main_frame.pack(fill="both", expand=True)

main_menu_frame()

root.mainloop()  # mainloop waits for user interactions

cursor.close()
connection.close()
