import dbConnect as db
import product

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
            product.addProduct()
        elif ch == 5:
            product.getList()
        elif ch == 6:
            product.searchProduct()
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
