import dbConnect as db

try:
    # Connect to DB
    conn = db.connect()
    # Create a cursor
    cur = db.cursor(conn)

    # Create Admin tables if not exists.
    tables = (
        """
        CREATE TABLE IF NOT EXISTS supplier (
            id SERIAL UNIQUE PRIMARY KEY,
            name VARCHAR ( 50 ) NOT NULL,
            phonenumber INT NOT NULL,
            address VARCHAR (200) NOT NULL,
            postnr INT NOT NULL,
            city VARCHAR (50),
            country VARCHAR (50)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS product (
            p_code SERIAL UNIQUE PRIMARY KEY,
            p_name VARCHAR (55) NOT NULL,
            p_quantity INT,
            p_basePrice INT,
            p_supplier VARCHAR (55) NOT NULL
        )
        """,
    )
    
    for table in tables:
        cur.execute(table)

    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
    conn.close()
except (Exception, db.psycopg2.DatabaseError) as error:
    print("*"*40)
    print("--- !!! Error on Admin file !!! ---")
    print(error)

def start():
    while 1:
        print("\n")
        print("*"*40)
        print("Admin page")
        print("*"*40)

        print("1. Add supplier")
        print("2. Add product")
        print("3. Edit the quantity of a product")
        print("4. Delete a product")
        print("5. See a list of all products")
        print("6. Search a product")
        print("7. Add a list of possible discounts")
        print("8. See discounts history")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            addSupplier()
        elif ch == 2:
            print("*"*40)
            addProduct()
        else:
            print("*"*40)
            print("Wrong Choice, try again!")
    
def addSupplier ():
    print("*"*40)
    print("Add Suplier")

    name = input("Name: ")
    address = input("Adress: ")
    postnr = int(input("Postnr: "))
    phonenumber = input("Phone number: ")
    city = input("City: ")
    country = input("Country: ")

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        print("Add new Supplier ...")
        cur.execute("""
            INSERT INTO Supplier (name, address, postnr, phonenumber, city, country)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (str(name), str(address), int(postnr), int(phonenumber), str(city), str(country))
        )
        cur.close()
        conn.commit()
        print("New customer registered.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to add new supplier !!! ---")
        print(error)

def addProduct():
    print("*"*40)
    print("Add Product")
    print("*"*40)
    
    p_name = input('Product name: ')
    p_quantity = input('Quantity: ')
    p_basePrice = input('Base price: ')
    p_supplier = str(input('Supplier: '))

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        print("Add Product ...")
        cur.execute("""
            INSERT INTO product (p_name, p_quantity, p_basePrice, p_supplier)
            VALUES (%s, %s, %s, %s);
            """,
            (str(p_name), int(p_quantity), int(p_basePrice), p_supplier)
        )
        cur.close()
        conn.commit()
        print("New product is added.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to add a product !!! ---")
        print(error)

    
    

    
