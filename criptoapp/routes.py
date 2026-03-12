from criptoapp import app
from flask import render_template
from models import select_all

@app.route("/")
def inicio():
    movimientos = select_all()
    return render_template("index.html", datos=movimientos)

@app.route("/compras")
def compra():
    return render_template("compras.html")

@app.route("/cartera")
def cartera():
    return render_template("cartera.html")