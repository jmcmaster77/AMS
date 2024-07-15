from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from models.ModelComprasdb import Compras
from models.ModelProveedoresdb import Proveedores
from models.ModelProductosdb import Productos
from datetime import datetime
from utils.db import db
from utils.log import logger
import json

gcomp = Blueprint("gcompras", __name__)


@gcomp.route("/compras")
@login_required
def compras():
    registros = Compras.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gcompras/compras.html", compras=registros, deleted=False)
    else:
        return render_template("gcompras/compras.html", compras=registros, deleted=False)


@gcomp.route("/compras_deleted")
@login_required
def compras_deleted():
    registros = Compras.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gcompras/compras.html", compras=registros, deleted=True)
    else:
        return render_template("gcompras/compras.html", compras=registros, deleted=True)

@gcomp.route("/rcompras", methods=["GET", "POST"])
@login_required
def registro_compras():
    if request.method == "GET":
        proveedores = Proveedores.query.all()
        if proveedores is not None:
            productos = Productos.query.all()
            return render_template("gcompras/rcompra.html", proveedores=proveedores, productos=productos) 
        else: 
            return render_template("gcompras/rcompra.html", proveedores="No") 
        
    else:


        # print("datos recibidos", request.form)
        # print("Proveedor: ", request.form["proveedor"])
        # print("Cantidad de Item: ", request.form["item"])

        data = {}
        data["productos"] = []
        
        for x in range(int(request.form["item"])):
            if x == 0:
                # print("Producto: ",request.form["producto"], "Cantidad: ", request.form["cantidad"], "Costo: ", request.form["costo"])
                pdata = Productos.query.filter_by(nombre=request.form['producto']).first()
                data["productos"].append({
                    "id": pdata.id,
                    "nombre": request.form["producto"],
                    "cantidad":int(request.form["cantidad"]),
                    "costo":float(request.form["costo"])
                })
                totalc = float(request.form["costo"]) * int(request.form["cantidad"])
                # print("data:",data)
                # print("Data JSON: ", json.dumps(data))
            else:
                # print(f"Producto "+str(x)+": ",request.form[f"producto"+str(x)], "Cantidad: ", request.form[f"cantidad"+str(x)], "Costo: ", request.form[f"costo"+str(x)])
                pdata = Productos.query.filter_by(nombre=request.form[f"producto"+str(x)]).first()
                data["productos"].append({
                    "id": pdata.id,
                    "nombre": request.form[f"producto"+str(x)],
                    "cantidad":int(request.form[f"cantidad"+str(x)]),
                    "costo":float(request.form[f"costo"+str(x)])
                })
                totalc = totalc + (float(request.form[f"costo"+str(x)]) * int(request.form[f"cantidad"+str(x)]))
        provdata = Proveedores.query.filter_by(fullname=request.form['proveedor']).first()
        print("Proveedor id", str(provdata.id) + " | " + provdata.fullname )
        print("Data JSON: ", json.dumps(data))
        print("Total Compra: ", "%.2f" %totalc)
        fecha = datetime.now()
        fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")

        compra = Compras(provdata.id, data, request.form["tcompra"], request.form["mpago"], True, totalc, fecha, False,  current_user.id)
        db.session.add(compra)
        db.session.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Registro compra id dev")
        flash({'title': "AMS", 'message': "Compra: " +
                "id dev" + " registrado satisfactoriamente"}, 'success')
        return redirect(url_for("gcompras.compras"))