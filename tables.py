import dbConnect as db

# Connect to DB
conn = db.connect()
# Create a cursor
cur = db.cursor(conn)

def create_tables():
    tables = (
        '''
        CREATE TABLE IF NOT EXIST admin (
            admin_id serial PRIMARY KEY, 
            username VARCHAR ( 50 ) UNIQUE NOT NULL,
            password VARCHAR ( 50 ) NOT NULL
        )
        ''',
    )

    conn = None
    try:
        # create table one by one
        for table in tables:
            cur.execute(table)

        # close communication with the PostgreSQL database server
        cur.close()

        # commit the changes
        conn.commit()
    except (Exception, db.psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
