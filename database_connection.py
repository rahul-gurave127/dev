 import psycopg2
import sys

try:
    print("Connecting  Database...")
    conn = psycopg2.connect("host='127.0.0.1' port='5432' dbname='db_local' user='user123' password='12345678'")
    print("Database Connected.")
except psycopg2.Error:
    print("Failed to connect database.")
    print(sys.exc_info())
 
#- Create cursor to communication with database.
cur = conn.cursor()

try:
    print('Executing SQL Command.')
    query = "select * from table_name;"
    cur.execute(query)
    res = cur.fetchall()
    print(res)
except psycopg2.Error:
    print(sys.exc_info())

print("Process Completed")
