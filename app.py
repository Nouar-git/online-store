import tables
import admin
import customer

# Start with creating all tables nedded for the application.
tables.createTables()

while 1:
    print("\n")
    print("*"*40)
    print("Welcom to Online Store!")
    print("*"*40)

    print("1.Admin")
    print("2.Customer")
    ch = int(input("Enter your choice (1 or 2): "))
    if ch == 1:
        admin.start()
    elif ch == 2:
        customer.start()
    else:
        print("Wrong Choice, try again!")
