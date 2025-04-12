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
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    #fetchhone stores the user with the correct email and password
    cursor.execute("SELECT user_name FROM customers WHERE user_email = %s AND BINARY password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        print(f"Login successful! Welcome, {user}")
    else:
        print("Invalid email or password.")
        login()
def delete_account():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM customers WHERE user_email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        cursor.execute("DELETE FROM customers WHERE user_email = %s", (email,))
        connection.commit()
        print("Account deleted successfully!")
    else:
        print("Invalid email or password.")

#main menu
def main():
    while True:
        print("\n Welcome to Chase Bank.")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_acc()
        elif choice == "2":
            delete_account()
        elif choice == "3":
            login()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
cursor.close()
connection.close()