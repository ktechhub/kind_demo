import mysql.connector
from datetime import datetime
from config import db_host, db_name, db_password, db_port, db_user

# create connection
conn = mysql.connector.connect(
    host=db_host, user=db_user, password=db_password, port=db_port, database=db_name
)

# get cursor
cur = conn.cursor()

# create a database
cur.execute("CREATE DATABASE mydatabase")

# list databases
cur.execute("SHOW DATABASES")
for x in cur:
    print(x)

# create a table
cur.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

# list tables
cur.execute("SHOW TABLES")
for x in cur:
    print(x)
