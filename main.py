import psycopg2
from pprint import pprint


def create_db(conn1):
    with conn1.cursor() as cur:
        cur.execute("""
                        DROP TABLE phones;
                        DROP TABLE clients
                    """)

        cur.execute("""
                        CREATE TABLE IF NOT EXISTS clients(
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(60) NOT NULL,
                        last_name VARCHAR(60) NOT NULL,
                        email VARCHAR(60) UNIQUE         
                        ); 
                    """)

        cur.execute("""
                        CREATE TABLE IF NOT EXISTS phones(
                            id SERIAL PRIMARY KEY,
                            phone_num VARCHAR(60) NOT NULL,
                            client_id INTEGER REFERENCES clients(id)
                             ); 
                    """)

        conn.commit()


def add_client(conn1):  # Добавляем клиента
    f_name = input("Enter client's first name: ")
    l_name = input("Enter client's last name: ")
    email = input("Enter client's e-mail: ")
    with conn1.cursor() as cur:
        cur.execute("""
                        INSERT INTO clients(first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
                    """, (f_name, l_name, email)
                    )
        id_client = cur.fetchone()[0]
    return id_client


def add_phone(conn1, client_id):
    ph_num = input("Enter phone number: ")
    with conn1.cursor() as cur:
        cur.execute("""
                        INSERT INTO phones(phone_num, client_id) VALUES (%s, %s) RETURNING id;
                    """, (ph_num, client_id)
                    )
        print(cur.fetchone()[0])  # выводим ID записи


def change_client(conn1, client_id):
    first_name = input('Enter new first name: ')
    last_name = input('Enter new last name: ')
    email = input('Enter new e-mail: ')
    phone = input('Enter new phone number: ')
    with conn1.cursor() as cur:
        if first_name != '':
            cur.execute("""
                         UPDATE clients SET first_name=%s WHERE id=%s;     
                        """, (first_name, client_id))
            conn1.commit()
        if last_name != '':
            cur.execute("""
                         UPDATE clients SET last_name=%s WHERE id=%s;     
                        """, (last_name, id))
            conn1.commit()
        if email != '':
            cur.execute("""
                         UPDATE clients SET email=%s WHERE id=%s;     
                        """, (email, id))
            conn1.commit()
        if phone != '':
            cur.execute("""
                         UPDATE phones SET phone_num=%s WHERE client_id=%s;     
                        """, (phone, id))
            conn1.commit()

    pass


def delete_phone(conn1, client_id):
    num = input("Enter client's phone: ")
    with conn1.cursor() as cur:
        cur.execute("""
                        DELETE FROM phones 
                        WHERE client_id=%s AND phone_num = %s;
                    """, (client_id, num))
        conn1.commit()


def delete_client(conn1, client_id):
    with conn1.cursor() as cur:
        cur.execute("""
                        DELETE FROM phones 
                        WHERE client_id=%s;
                    """, (client_id,))
        conn1.commit()
        cur.execute("""
                                DELETE FROM clients 
                                WHERE id=%s;
                            """, (client_id,))
        conn1.commit()


def find_phone(conn1):
    with conn1.cursor() as cur:
        cur.execute("""
                            SELECT * FROM phones;
                    """)
        pprint(cur.fetchall())


def find_client(conn1):
    column = input('Enter column (first_name, last_name, email or phone_num: ')
    data = input('Enter data to find: ')

    with conn1.cursor() as cur:
        if column == 'first_name':
            cur.execute("""
                            SELECT c.id, first_name, last_name, email, phone_num FROM clients c
                            LEFT JOIN phones on c.id = phones.client_id
                            WHERE first_name=%s;
                         """, (data,))
            pprint(cur.fetchall())
        if column == 'last_name':
            cur.execute("""
                            SELECT c.id, first_name, last_name, email, phone_num FROM clients c
                            LEFT JOIN phones on c.id = phones.client_id
                            WHERE last_name=%s;
                         """, (data,))
            pprint(cur.fetchall())
        if column == 'email':
            cur.execute("""
                            SELECT c.id, first_name, last_name, email, phone_num FROM clients c
                            LEFT JOIN phones on c.id = phones.client_id
                            WHERE email=%s;
                         """, (data,))
            pprint(cur.fetchall())
        if column == 'phone_num':
            cur.execute("""
                            SELECT c.id, first_name, last_name, email, phone_num FROM clients c
                            LEFT JOIN phones on c.id = phones.client_id
                            WHERE phone_num=%s;
                         """, (data,))
            pprint(cur.fetchall())


username = input('DataBase user: ')
passwd = input('DataBase password: ')

conn = psycopg2.connect(database="phone_book", user=username, password=passwd)

create_db(conn)  # Создание таблиц в БД
# conn
while True:
    st = input('введите команду: ')
    if st.lower() == 'a' or st.lower() == 'add':
        p = add_client(conn)  # добавление клиента в адресную книгу
        pg_exist = input("Do you want to enter phone number? (Y/N)")  # если есть телефон, сразу добавляем
        if pg_exist.lower() == 'y':
            add_phone(conn, p)
    elif st.lower() == 'ap' or st.lower() == 'add_phone':  # добавляем телефон к существующему клиенту
        client_id = int(input("Enter client's ID: "))
        add_phone(conn, client_id)
    elif st.lower() == 'dp' or st.lower() == 'del_phone':  # удаляем телефон существующего клиента
        client_id = int(input("Enter client's ID: "))
        delete_phone(conn, client_id)
    elif st.lower() == 'dc' or st.lower() == 'del_client':  # удаляем клиента
        client_id = int(input("Enter client's ID: "))
        delete_client(conn, client_id)
    elif st.lower() == 'cc' or st.lower() == 'change_client':  # меняем клиента
        client_id = int(input("Enter client's ID: "))
        change_client(conn, client_id)
    elif st.lower() == 'f' or st.lower() == 'find':  # поиск клиента
        find_client(conn)

    else:
        break  # выходим из программы

conn.close()
