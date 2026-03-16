from criptoapp import app
from flask import render_template, request, flash, redirect
from models import select_all, insert
from datetime import datetime

@app.route("/")
def inicio():
    movimientos = select_all()
    return render_template("index.html", datos=movimientos)

@app.route("/compras", methods=['GET','POST'])
def compra():
    if request.method == 'POST':
        #Aquí se recoge lo que viene del formulario
        moneda_venta = request.form.get('from_currency')
        moneda_cantidad = request.form.get('from_quantity')
        moneda_compra = request.form.get('to_currency')

        #Validación si las monedas son las mismas
        if moneda_venta == moneda_compra:
            #si son iguales salta un error
            return render_template("compras.html", error ="Cambie una de las monedas")
        #Si todo va bien seguimos
        fecha_hora = datetime.now()
        nuevo_movimiento = {
            "date": fecha_hora.strftime("%Y-%m-%d"),
            "time": fecha_hora.strftime("%H:%M:%S"),
            "from_currency": moneda_venta,
            "from_quantity":  moneda_cantidad,
            "to_currency": moneda_compra,
            "to_quantity": 1.0 #Esto lo calcularemos con la API más adelante
        }
        insert(nuevo_movimiento)
        return redirect("/")
    return render_template("compras.html")

@app.route("/cartera")
def cartera():
    return render_template("cartera.html")