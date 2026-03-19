from criptoapp import app
from flask import render_template, request, flash, redirect
from models import select_all, insert, consultar_saldo, obtener_precio_api
from datetime import datetime

@app.route("/")
def inicio():
    movimientos = select_all()
    return render_template("index.html", datos=movimientos)

@app.route("/compras", methods=['GET','POST'])
def compra():
    #Pongo variables para que el HTML no explote si no hay datos
    sel_from = "" #Es la moneda para vender
    v_from = "" #Es la cantidad numérica 
    sel_to = ""  #Es la moneda para comprar
    cantidad_calculada = "" #Es el resultado de la API

    if request.method == 'POST':
        #Se recoge todo lo que hay en el formulario
        moneda_venta = request.form.get('from_currency')
        moneda_compra = request.form.get('to_currency')
           
        #Saco el numero fuera para que este libre para ambos botones
        try:
            from_quant = float(request.form.get('from_quantity'))
        except:
            from_quant = 0.0

        #Botón calcular    
        if "btn_calcular" in request.form:
            if from_quant <= 0:
                return render_template("compras.html", error="Introduce una cantidad", sel_from=moneda_venta, sel_to=moneda_compra)

            # Llamamos a la función de models.py
            precio_real = obtener_precio_api(from_quant, moneda_venta, moneda_compra)
            
            if precio_real:
                #Volvemos a mostrar el formulario pero con los datos para que no se borren.
                return render_template("compras.html", cantidad_calculada=precio_real,
                                                       sel_to=moneda_compra,
                                                       sel_from=moneda_venta,
                                                       v_from=from_quant)
            else:
                return render_template("compras.html", error="No se pudo obtener el precio de la API", sel_from=moneda_venta, sel_to=moneda_compra, v_from=from_quant)

        #Botón comprar
        else:
            to_quant = request.form.get('to_quantity')

            # VALIDACIÓN: Si el usuario intenta comprar sin calcular, moneda_cantidad_recibida estará vacío
            if not to_quant or to_quant == "":
                return render_template("compras.html", error="Debes calcular el precio antes de comprar", 
                                       sel_from=moneda_venta, sel_to=moneda_compra, v_from=from_quant)
            
            moneda_cantidad_recibida = float(to_quant)

            # VALIDACIÓN DE SALDO (Excepto para Euros)
            if moneda_venta != "EUR":
                saldo_actual = consultar_saldo(moneda_venta)
                if from_quant > saldo_actual:
                    return render_template("compras.html", error=f"Saldo insuficiente. Solo tienes {saldo_actual} {moneda_venta}",
                                            sel_from=moneda_venta, sel_to=moneda_compra, v_from=from_quant, cantidad_calculada=to_quant)

            #Validación si las monedas son las mismas
            if moneda_venta == moneda_compra:
                #si son iguales salta un error
                return render_template("compras.html", error ="Cambie una de las monedas",
                                       #Al pasarle todas esas variables, le estamos devolviendo al usuario sus propios datos
                                       sel_from=moneda_venta, sel_to=moneda_compra, v_from=from_quant, cantidad_calculada=to_quant)
            #Si todo va bien guardamos
            fecha_hora = datetime.now()
            nuevo_movimiento = {
                "date": fecha_hora.strftime("%Y-%m-%d"),
                "time": fecha_hora.strftime("%H:%M:%S"),
                "from_currency": moneda_venta,
                "from_quantity":  from_quant,
                "to_currency": moneda_compra,
                "to_quantity": moneda_cantidad_recibida
            }
            insert(nuevo_movimiento)
            return redirect("/")
    return render_template("compras.html")

@app.route("/cartera")
def cartera():
    return render_template("cartera.html")