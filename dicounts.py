import dbConnect as db

def addDiscount():
    print("\n")
    print("*"*40)
    print("Add discounts!")
    print("*"*40)
    
    d_precent = int(input('Precentage: '))
    d_name = input('Discount name: ')
    d_startDate = int(input('Start date(YYYYMMDD): '))
    d_endDate = int(input('End date(YYYYMMDD): '))

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute("""
            INSERT INTO discount (d_precent, d_name, d_startDate, d_endDate)
            VALUES (%s, %s, %s, %s);
            """,
            (d_precent, d_name, d_startDate, d_endDate)
        )
        cur.close()
        conn.commit()
        print("New discount is added.")
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to add a discount !!! ---")
        print(error)


def getDiscountPrice(price, discount):
    sum = price * (100 - discount) / 100
    return sum

def seeHistory ():
    print("\n")
    print("*"*40)
    print("Discounts' History")
    print("*"*40)

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute("""
            SELECT product.p_id, product.p_name, product.p_basePrice, discount.d_id, discount.d_name, discount.d_precent, discount.d_startDate, discount.d_endDate
            FROM product
            INNER JOIN discount ON product.p_discount=discount.d_id
        """)
        data = cur.fetchall()

        if data:
            print ("{:<15} {:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<13} {:<15}".format('Product id', 'Product name', 'BasePrice', 'Discounted prise', 'Discount id', 'Discount name', 'Discount %', 'D_startDate', 'D_endDate'))
            print("-"*140)
            for d in data:
                discounPrise = getDiscountPrice(d[2], d[5])
                print ("{:<15} {:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<13} {:<15}".format(d[0], d[1], d[2], discounPrise, d[3], d[4], d[5], d[6], d[7]))
                
            return data
        else:
            print("--- !!! Failed to get discount list !!! ---")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to get a list of discounts !!! ---")
        print(error)
