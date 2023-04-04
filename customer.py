import dbConnect as db
import product
from datetime import datetime


def start():
    while 1:
        print("\n")
        print("*"*40)
        print("Customer page")
        print("*"*40)

        print("1. Sign up")
        print("2. Login")
        print("3. See a list of all available products")
        print("4. Search for aproduct")
        print("5. Add products to the shopping list")
        print("6. See the shopping list's total price and pay")
        print("7. See the orders list")
        print("8. Delete an order")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            signup()
        elif ch == 2:
            login()
        elif ch == 3:
            getListProducts()
        elif ch == 4:
            product.searchProduct()
        elif ch == 5:
            addProductByCustomer()
        elif ch == 6:
            payPrice()
        elif ch == 7:
            seeOrder()
        elif ch == 8:
            deleteOrder()
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

def getListProducts():
    print("\n")
    print("*"*40)
    print("List of all products")
    print("*"*40)

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute("SELECT * FROM product")
        data = cur.fetchall()

        if data:
            print ("{:<8} {:<20} {:<15} {:<15} {:<20} {:<20}".format('Id','Name','Quantity','Price','Supplier', 'Discount'))
            print("-"*92)
            for d in data:
                if d[5]:
                    print ("{:<8} {:<20} {:<15} {:<15} {:<20} {:<20}".format(d[0], d[1], d[2], d[3], d[4], d[5]))
                else:
                    print ("{:<8} {:<20} {:<15} {:<15} {:<20} {:<20}".format(d[0], d[1], d[2], d[3], d[4], 'No discount'))
            return data
        else:
            print("--- !!! Failed to get product list !!! ---")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to get a list of products !!! ---")
        print(error)

def addProductByCustomer():
    print("\n")
    print("*"*40)
    print("Add Product to the shopping list")
    print("*"*40)
    
    p_id = int(input('Product id: '))
    p_quantity = int(input('Quantity: '))

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute(f"SELECT p_id FROM product WHERE product.p_id = '{p_id}' ")
        pId = cur.fetchone()

        now = datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M")

        if pId:
            cur.execute("""
                INSERT INTO orders (o_product, o_quantity, o_customer, o_date)
                VALUES (%s, %s, %s, %s);
                """,
                (pId, p_quantity,1, dt)
            )
            cur.close()
            conn.commit()
            product.autoEditQuantity(p_id, p_quantity, 'de')
            print("Added new order.")
        else:
            print("Product id not found.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to add a order !!! ---")
        print(error)


def payPrice ():
    print("\n")
    print("*"*40)
    print("Total payment")
    print("*"*40)


    try:
        conn = db.connect()
        cur = db.cursor(conn)
        
        cur.execute("SELECT o_product FROM orders")
        p1 = cur.fetchone()

        cur.execute(f"SELECT p_basePrice FROM product WHERE p_id = {p1[0]}")
        price = cur.fetchone()

        if price:
            pay = input(f"Total price = {price[0]}. To pay Enter 1: ")
        else:
            print("--- !!! price not found !!! ---")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to see final payment !!! ---")
        print(error)


def seeOrder ():
    print("\n")
    print("*"*40)
    print("Order list")
    print("*"*40)

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute("SELECT * FROM orders")
        data = cur.fetchall()


        if data:
            print ("{:<8} {:<20} {:<15} {:<15}".format('Id','ProductId','Quantity','Price'))
            print("-"*92)
            for d in data:
                cur.execute(f"SELECT p_basePrice FROM product WHERE p_id = {d[1]}")
                pPrice = cur.fetchone()
                pPrice = pPrice[0]

                print ("{:<8} {:<20} {:<15} {:<15}".format(d[0], d[1], d[2], pPrice))
            return data
        else:
            print("--- !!! Failed to get product list !!! ---")

        cur.close()
        product.autoEditOrder(oId, 'in')
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to get a list of products !!! ---")
        print(error)


def deleteOrder():
    print("\n")
    print("*"*40)
    print("Delete the order!")
    print("*"*40)

    oId = int(input("Set order code/Id: "))

    try:
        conn = db.connect()
        cur = db.cursor(conn)
        
        cur.execute(f"SELECT o_quantity FROM orders WHERE o_id = {oId}")
        quantity = cur.fetchone()
        quantity = quantity[0]

        cur.execute(f"SELECT o_product FROM orders WHERE o_id = {oId}")
        pId = cur.fetchone()
        pId = pId[0]

        cur.execute(f"DELETE FROM orders WHERE o_id = {oId}")

        cur.close()
        conn.commit()
        product.autoEditQuantity(pId, quantity, 'in')
        print("order is deleted.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to delete the product !!! ---")
        print(error)