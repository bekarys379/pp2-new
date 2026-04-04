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
                    phone VARCHAR(200) UNIQUE
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
                                "INSERT INTO phonebook (name, phone) VALUES (%s, %s);",
                                (row['name'], row['phone'])
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
    inumber=input("Enter phone:")
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s);", (iname, inumber))
            conn.commit()
        print("Contact added succesfully")
    except Exception as e:
        print(f"Database error:{e}")


#Implement updating a contact's first name or phone number

def update_contact():
    phone = input("Enter the phone of the contact to update: ")
    print("1. Update name")
    print("2. Update phone")
    choice = input("Choose option: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                if choice=="1":
                    new_name=input("Enter new name")
                    cursor.execute("UPDATE phonebook SET name=%s WHERE phone=%s;", (new_name, phone))
                elif choice == "2":
                    new_phone = input("Enter new phone: ")
                    cursor.execute("UPDATE phonebook SET phone=%s WHERE phone=%s;", (new_phone, phone))
            conn.commit()
        print("Update added succesfully")
    except Exception as e:
        print(f"Database error:{e}")


#Implement querying contacts with different filters (e.g. by name, by phone prefix)


def query_contacts():
    print("1. By name")
    print("2. By phone prefix")
    choice = str(input("Choose filter: "))

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                if choice=="1":
                    name=input("Enter name")
                    cursor.execute("SELECT * FROM phonebook WHERE name ILIKE %s;", (f"%{name}%",))
                elif choice=="2":
                    prefix=input("Enter prefix")
                    cursor.execute("SELECT * FROM phonebook WHERE phone LIKE %s;", (f"{prefix}%",))
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
    print("2. By phone")
    choice=str(input())
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                if choice=="1":
                    name=input("Enter username")
                    cursor.execute("DELETE FROM phonebook WHERE name=%s;", (name,))
                elif choice=="2":
                    phone=input("Enter the phone")
                    cursor.execute("DELETE FROM phonebook WHERE phone=%s;", (phone,))
            conn.commit()
        print("Deletion was succesfull")
    except Exception as e:
        print(f"Database error:{e}")

#updated part starts here
def matching_patterns():
    pattern=input("Enter your pattern:")
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM matching_patterns(%s)", (pattern,))
                results=cursor.fetchall()
                for r in results:
                    print(r)
            conn.commit()
    except Exception as e:
        print(e)


def pagination():
    limits=int(input("Enter your limit:"))
    offset=int(input("Enter  your offset:"))
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pagination(%s, %s)", (limits, offset))
                rows=cursor.fetchall()
                for row in rows:
                    print(row)
            conn.commit()
    except Exception as e:
        print(e)


def insertion():
    name=input("Enter the name:")
    phone=input("Enter the phone:")
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CALL insert_user(%s, %s)", (name, phone))
            conn.commit()
            print(f"{name} inserted/updated successfully.")
    except Exception as e:
        print(e)


def upsert_multiple_contacts():
    names=input("Enter the names").split(",")
    phones=input("Enter the numbers").split(",")

    names = [n.strip() for n in names]
    phones = [p.strip() for p in phones]
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CALL insert_many_users(%s, %s)", (names, phones))
            conn.commit()
            print("Insertion was successful!")
    except Exception as e:
        print(e)


def deleting_procedure():
    name=input("Enter the name:")
    phone=input("Enter the phone:")
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CALL delete_data(%s, %s)", (name, phone))
            conn.commit()
            print("Deletion was successful")
    except Exception as e:
        print(e)



def menu():
    create_table()
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update Contact")
        print("4. Query Contacts")
        print("5. Delete Contact")
        print("6. Find by pattern")
        print("7. Paginate")
        print("8. Insertion ")
        print("9. Upsert multiple users")
        print("10. Deleting procedure")
        print("11. Exit")

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
            matching_patterns()
        elif choice == "7":
            pagination()
        elif choice == "8":
            insertion()
        elif choice == "9":
            upsert_multiple_contacts()
        elif choice == "10":
            deleting_procedure()
        elif choice == "11":
            print("Leaving...")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    menu()


                    

    
        





  







