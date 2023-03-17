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


def seeHistory ():
    print("\n")
    print("*"*40)
    print("Discounts' History")
    print("*"*40)

    try:
        conn = db.connect()
        cur = db.cursor(conn)

        cur.execute("SELECT * FROM discount")
        data = cur.fetchall()

        if data:
            print ("{:<10} {:<15} {:<20} {:<20} {:<20}".format('d_id', 'd_precent', 'd_name', 'd_startDate', 'd_endDate'))
            print("-"*80)
            for d in data:
                print ("{:<10} {:<15} {:<20} {:<20} {:<20}".format(d[0], d[1], d[2], d[3], d[4]))
                
            return data
        else:
            print("--- !!! Failed to get discount list !!! ---")

        cur.close()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print("*"*40)
        print("--- !!! Failed to get a list of discounts !!! ---")
        print(error)
