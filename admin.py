import dbConnect as db

# Connect to DB
conn = db.connect()
# Create a cursor
cur = db.cursor(conn)

# 1 - Create Admin table
print("Create Admin table ...")
q = "CREATE TABLE IF NOT EXISTS admin (admin_id serial PRIMARY KEY, username VARCHAR ( 50 ) UNIQUE NOT NULL, password VARCHAR ( 50 ) NOT NULL);"
cur.execute(q)
# 2 - Add an Admin to DB/Admin table
print("Insert into Admin table ...")
q = "INSERT INTO admin (username, password) VALUES ({}, {});".format("'Noor3'", "'123abc'")
cur.execute(q)
# 3 - Get the latest created admin info from DB
print("Select from Admin table ...")
q = "SELECT * FROM admin;"
cur.execute(q)
admins = cur.fetchall()
print(admins)

cur.close()
conn.commit()





