import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='mlind',
        password='123',
        database='mlind',
        port=3306
    )
    if connection.is_connected():
        print("Successfully connected to the database")
except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        connection.close()