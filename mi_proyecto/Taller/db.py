import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="taller_mecanico_dj",
        port=3308
    )