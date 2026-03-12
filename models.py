import sqlite3
from config import DATABASE_PATH


def select_all():
    conexion = sqlite3.connect(DATABASE_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, date, time, from_currency, from_quantity, to_currency, to_quantity FROM movements ORDER BY date DESC")
    datos = cursor.fetchall()
    conexion.close()
    return datos