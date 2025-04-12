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
        create_acc()

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

create_acc()

cursor.close()
connection.close()