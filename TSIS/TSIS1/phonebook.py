from connect import get_connection
import psycopg2
from config import DB_config
import json


def create_table():
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS contacts ( id SERIAL PRIMARY KEY, name VARCHAR(200),
                email VARCHAR(100),
                birthday DATE,
                group_id INTEGER REFERENCES groups(id) );""")
                conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")




def insert_from_csv():
    file_path=input("Enter your file path")
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                with open(file_path, newline='') as csv_file:
                    rows = csv.DictReader(csv_file)

                    for row in rows:
                        try:
                            # 1. Insert into contacts
                            cursor.execute("""
                                INSERT INTO contacts (name, email, birthday, group_id)
                                VALUES (%s, %s, %s, %s)
                                RETURNING id;
                            """, (
                                row['name'],
                                row.get('email'),
                                row.get('birthday'),
                                row.get('group_id')
                            ))

                            contact_id = cursor.fetchone()[0]

                            # 2. Insert into phones
                            cursor.execute("""
                                INSERT INTO phones (contact_id, phone, type)
                                VALUES (%s, %s, %s);
                            """, (
                                contact_id,
                                row['phone'],
                                'mobile'  # default type
                            ))

                        except Exception as e:
                            print(f"Error inserting {row.get('name')}: {e}")

                conn.commit()

        print("Completed inserting CSV file")

    except Exception as e:
        print(f"Database error: {e}")


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email (optional): ")
    birthday = input("Enter birthday (YYYY-MM-DD, optional): ")
    group_id = input("Enter group id (optional): ")

    # handle empty inputs
    email = email if email else None
    birthday = birthday if birthday else None
    group_id = group_id if group_id else None

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                # 1. Insert into contacts
                cursor.execute("""
                    INSERT INTO contacts (name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                """, (name, email, birthday, group_id))

                contact_id = cursor.fetchone()[0]

                # 2. Insert into phones
                cursor.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s);
                """, (contact_id, phone, 'mobile'))

            conn.commit()

        print("Contact added successfully")

    except Exception as e:
        print(f"Database error: {e}")


def update_contact():
    contact_id = input("Enter contact ID: ")

    print("1. Update name")
    print("2. Update email")
    print("3. Update birthday")
    print("4. Update group")
    print("5. Update phone")

    choice = input("Choose option: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                if choice == "1":
                    new_name = input("Enter new name: ")
                    cursor.execute(
                        "UPDATE contacts SET name=%s WHERE id=%s;",
                        (new_name, contact_id)
                    )

                elif choice == "2":
                    new_email = input("Enter new email: ")
                    cursor.execute(
                        "UPDATE contacts SET email=%s WHERE id=%s;",
                        (new_email, contact_id)
                    )

                elif choice == "3":
                    new_birthday = input("Enter birthday (YYYY-MM-DD): ")
                    cursor.execute(
                        "UPDATE contacts SET birthday=%s WHERE id=%s;",
                        (new_birthday, contact_id)
                    )

                elif choice == "4":
                    new_group = input("Enter group id: ")
                    cursor.execute(
                        "UPDATE contacts SET group_id=%s WHERE id=%s;",
                        (new_group, contact_id)
                    )

                elif choice == "5":
                    old_phone = input("Enter old phone: ")
                    new_phone = input("Enter new phone: ")

                    cursor.execute(
                        "UPDATE phones SET phone=%s WHERE contact_id=%s AND phone=%s;",
                        (new_phone, contact_id, old_phone)
                    )

            conn.commit()

        print("Update successful")

    except Exception as e:
        print(f"Database error: {e}")




def query_contacts():
    print("1. By name")
    print("2. By phone prefix")

    choice = input("Choose filter: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                if choice == "1":
                    name = input("Enter name: ")
                    cursor.execute("""
                        SELECT c.id, c.name, c.email, c.birthday, p.phone, p.type
                        FROM contacts c
                        LEFT JOIN phones p ON c.id = p.contact_id
                        WHERE c.name ILIKE %s;
                    """, (f"%{name}%",))

                elif choice == "2":
                    prefix = input("Enter prefix: ")
                    cursor.execute("""
                        SELECT c.id, c.name, c.email, c.birthday, p.phone, p.type
                        FROM contacts c
                        JOIN phones p ON c.id = p.contact_id
                        WHERE p.phone LIKE %s;
                    """, (f"{prefix}%",))

                results = cursor.fetchall()

                if results:
                    for r in results:
                        print(r)
                else:
                    print("No contacts found")

    except Exception as e:
        print(f"Database error: {e}")



def delete_contact():
    contact_id = input("Enter contact ID: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                # optional: show who you are deleting
                cursor.execute(
                    "SELECT name FROM contacts WHERE id=%s;",
                    (contact_id,)
                )
                result = cursor.fetchone()

                if not result:
                    print("Contact not found")
                    return

                print(f"Deleting: {result[0]}")

                # delete contact (phones auto-deleted via CASCADE)
                cursor.execute(
                    "DELETE FROM contacts WHERE id=%s;",
                    (contact_id,)
                )

            conn.commit()

        print("Deletion successful")

    except Exception as e:
        print(f"Database error: {e}")

def matching_patterns():
    pattern = input("Enter your pattern: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM matching_patterns(%s)",
                    (pattern,)
                )

                results = cursor.fetchall()

                for r in results:
                    print(r)

    except Exception as e:
        print(e)


def pagination():
    limits=int(input("Enter your limit:"))
    offset=int(input("Enter your offset:"))
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor: cursor.execute("SELECT * FROM pagination(%s, %s)", (limits, offset))
            rows=cursor.fetchall()
            for row in rows:
                print(row)
                conn.commit() 
    except Exception as e:
        print(e)


def insertion():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email (optional): ")
    birthday = input("Enter birthday (optional YYYY-MM-DD): ")
    group_id = input("Enter group id (optional): ")

    email = email if email else None
    birthday = birthday if birthday else None
    group_id = group_id if group_id else None

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                # 1. insert contact
                cursor.execute("""
                    INSERT INTO contacts (name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                """, (name, email, birthday, group_id))

                contact_id = cursor.fetchone()[0]

                # 2. insert phone
                cursor.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s);
                """, (contact_id, phone, 'mobile'))

            conn.commit()

        print(f"{name} inserted successfully.")

    except Exception as e:
        print(e)


def upsert_multiple_contacts():
    names = input("Enter names (comma separated): ").split(",")
    phones = input("Enter phones (comma separated): ").split(",")
    emails = input("Enter emails (comma separated, optional): ").split(",")
    birthdays = input("Enter birthdays (comma separated, optional YYYY-MM-DD): ").split(",")
    group_ids = input("Enter group ids (comma separated, optional): ").split(",")

    names = [n.strip() for n in names]
    phones = [p.strip() for p in phones]
    emails = [e.strip() if e.strip() else None for e in emails]
    birthdays = [b.strip() if b.strip() else None for b in birthdays]
    group_ids = [g.strip() if g.strip() else None for g in group_ids]

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                for i in range(len(names)):

                    # 1. insert contact
                    cursor.execute("""
                        INSERT INTO contacts (name, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id;
                    """, (
                        names[i],
                        emails[i] if i < len(emails) else None,
                        birthdays[i] if i < len(birthdays) else None,
                        group_ids[i] if i < len(group_ids) else None
                    ))

                    contact_id = cursor.fetchone()[0]

                    # 2. insert phone
                    cursor.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s);
                    """, (
                        contact_id,
                        phones[i],
                        'mobile'
                    ))

            conn.commit()

        print("Bulk insertion successful!")

    except Exception as e:
        print(e)


def deleting_procedure():
    contact_id = input("Enter contact ID: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                # optional check before deleting
                cursor.execute(
                    "SELECT name FROM contacts WHERE id=%s;",
                    (contact_id,)
                )
                result = cursor.fetchone()

                if not result:
                    print("Contact not found")
                    return

                print(f"Deleting: {result[0]}")

                cursor.execute(
                    "DELETE FROM contacts WHERE id=%s;",
                    (contact_id,)
                )

            conn.commit()

        print("Deletion successful")

    except Exception as e:
        print(e)


def filter_by_group():
    group_id = input("Enter group id: ")
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT * FROM contacts WHERE group_id = %s""", (group_id,))
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
    except Exception as e:
        print(e)

def search_by_email():
    email_part = input("Enter email keyword: ")
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT * FROM contacts WHERE email ILIKE %s""", (f"%{email_part}%",))
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
    except Exception as e:
        print(e)


def sort_contacts():
    print("Sort by:")
    print("1 - name")
    print("2 - birthday")
    print("3 - id")
    choice = input("Choose option: ")
    if choice == "1":
        order = "name"
    elif choice == "2":
        order = "birthday"
    else:
        order = "id"
    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM contacts ORDER BY {order}""")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
    except Exception as e:
        print(e)

def export_to_json():
    file_path = input("Enter your file path: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                cursor.execute("""
                    SELECT c.id, c.name, c.email, c.birthday,
                           g.name AS group_name
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id;
                """)

                contacts = cursor.fetchall()

                result = []

                for c in contacts:
                    contact_id = c[0]

                    cursor.execute("""
                        SELECT phone, type
                        FROM phones
                        WHERE contact_id = %s;
                    """, (contact_id,))

                    phones = cursor.fetchall()

                    result.append({
                        "id": c[0],
                        "name": c[1],
                        "email": c[2],
                        "birthday": str(c[3]) if c[3] else None,
                        "group": c[4],
                        "phones": [
                            {"phone": p[0], "type": p[1]} for p in phones
                        ]
                    })

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print("Exported to JSON successfully")

    except Exception as e:
        print("Database error:", e)

def import_from_json():
    file_path = input("Enter JSON file path: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                for item in data:

                    cursor.execute("""
                        SELECT id FROM contacts WHERE name = %s;
                    """, (item["name"],))

                    existing = cursor.fetchone()
                    contact_id = None

                    if existing:
                        choice = input(f"{item['name']} exists. skip/overwrite? ")

                        if choice.lower() == "skip":
                            continue

                        contact_id = existing[0]

                        # overwrite main info
                        cursor.execute("""
                            UPDATE contacts
                            SET email=%s, birthday=%s
                            WHERE id=%s;
                        """, (
                            item["email"],
                            item["birthday"],
                            contact_id
                        ))

                        # delete old phones
                        cursor.execute("""
                            DELETE FROM phones WHERE contact_id=%s;
                        """, (contact_id,))

                    else:
                        cursor.execute("""
                            INSERT INTO contacts (name, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s)
                            RETURNING id;
                        """, (
                            item["name"],
                            item["email"],
                            item["birthday"],
                            None
                        ))

                        contact_id = cursor.fetchone()[0]

                    # insert phones
                    for p in item.get("phones", []):
                        cursor.execute("""
                            INSERT INTO phones (contact_id, phone, type)
                            VALUES (%s, %s, %s);
                        """, (
                            contact_id,
                            p["phone"],
                            p.get("type", "mobile")
                        ))

        print("JSON import completed")

    except Exception as e:
        print("Database error:", e)

def test_add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    type_ = input("Type (mobile/work/home): ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (name, phone, type_)
                )
            conn.commit()

        print("Phone added via procedure")

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
        print("11. Filter by group")        # NEW
        print("12. Search by email")       # NEW
        print("13. Sort contacts")          # NEW
        print("14. Export to Json")
        print("15. Import from Json")
        print("16. Test add phone")
        print("17. Move to group")
        print("18. Test search")
        print("19. Exit")

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
            filter_by_group()
        elif choice == "12":
            search_by_email()
        elif choice == "13":
            sort_contacts()
        elif choice== "14":
            export_to_json()
        elif choice=="15":
            import_from_json()
        elif choice=="16":
            test_add_phone()
        elif choice=="17":
            move_to_group()
        elif choice=="18":
            test_search()
        elif choice == "19":
            print("Leaving...")
            break
        else:
            print("Invalid option, try again.")

def test_move_to_group():
    name = input("Contact name: ")
    group = input("Group name: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "CALL move_to_group(%s, %s)",
                    (name, group)
                )
            conn.commit()

        print("Group updated")

    except Exception as e:
        print(e)

def test_search():
    query = input("Search: ")

    try:
        with psycopg2.connect(**DB_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM search_contacts(%s)",
                    (query,)
                )

                for row in cursor.fetchall():
                    print(row)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    menu()


                    

    
        





  







