import dbConnect as db

try:
    # Connect to DB
    conn = db.connect()
    # Create a cursor
    cur = db.cursor(conn)

    # Create Customer table if not exists
    q = """
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id serial PRIMARY KEY,
            fname VARCHAR ( 50 ) NOT NULL,
            lname VARCHAR ( 50 ) NOT NULL,
            email VARCHAR (100) UNIQUE NOT NULL,
            address VARCHAR (200) NOT NULL,
            city VARCHAR (50) NOT NULL,
            country VARCHAR (50) NOT NULL,
            phonenumber INT NOT NULL
        )
        """

    cur.execute(q)
    cur.close()
    conn.commit()
    conn.close()
except (Exception, db.psycopg2.DatabaseError) as error:
    print("*"*40)
    print("--- !!! Error on customer file !!! ---")
    print(error)

def start():
    while 1:
        print("\n")
        print("*"*40)
        print("Customer page")
        print("*"*40)

        print("1.Sign up")
        print("2.Login")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            signup()
        elif ch == 2:
            login()
        else:
            print("*"*40)
            print("Wrong Choice, try again!")

def signup():
    print("*"*40)
    fname = input("First name: ")
    lname = input("Last name: ")
    email = input("Email: ")
    address = input("Address: ")
    city = input("City: ")
    country = input("Country: ")
    phonenumber = input("Phone number: ")

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        print("Register new customer ...")
        cur.execute("""
            INSERT INTO Customer (fname, lname, email, address, city, country, phonenumber)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (str(fname), str(lname), str(email), str(address), str(city), str(country), int(phonenumber))
        )
        cur.close()
        conn.commit()
        print("New customer registered.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to register new customer !!! ---")
        print(error)

def login():
    print("*"*40)
    email = input("Email: ")

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        print("Customer login ...")
        q = f"SELECT * FROM Customer WHERE email = '{str(email)}'"
        cur.execute(q)
        data = cur.fetchone()

        if data:
            print(f"hello {data[1]}, you are seccessfully loged in.")
        else:
            print("--- !!! Failed to login !!! ---")
            print(f"No customer is registered with email: {email} !!!")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to login !!! ---")
        print(error)
