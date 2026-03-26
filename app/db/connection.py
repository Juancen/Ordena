import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="proyecto_ordena"
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None