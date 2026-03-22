# Proyecto Final: Aplicación de Gestión de Criptomonedas
Programa hecho en Python utilizando el framework Flask y SQLite para la gestión de una cartera de inversiones con consulta de precios en tiempo real.

# Instalación
Crear un entorno virtual de Python, activarlo e instalar las dependencias:
pip install -r requirements.txt

# Las librerías principales utilizadas son:

Flask (Framework web): https://flask.palletsprojects.com

Requests (Para consultas a la API): https://requests.readthedocs.io

Flask-SQLite: Gestión de base de datos local

# Configuración
Es necesario disponer de una API Key de CoinAPI.io.

La clave debe configurarse en el archivo config.py o en la variable de entorno correspondiente para que las consultas de precio funcionen correctamente.

# Ejecución del programa
Inicializar parámetros para el servidor de Flask en Windows:
set FLASK_APP=main.py

Comando para ejecutar el servidor por defecto (puerto 5000):
flask --app main run

Comando para ejecutar el servidor en un puerto diferente (ejemplo puerto 5002):
flask --app main run -p 5002

Comando para activar el modo debug (recarga automática al detectar cambios):
flask --app main run --debug

# Estructura del Proyecto
index.html: Listado de movimientos (Inicio).

compras.html: Formulario de intercambio con validaciones de saldo y cálculo de precio unitario.

cartera.html: Estado actual de la inversión con cálculo de ganancias/pérdidas.

models.py: Lógica de acceso a datos y consultas a la API externa.

# Funcionalidades

Inicio: Registro histórico de movimientos.

Compra: Formulario con validación de saldo, control de monedas duplicadas y visualización de precio unitario.

Cartera: Estado de la inversión con cálculo de valor actual y balance de ganancias/pérdidas en color (verde/rojo).