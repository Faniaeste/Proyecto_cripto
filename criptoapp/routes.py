from criptoapp import app
from flask import render_template, request, flash, redirect
from models import select_all

@app.route("/")
def inicio():
    movimientos = select_all()
    return render_template("index.html", datos=movimientos)

@app.route("/compras", methods=['GET','POST'])
def compra():
    if request.method == 'POST':
        moneda_venta = request.form.get('from_currency')
        moneda_compra = request.form.get('to_currency')

        if moneda_venta == moneda_compra:
            print("Error: No puedes cambiar la misma moneda")
            return render_template("compras.html", error="Las monedas no pueden ser iguales.")
        return redirect("/")
        
    return render_template("compras.html")
            

@app.route("/cartera")
def cartera():
    return render_template("cartera.html")