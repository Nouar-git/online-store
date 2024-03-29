import dbConnect as db
from datetime import datetime

def addProduct():
    print("\n")
    print("*"*40)
    print("Add Product")
    print("*"*40)
    
    p_name = str(input('Product name: '))
    p_quantity = int(input('Quantity: '))
    p_basePrice = int(input('Base price: '))
    p_supplier = str(input('Supplier name: '))
    p_discount = input('Discount id: ')

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        supplier = None
        if p_supplier:
            cur.execute(f"SELECT name FROM supplier WHERE name = '{p_supplier}'")
            supplier = cur.fetchone()

        discount = None
        if p_discount:
            cur.execute(f"SELECT d_id FROM discount WHERE d_id = '{p_discount}'")
            discount = cur.fetchone()

        print("Add Product ...")
        if supplier and discount:
            cur.execute("""
                INSERT INTO product (p_name, p_quantity, p_basePrice, p_supplier, p_discount)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (p_name, p_quantity, p_basePrice, p_supplier, p_discount)
            )
        elif supplier:
            cur.execute("""
                INSERT INTO product (p_name, p_quantity, p_basePrice, p_supplier)
                VALUES (%s, %s, %s, %s);
                """,
                (p_name, p_quantity, p_basePrice, p_supplier)
            )
        else:
            print('Supplier or discount not found, list to find out the name or id.')

        cur.close()
        conn.commit()
        print("New product is added.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to add a product !!! ---")
        print(error)

def getList ():
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
            print ("{:<8} {:<20} {:<15} {:<15} {:<20}".format('Id','Name','Quantity','Price','Supplier'))
            print("-"*80)
            for d in data:
                print ("{:<8} {:<20} {:<15} {:<15} {:<20}".format(d[0], d[1], d[2], d[3], d[4]))
                
            return data
        else:
            print("--- !!! Failed to get product list !!! ---")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to get a list of products !!! ---")
        print(error)

def searchProduct():
    print("\n")
    print("*"*40)
    print("Search")
    print("*"*40)

    sq = input("Search on id,name or suplier: ")

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        if sq.isdigit():
            cur.execute(f"SELECT * FROM product WHERE p_id = {sq}")
        else:
            cur.execute("""
                SELECT * FROM product
                WHERE p_name LIKE %s OR p_supplier LIKE %s
                """,
                ('%'+str(sq)+'%', '%'+str(sq)+'%')
            )

        data = cur.fetchall()

        if data:
            print ("{:<8} {:<20} {:<15} {:<15} {:<20}".format('Id','Name','Quantity','Price','Supplier'))
            print("-"*80)
            for d in data:
                print ("{:<8} {:<20} {:<15} {:<15} {:<20}".format(d[0], d[1], d[2], d[3], d[4]))
            return data
        else:
            print("--- !!! Could not find any result !!! ---")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to search !!! ---")
        print(error)
    
def deleteProduct():
    print("\n")
    print("*"*40)
    print("Delete a product!")
    print("*"*40)

    pId = int(input("Set product code/Id: "))

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute(f"DELETE FROM product WHERE p_id = {pId}")

        cur.close()
        conn.commit()
        print("product is deleted.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to delete the product !!! ---")
        print(error)

def editQuantity():
    print("\n")
    print("*"*40)
    print("Edit the quantity of a product!")
    print("*"*40)

    pId = int(input("Set product code/Id: "))
    pQ = int (input("Edit the quantity of a product: "))

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute(f"UPDATE product SET p_quantity = {pQ} WHERE p_id = {pId}")

        cur.close()
        conn.commit()
        print("Quantity is edited.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to edit the quantity !!! ---")
        print(error)

def autoEditQuantity (productId, pq, deOrIn):
    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute(f"SELECT p_quantity FROM product WHERE p_id =  '{productId}'")
        quantity = cur.fetchone()

        result = 0
        if quantity:
            if deOrIn == 'de':
                result = quantity[0] - pq
            else:
                result = quantity[0] + pq
            
            try:
                conn = db.connect()
                cur = db.cursor(conn)

                cur.execute(f"UPDATE product SET p_quantity = {result} WHERE p_id = {productId}")
                conn.commit()
            except (Exception, db.psycopg2.DatabaseError) as error:
                print("*"*40)
                print("--- !!! Failed to edite the quantity 2 !!! ---")
                print(error)

        cur.close()
        print("Quantity is edited.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to edite the quantity 1 !!! ---")
        print(error)


def SeeNewOrders ():
    print("\n")
    print("*"*40)
    print("List of all orders")
    print("*"*40)

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute("SELECT * FROM orders")
        data = cur.fetchall()

        if data:
            print ("{:<8} {:<20} {:<15} {:<15} {:<20}".format('Id','productId','Quantity','Price','Confirmed'))
            print("-"*80)
            for d in data:
                cur.execute(f"SELECT p_basePrice FROM product WHERE p_id = {d[1]}")
                pPrice = cur.fetchone()
                pPrice = pPrice[0]
                print ("{:<8} {:<20} {:<15} {:<15} {:<20}".format(d[0], d[1], d[2], pPrice, d[4]))
                
            return data
        else:
            print("--- !!! Failed to show orders list !!! ---")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to get a list of new orders !!! ---")
        print(error)

def autoEditOrder (orderId, de):
    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute(f"SELECT o_quantity FROM orders WHERE o_id = '{orderId}'")
        order = cur.fetchone()

        result = 0
        if order:
            if de == 'de':
                result = order[0] - 1
            
            try:
                conn = db.connect()
                cur = db.cursor(conn)

                cur.execute(f"UPDATE orders SET o_quantity = {result} WHERE o_id = '{orderId}'")
                conn.commit()

            except (Exception, db.psycopg2.DatabaseError) as error:
                print("*"*40)
                print("--- !!! Failed to edite the quantity2 !!! ---")
                print(error)

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to edite the quantity 1 !!! ---")
        print(error)


def confirmOrder():
    print("\n")
    print("*"*40)
    print("Confirm an order!")
    print("*"*40)

    oId = int(input("Set order nr/Id: "))

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute(f"UPDATE orders SET o_confirmed = 'True' WHERE o_id = {oId}")

        cur.close()
        conn.commit()
        print("The order is confirmed.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to confirm the order !!! ---")
        print(error)

def listMaximumOrdersInEachMonth():
    print("\n")
    print("*"*40)
    print("List of products with maximum orders in each month!")
    print("*"*40)

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute("SELECT * FROM orders ORDER BY o_quantity ASC")
        data = cur.fetchall()

        if data:
            print ("{:<8} {:<10} {:<15} {:<15}".format('Year','Month','Product Id','Quantity'))
            print("-"*50)
            for d in data:
                if d[4] == 'False':
                    continue
                else:
                    dt = datetime.strptime(d[5], '%Y-%m-%d %H:%M')
                    print ("{:<8} {:<10} {:<15} {:<15}".format(dt.year, dt.month, d[1], d[2]))
        else:
            print("--- !!! Failed to show a list maximum orders !!! ---")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to list maximum orders !!! ---")
        print(error)