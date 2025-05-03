import sys
import mysql.connector

class DBhelper:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="hit-db-demo"
            )
            self.mycursor = self.conn.cursor()
        except:
            print("Some error occurred. Could not connect to database.")
            sys.exit(0)
        else:
            print("Connected to Database")

    def register(self, name, email, password):
        try:
            self.mycursor.execute(f"""
                INSERT INTO user (id, name, email, password)
                VALUES (NULL, '{name}', '{email}', '{password}');
            """)
            self.conn.commit()
        except:
            return -1
        else:
            return 1

    def search(self, email, password):
        self.mycursor.execute(f"""
            SELECT * FROM user WHERE email = '{email}' AND password = '{password}'
        """)
        data = self.mycursor.fetchall()
        return data


class Flipkart:
    def __init__(self):
        self.db = DBhelper()
        self.menu()

    def menu(self):
        user_input = input("""
        1. Enter 1 to Register
        2. Enter 2 to Login
        3. Anything else to Exit
        """)
        if user_input == "1":
            self.register()
        elif user_input == "2":
            self.login()
        else:
            sys.exit(1000)

    def login_menu(self):
        while True:
            choice = input("""
            1. Enter 1 to see profile
            2. Enter 2 to edit profile
            3. Enter 3 to delete profile
            4. Enter 4 to logout
            """)
            if choice == "4":
                print("Logging out...")
                self.menu()
                break
            else:
                print("Feature not implemented yet.")

    def register(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        response = self.db.register(name, email, password)
        if response == 1:
            print("Registration Successful!")
        else:
            print("Registration Failed. Email might already exist.")
        self.menu()

    def login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        data = self.db.search(email, password)
        if len(data) == 0:
            print("Incorrect email or password.")
            self.login()
        else:
            print("Hello", data[0][1])
            self.login_menu()


if __name__ == "__main__":
    Flipkart()