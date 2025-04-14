import mysql.connector

connection = mysql.connector.connect(user='root', database='example', password='creeperS!1')

cursor = connection.cursor()

# Create account function
def create_acc():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    password = input("Enter your password: ")

    # Check if email already in use
    try:
        cursor.execute(
            "INSERT INTO customers (user_name, user_email, phone_number, balance, password) VALUES (%s, %s, %s, %s, %s)",
            (name, email, phone, '0.00', password)
        )
        connection.commit()
        print("Account created successfully!")
    except mysql.connector.IntegrityError:
        print("Email already in use. Please choose a different email.")
        
#login
def login():
    global logged_in_user_email  # make global so we don't hve to ask user for email

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Fetch the user with the correct email and password
    cursor.execute("SELECT user_name FROM customers WHERE user_email = %s AND BINARY password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        print(f"Login successful! Welcome, {user[0]}")
        logged_in_user_email = email  # store the email to use elsewhere
        logged_in_menu()
    else:
        print("Invalid email or password.")

#delete account
def delete_account():
    global logged_in_user_email
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM customers WHERE user_email = %s AND password = %s", (logged_in_user_email, password))
    user = cursor.fetchone()

    if user:
        cursor.execute("DELETE FROM customers WHERE user_email = %s", (logged_in_user_email,))
        connection.commit()
        logged_in_user_email = None  # Reset the email
        print("Account deleted successfully!")
        return True  # Indicate that the account was deleted
    else:
        print("Invalid email or password.")
        return False  # Indicate that the account was not deleted

#Check Balance
def check_balance():
    global logged_in_user_email 

    cursor.execute("SELECT balance FROM customers WHERE user_email = %s", (logged_in_user_email,))
    balance = cursor.fetchone()
    print(f"Your current balance is: ${balance[0]}")



#Deposit funds
def deposit():
    global logged_in_user_email

    try:
        deposit_funds = float(input("Enter deposit amount: "))

        if deposit_funds <= 0:
                print("Deposit amount must be greater than zero.")

        else:
            cursor.execute("UPDATE customers SET balance = balance + %s WHERE user_email = %s", (deposit_funds, logged_in_user_email))
            connection.commit()
            print(f"${deposit_funds:.2f} deposited successfully!")

    except ValueError:
        print("Invalid amount")


#Withdraw
def withdraw():
    global logged_in_user_email

    try:
        withdraw_funds = float(input("Enter withdraw amount: "))

        if withdraw_funds <= 0:
                print("Withdraw amount must be greater than zero.")

        else:
            cursor.execute("UPDATE customers SET balance = balance - %s WHERE user_email = %s", (withdraw_funds, logged_in_user_email))
            connection.commit()
            print(f"${withdraw_funds:.2f} deposited successfully!")

    except ValueError:
        print("Invalid amount")

#Account details
def account_details():
    global logged_in_user_email 
    print("\n ACCOUNT DETAILS")
    cursor.execute("SELECT user_id FROM customers WHERE user_email = %s", (logged_in_user_email,))
    user_id = cursor.fetchone()
    print(f"User ID: {user_id[0]}")

    cursor.execute("SELECT phone_number FROM customers WHERE user_email = %s", (logged_in_user_email,))
    phone_number = cursor.fetchone()
    print(f"Phone Number: {phone_number[0]}")

    cursor.execute("SELECT user_email FROM customers WHERE user_email = %s", (logged_in_user_email,))
    user_email = cursor.fetchone()
    print(f"Email: {user_email[0]}")

    cursor.execute("SELECT password FROM customers WHERE user_email = %s", (logged_in_user_email,))
    password = cursor.fetchone()
    print(f"Password: {password[0]}")


#Change phone number
def change_phone():
    new_phone = input("Enter a phone number: ")
    cursor.execute("UPDATE customers SET phone_number = %s WHERE user_email = %s", (new_phone, logged_in_user_email))
    connection.commit()
    print("Phone number changed successfully")

#Change Email
def change_email():
    global logged_in_user_email
    new_email = input("Enter an Email Address: ")
    cursor.execute("UPDATE customers SET user_email = %s WHERE user_email = %s", (new_email, logged_in_user_email))
    connection.commit()
    logged_in_user_email = new_email #change the email to new email
    print("Email address changed successfully")

#Change password
def change_password():
    new_password = input("Enter a password: ")
    cursor.execute("UPDATE customers SET password = %s WHERE user_email = %s", (new_password, logged_in_user_email))
    connection.commit()
    print("Password changed successfully")

#logged in menu
def logged_in_menu():
    while True:
        print("\n How may we help today?")
        print("1. Check Balance")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. Account Details")
        print("5. Log Out")
        choice = input("Enter your choice: ")

        if choice == "1":
            check_balance()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            account_details()
            print("\n")
            print("1. Change Phone Number")
            print("2. Change Email Address")
            print("3. Change Password")
            print("4. Delete Account")
            sub_choice = input("Enter your choice: ")
            if sub_choice == "1":
                change_phone()
            elif sub_choice == "2":
                change_email()
            elif sub_choice == "3":
                change_password()
            elif sub_choice == "4":
                if delete_account():
                    break  # Exit the logged-in menu if the account is deleted
        elif choice == "5":
            print("Logging out...")
            global logged_in_user_email
            logged_in_user_email = None  # Reset the email
            break
        else:
            print("Invalid choice. Please try again.")



#main menu
def main():
    while True:
        print("\n Welcome to Chase Bank.")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_acc()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
cursor.close()
connection.close()