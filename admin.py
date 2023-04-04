import dbConnect as db
import product
import dicounts
import customer

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
        print("9. See discount history for discounted products")
        print("10. See a list of all new orders")
        print("11. Confirm order")
        print("12. See a list of products with maximum orders in each month")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            addSupplier()
        elif ch == 2:
            print("*"*40)
            product.addProduct()
        elif ch == 3:
            product.editQuantity()
        elif ch == 4:
            product.deleteProduct()
        elif ch == 5:
            product.getList()
        elif ch == 6:
            product.searchProduct()
        elif ch == 7:
            dicounts.addDiscount()
        elif ch == 8:
            dicounts.addedDiscounts()
        elif ch == 9:
            dicounts.seeHistory()
        elif ch == 10:
            product.SeeNewOrders()
        elif ch == 11:
            product.confirmOrder()
        elif ch == 12:
            product.listMaximumOrdersInEachMonth()
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

        print("\n")
        print("Add new Supplier ...")
        cur.execute("""
            INSERT INTO Supplier (name, address, postnr, phonenumber, city, country)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (str(name), str(address), int(postnr), int(phonenumber), str(city), str(country))
        )
        cur.close()
        conn.commit()
        print("New Supplier registered.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to add new supplier !!! ---")
        print(error)
