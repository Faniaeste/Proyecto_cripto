import sqlite3
from config import DATABASE_PATH, SECRET_KEY
import requests 

#Esta función sirve para leer la base de datos
def select_all():
    conexion = sqlite3.connect(DATABASE_PATH)
    #Lo convierte en un "diccionario", así me quito el problema de las tuplas.
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT id, date, time, from_currency, from_quantity, to_currency, to_quantity FROM movements ORDER BY date DESC")
    datos = cursor.fetchall()
    conexion.close()
    return datos

#Esta sirve para insertar datos nuevos
def insert(movimiento):
    #Conecta con la base
    conexion = sqlite3.connect(DATABASE_PATH)
    cursor = conexion.cursor()
    
    #Los "?" son huecos que luego rellenamos, por seguridad.
    sql = """
        INSERT INTO movements (date, time, from_currency, from_quantity, to_currency, to_quantity)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    #Ejecutamos pasando los datos en orden
    cursor.execute(sql, (
        movimiento['date'],
        movimiento['time'],
        movimiento['from_currency'],
        movimiento['from_quantity'],
        movimiento['to_currency'],
        movimiento['to_quantity']
    ))
    
    #Aquí se guardan los cambios y se cierrar
    conexion.commit()
    conexion.close()


def consultar_saldo(moneda):
    conexion = sqlite3.connect(DATABASE_PATH)
    cursor = conexion.cursor()

    #Se suma la moneda
    cursor.execute("SELECT SUM(to_quantity) FROM movements WHERE to_currency = ?", (moneda,))
    resultado_entrada = cursor.fetchone()[0] or 0.0
    #[0] aquí le pido el primer compartimento porque viene en tuplas, aqnue solo haya 1 número
    #0.0 es para evitar que devuelva un None y pete el programa al intentar hacer la resta.


    #Se Suma lo que ha salido de esa moneda
    cursor.execute("SELECT SUM(from_quantity) FROM movements WHERE from_currency = ?", (moneda,))
    resultado_salida = cursor.fetchone()[0] or 0.0

    conexion.close()

    #Total es lo que entró menos lo que salió
    return resultado_entrada - resultado_salida

def obtener_precio_api(cantidad, moneda_venta, moneda_compra):
    #La URL para convertir monedas en criptos
    url = "https://pro-api.coinmarketcap.com/v2/tools/price-conversion"

    #amount: cantidad a convertir
    #symbol: la moneda que TIENES
    #convert: la moneda que QUIERES

    #Esto se envia a la API
    parametros = {
        'amount': cantidad,
        'symbol': moneda_venta,
        'convert': moneda_compra
    }
    cabeceras = {
        'X-CMC_PRO_API_KEY': SECRET_KEY
    }
    try:
        respuesta = requests.get(url, params=parametros, headers=cabeceras)
        dato_json = respuesta.json()
        
        #Primero accedo a data, posición 0, quote, moneda_compra, price.
        precio = dato_json['data'][0]['quote'][moneda_compra]['price']
        return precio
    #Para que no se rompa nada, si falla la api le doy un error.

    except Exception as e:
        print("Vaya, no ay conexión con la API", e)
        return None

 
