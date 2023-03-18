import dbConnect as db

def addProduct():
    print("\n")
    print("*"*40)
    print("Add Product")
    print("*"*40)
    
    p_name = input(str('Product name: '))
    p_quantity = input(int('Quantity: '))
    p_basePrice = input(int('Base price: '))
    p_supplier = input(str('Supplier: '))
    p_discount = input(int('Discount: '))

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

        if supplier:
            print("Add Product ...")
            cur.execute("""
                INSERT INTO product (p_name, p_quantity, p_basePrice, p_supplier)
                VALUES (%s, %s, %s, %s);
                """,
                (str(p_name), int(p_quantity), int(p_basePrice), str(p_supplier))
            )
            cur.close()
            conn.commit()
            print("New product is added.")
        else:
            print('Supplier not found, list product to find out the supplier names')
        
        if supplier and discount:
            cur.execute("""
                INSERT INTO product (p_discount)
                VALUES (%s);
                """,
                (int(p_discount))
            )
            cur.close()
            conn.commit()
        else:
            print("Discount not found")
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
            cur.execute(f"SELECT * FROM product WHERE p_code = {sq}")
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

        cur.execute(f"DELETE FROM product WHERE p_code = {pId}")

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