import customer

while 1:
    print("\n")
    print("*"*40)
    print("Welcom to Online Store!")
    print("*"*40)

    print("1.Admin")
    print("2.Customer")
    ch = int(input("Enter your choice (1 or 2): "))
    if ch == 1:
        print("*"*40)
        print('TODO fix Admin function .....')
    elif ch == 2:
        customer.start()
    else:
        print("Wrong Choice, try again!")
