import psycopg2

def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="pgserver.mau.se",
            port="5432",
            database="ag3907",
            user="ag3907",
            password="abv317ij"
        )

	    # Return cur
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def close(cur):
    # close the communication with the PostgreSQL
    return cur.close()

def cursor(conn):
    # Create a cursor
    return conn.cursor()
