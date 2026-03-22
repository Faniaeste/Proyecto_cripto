from criptoapp import app
from flask import render_template, request, flash, redirect
from models import select_all, insert, consultar_saldo, obtener_precio_api, obtener_total_cartera, obtener_totales_euros
from datetime import datetime

@app.route("/")
def inicio():
    movimientos = select_all()
    return render_template("index.html", datos=movimientos)

@app.route("/compras", methods=['GET','POST'])
def compra():
    #Pongo variables para que el HTML no explote si no hay datos
    moneda_venta = "" #Es la moneda para vender
    from_quant = "" #Es la cantidad numérica 
    moneda_compra = ""  #Es la moneda para comprar
    cantidad_calculada = "" #Es el resultado de la API
    saldo_v = 0.0 #Para mostrar el saldo de esa moneda
    precio_u = "" #Para el precio unitario

    if request.method == 'POST':
        #Se recoge todo lo que hay en el formulario
        moneda_venta = request.form.get('from_currency')
        moneda_compra = request.form.get('to_currency')

        #Calculamos el saldo de la moneda de venta
        saldo_v = consultar_saldo(moneda_venta)
           
        #Saco el numero fuera para que este libre para ambos botones
        try:
            from_quant = float(request.form.get('from_quantity'))
        except:
            from_quant = 0.0

        #Botón calcular    
        if "btn_calcular" in request.form:
            if moneda_venta == moneda_compra:
                return render_template("compras.html", error="Las monedas no pueden ser iguales", 
                               sel_from=moneda_venta, sel_to=moneda_compra, v_from=from_quant, saldo_v=saldo_v)

            if from_quant <= 0:
                saldo_v = consultar_saldo(moneda_venta)
                return render_template("compras.html", error="Introduce una cantidad", sel_from=moneda_venta, sel_to=moneda_compra, saldo_v=saldo_v)

            # Llamamos a la función de models.py
            precio_real = obtener_precio_api(from_quant, moneda_venta, moneda_compra)
            
            if precio_real:
                precio_u = precio_real / from_quant
                #Volvemos a mostrar el formulario pero con los datos para que no se borren.
                return render_template("compras.html", cantidad_calculada=precio_real,
                                                       sel_to=moneda_compra,
                                                       sel_from=moneda_venta,
                                                       v_from=from_quant,
                                                       saldo_v=saldo_v,
                                                       precio_u=precio_u)
            else:
                return render_template("compras.html", error="No se pudo obtener el precio de la API", sel_from=moneda_venta, sel_to=moneda_compra, v_from=from_quant)

        #Botón comprar
        else:
            to_quant = request.form.get('to_quantity')
            #Si la compra falla, y queremos volver a mostrar la pagina con todos
            #los datos ue ya teníamos, sino lo hacemos así al recuperar la página
            #saldría vacío y pareceria que se ubiera roto la página
            precio_u = request.form.get('precio_unitario_hidden')

            # VALIDACIÓN: Si el usuario intenta comprar sin calcular, moneda_cantidad_recibida estará vacío
            if not to_quant or to_quant == "":
                return render_template("compras.html", error="Debes calcular el precio antes de comprar", 
                                       sel_from=moneda_venta, sel_to=moneda_compra, v_from=from_quant)
            
            moneda_cantidad_recibida = float(to_quant)

            # VALIDACIÓN DE SALDO (Excepto para Euros)
            if moneda_venta != "EUR":
                if from_quant > saldo_v:
                    return render_template("compras.html", error=f"Saldo insuficiente. Solo tienes {saldo_v} {moneda_venta}",
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
    return render_template("compras.html",  sel_from=moneda_venta,
         sel_to=moneda_compra, fv_from=from_quant, cantidad_calculada=cantidad_calculada, saldo_v=saldo_v)

@app.route("/cartera")
def cartera():
    #Obtenemos las criptos y su valor actual en €
    mis_monedas = obtener_total_cartera()
    total_valor_euros = 0

    #Calculamos el valor total de cada una
    for item in mis_monedas:
        if item['symbol'] == "EUR":
            item['valor_actual'] = item['cantidad']
        else:
            #Consulto a la Api cuanto vale la moneda en EUR
            precio_en_euros = obtener_precio_api(item['cantidad'], item['symbol'], "EUR")
            if precio_en_euros:
                item['valor_actual'] = precio_en_euros
            else:
                item['valor_actual'] = 0

        total_valor_euros += item['valor_actual']
    #Obtengo los totales de inversión
    invertido, recuperado, valor_compra = obtener_totales_euros()

    return render_template("cartera.html", cartera=mis_monedas,
                            total_valor=total_valor_euros,
                             invertido=invertido,
                              recuperado=recuperado,
                               valor_compra=valor_compra, )