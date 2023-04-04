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
                customer_id SERIAL PRIMARY KEY,
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
                name VARCHAR ( 50 ) UNIQUE PRIMARY KEY,
                phonenumber INT NOT NULL,
                address VARCHAR (200) NOT NULL,
                postnr INT NOT NULL,
                city VARCHAR (50),
                country VARCHAR (50)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS discount(
                d_id SERIAL UNIQUE PRIMARY KEY,
                d_precent INT NOT NULL,
                d_name VARCHAR (55) NOT NULL,
                d_startDate INT NOT NULL,
                d_endDate INT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS product (
                p_id SERIAL UNIQUE PRIMARY KEY,
                p_name VARCHAR (55) NOT NULL,
                p_quantity INT,
                p_basePrice INT,
                p_supplier VARCHAR NOT NULL,
                p_discount INT,
                FOREIGN KEY (p_supplier) REFERENCES supplier (name),
                FOREIGN KEY (p_discount) REFERENCES discount (d_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                o_id SERIAL UNIQUE PRIMARY KEY,
                o_product INT NOT NULL,
                o_quantity INT NOT NULL,
                o_customer INT NOT NULL,
                o_confirmed VARCHAR (50) DEFAULT 'False',
                o_date VARCHAR (55) NOT NULL,
                FOREIGN KEY (o_product) REFERENCES product (p_id)
            )
            """
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
