import psycopg2
import csv
from config import DB_config


def create_table():
        try:
             with psycopg2.connect(**DB_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200),
                    number VARCHAR(200) UNIQUE
                    );
                    """)
                    conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

#Command to insert contacts from csv

def insert_from_csv(file_path):
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                with open(file_path, newline='') as csv_file:
                    rows=csv.DictReader(csv_file)
                    for row in rows:
                        try:
                            cursor.execute(
                                "INSERT INTO phonebook (name, number) VALUES (%s, %s);",
                                (row['name'], row['number'])
                            )
                        except Exception as e:
                            print(f"Error inserting {row['name']}:{e}")
                conn.commit()
        print("Completed inserting CSV file")
    except Exception as e:
        print(f"Database error:{e}")


#Inserting contact from console

def insert_from_console():
    iname=input("Enter name:")
    inumber=input("Enter number:")
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO phonebook (name, number) VALUES (%s, %s);", (iname, inumber))
            conn.commit()
        print("Contact added succesfully")
    except Exception as e:
        print(f"Database error:{e}")


#Implement updating a contact's first name or phone number

def update_contact():
    number = input("Enter the phone number of the contact to update: ")
    print("1. Update name")
    print("2. Update number")
    choice = input("Choose option: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                if choice=="1":
                    new_name=input("Enter new name")
                    cursor.execute("UPDATE phonebook SET name=%s WHERE number=%s;", (new_name, number))
            conn.commit()
        print("Update added succesfully")
    except Exception as e:
        print(f"Database error:{e}")


#Implement querying contacts with different filters (e.g. by name, by phone prefix)


def query_contacts():
    print("1. By name")
    print("2. By number prefix")
    choice = str(input("Choose filter: "))

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                if choice=="1":
                    name=input("Enter name")
                    cursor.execute("SELECT * FROM phonebook WHERE name ILIKE %s;", (f"%{name}%",))
                elif choice=="2":
                    prefix=input("Enter prefix")
                    cursor.execute("SELECT * FROM phonebook WHERE name LIKE %s;", (f"{prefix}%",))
                results=cursor.fetchall()
                if results:
                    for r in results:
                        print(r)
                else:
                    print("No contacts found")
    except Exception as e:
        print(f"Database error:{e}")



#Implement deleting a contact by username or phone number


def delete_contact():
    print("1. By username")
    print("2. By number")
    choice=str(input())
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                if choice=="1":
                    name=input("Enter username")
                    cursor.execute("DELETE FROM phonebook WHERE name=%s;", (name,))
                elif choice=="2":
                    number=input("Enter the number")
                    cursor.execute("DELETE FROM phonebook WHERE number=%s;", (number,))
            conn.commit()
        print("Deletion was succesfull")
    except Exception as e:
        print(f"Database error:{e}")



def menu():
    create_table()
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update Contact")
        print("4. Query Contacts")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Leaving...")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    menu()


                    

    
        





  







