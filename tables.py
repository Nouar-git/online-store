import dbConnect as db

def createTables():
    try:
        # Connect to DB
        conn = db.connect()
        # Create a cursor
        cur = db.cursor(conn)

        # Create tables.
        tables = (
            """
            CREATE TABLE IF NOT EXISTS Customer (
                customer_id serial PRIMARY KEY,
                fname VARCHAR ( 50 ) NOT NULL,
                lname VARCHAR ( 50 ) NOT NULL,
                email VARCHAR (100) UNIQUE NOT NULL,
                address VARCHAR (200) NOT NULL,
                city VARCHAR (50) NOT NULL,
                country VARCHAR (50) NOT NULL,
                phonenumber INT NOT NULL
            )
            """,
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
        print("--- !!! Error on tables.py !!! ---")
        print(error)
