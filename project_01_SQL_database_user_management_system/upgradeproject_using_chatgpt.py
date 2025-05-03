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

    def get_profile(self, user_id):
        self.mycursor.execute(f"""
            SELECT id, name, email FROM user WHERE id = {user_id}
        """)
        return self.mycursor.fetchone()

    def update_profile(self, user_id, name, email, password):
        try:
            self.mycursor.execute(f"""
                UPDATE user
                SET name = '{name}', email = '{email}', password = '{password}'
                WHERE id = {user_id}
            """)
            self.conn.commit()
            return 1
        except:
            return -1

    def delete_profile(self, user_id):
        try:
            self.mycursor.execute(f"""
                DELETE FROM user WHERE id = {user_id}
            """)
            self.conn.commit()
            return 1
        except:
            return -1


class Flipkart:
    def __init__(self):
        self.db = DBhelper()
        self.current_user_id = None
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
            1. Enter 1 to View Profile
            2. Enter 2 to Edit Profile
            3. Enter 3 to Delete Profile
            4. Enter 4 to Logout
            """)
            if choice == "1":
                self.view_profile()
            elif choice == "2":
                self.edit_profile()
            elif choice == "3":
                self.delete_profile()
                break
            elif choice == "4":
                print("Logging out...")
                self.menu()
                break
            else:
                print("Invalid option. Try again.")

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
            self.current_user_id = data[0][0]
            print("Hello", data[0][1])
            self.login_menu()

    def view_profile(self):
        profile = self.db.get_profile(self.current_user_id)
        if profile:
            print("\n--- Profile Details ---")
            print("User ID:", profile[0])
            print("Name   :", profile[1])
            print("Email  :", profile[2])
            print("------------------------\n")
        else:
            print("Profile not found.")

    def edit_profile(self):
        name = input("Enter new name: ")
        email = input("Enter new email: ")
        password = input("Enter new password: ")

        response = self.db.update_profile(self.current_user_id, name, email, password)
        if response == 1:
            print("Profile updated successfully.")
        else:
            print("Failed to update profile.")

    def delete_profile(self):
        confirm = input("Are you sure you want to delete your profile? (yes/no): ")
        if confirm.lower() == "yes":
            response = self.db.delete_profile(self.current_user_id)
            if response == 1:
                print("Profile deleted successfully.")
                self.menu()
            else:
                print("Failed to delete profile.")
        else:
            print("Deletion canceled.")


if __name__ == "__main__":
    Flipkart()
