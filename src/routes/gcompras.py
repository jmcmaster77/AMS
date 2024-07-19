from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user
from models.ModelComprasdb import Compras
from models.ModelProveedoresdb import Proveedores
from models.ModelProductosdb import Productos
from datetime import datetime
from utils.db import db
from utils.log import logger
import json
import jinja2
import pdfkit
import os


gcomp = Blueprint("gcompras", __name__)


@gcomp.route("/compras")
@login_required
def compras():
    registros = Compras.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y")
            registro.fechaf = registro.fechaf.strftime("%d/%m/%y")

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
        if request.form['proveedor'] == "":
            flash({'title': "AMS", 'message': "Seleccionar Proveedor: "}, 'warning')
            return redirect(url_for("gcompras.registro_compras"))
        data = {}
        data["productos"] = []

        for x in range(int(request.form["item"])):
            if x == 0:
                # print("Producto: ",request.form["producto"], "Cantidad: ", request.form["cantidad"], "Costo: ", request.form["costo"])
                pdata = Productos.query.filter_by(
                    nombre=request.form['producto']).first()
                data["productos"].append({
                    "id": pdata.id,
                    "nombre": request.form["producto"],
                    "cantidad": int(request.form["cantidad"]),
                    "costo": float(request.form["costo"])
                })
                if pdata.cantidad == 0:

                    pdata.cantidad = int(request.form["cantidad"])
                    pdata.costo = float(request.form["costo"])
                    pdata.precio = float(
                        request.form["costo"]) * ((pdata.porcentaje/100)+1)

                else:
                    pdata.cantidad = pdata.cantidad + \
                        int(request.form["cantidad"])
                    pdata.costo = float(request.form["costo"])
                    pdata.precio = float(
                        request.form["costo"]) * ((pdata.porcentaje/100)+1)

                totalc = float(request.form["costo"]) * \
                    int(request.form["cantidad"])
                # print("data:",data)
                # print("Data JSON: ", json.dumps(data))
            else:
                # print(f"Producto "+str(x)+": ",request.form[f"producto"+str(x)], "Cantidad: ", request.form[f"cantidad"+str(x)], "Costo: ", request.form[f"costo"+str(x)])
                pdata = Productos.query.filter_by(
                    nombre=request.form[f"producto"+str(x)]).first()
                if pdata.cantidad == 0:

                    data["productos"].append({
                        "id": pdata.id,
                        "nombre": request.form[f"producto"+str(x)],
                        "cantidad": int(request.form[f"cantidad"+str(x)]),
                        "costo": float(request.form[f"costo"+str(x)])
                    })
                    pdata.cantidad = int(request.form[f"cantidad"+str(x)])
                    pdata.costo = float(request.form[f"costo"+str(x)])
                    pdata.precio = float(
                        request.form[f"costo"+str(x)]) * ((pdata.porcentaje/100)+1)

                else:
                    data["productos"].append({
                        "id": pdata.id,
                        "nombre": request.form[f"producto"+str(x)],
                        "cantidad": int(request.form[f"cantidad"+str(x)]),
                        "costo": float(request.form[f"costo"+str(x)])
                    })
                    pdata.cantidad = pdata.cantidad + \
                        int(request.form[f"cantidad"+str(x)])
                    pdata.costo = float(request.form[f"costo"+str(x)])
                    pdata.precio = float(
                        request.form[f"costo"+str(x)]) * ((pdata.porcentaje/100)+1)

                totalc = totalc + \
                    (float(request.form[f"costo"+str(x)])
                     * int(request.form[f"cantidad"+str(x)]))

        provdata = Proveedores.query.filter_by(
            fullname=request.form['proveedor']).first()
        # print("Proveedor id", str(provdata.id) + " | " + provdata.fullname )
        # print("Data JSON: ", json.dumps(data))
        # print("Total Compra: ", "%.2f" %totalc)
        fecha = datetime.now()
        fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        if request.form["tcompra"] == "Contado":
            pagado = True
        else:
            pagado = False
        nfact = request.form["nfact"]
        fechaf = datetime.strptime(request.form["fechaf"], "%d/%m/%Y")

        compra = Compras(provdata.id, nfact, fechaf, data,
                         request.form["tcompra"], request.form["mpago"], pagado, totalc, fecha, False,  current_user.id)
        db.session.add(compra)
        db.session.commit()

        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Registro compra id " + str(compra.id))
        flash({'title': "AMS", 'message': "Compra: " +
               "id " + str(compra.id) + " registrado satisfactoriamente"}, 'success')
        return redirect(url_for("gcompras.compras"))


@gcomp.route("/comprobantec/<id>")
@login_required
def comprobantec(id):
    # obteniendo datos de la compra
    compradata = Compras.query.get(id)
    # obteniendo datos del proveedor
    provdata = Proveedores.query.get(compradata.id_p)
    fechac = compradata.fecha.strftime("%d/%m/%Y")
    fechaf = compradata.fechaf.strftime("%d/%m/%Y")

    return render_template("comprobantes/comprobante.html", compra=compradata, provdata=provdata, fechac=fechac, fechaf=fechaf)


def creaPdf(ruta_template, compradata, provdata, fechac, fechaf):
    template_name = ruta_template.split('\\')[-1]
    ruta_template = ruta_template.replace(template_name, '')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(template_name)
    rutaimglogo = os.path.abspath(f"src/static/ico/store-svgrepo-com2.svg")
    html = template.render(compra=compradata, provdata=provdata, fechac=fechac, fechaf=fechaf)
    
    options = {
        "page-size" : "Letter",
        "margin-top" : "0.5in",
        "margin-bottom" : "0.5in", 
        "margin-right" : "0.5in",
        "margin-left" : "0.5in",
        "encoding" : "UTF-8",
        "enable-local-file-access": None
    }
        # para posible implementacion 
    # file_name = 'invoice.pdf'
    # pdf_path = os.path.join(settings.BASE_DIR, 'static', 'pdf', file_name)
    
    # ummm 
    # return FileResponse(open(pdf_path, 'rb'), filename=file_name, content_type='application/pdf')

    #config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf") 
    rutaarchivo = os.path.abspath(f"src/static/ext/bin/wkhtmltopdf.exe")
    config = pdfkit.configuration(wkhtmltopdf=rutaarchivo) 
    ruta_salida = os.path.abspath(f"src/static/pdf/test.pdf")
    cssfile = os.path.abspath(f"src/static/css/comprobante.css")
    pdfkit.from_string(html, ruta_salida, options=options, configuration=config)

    # print(html)
    return html


@gcomp.route("/comprobantectpdf/<id>")
@login_required
def comprobantectpdf(id):
    # obteniendo datos de la compra
    compradata = Compras.query.get(id)
    # obteniendo datos del proveedor
    provdata = Proveedores.query.get(compradata.id_p)
    fechac = compradata.fecha.strftime("%d/%m/%Y")
    fechaf = compradata.fechaf.strftime("%d/%m/%Y")
    
    # rutaarchivo = os.path.abspath(f"src/static/img/productos/")
    ruta_template = "C:\\CODE\\AMS\\src\\templates\\comprobantes\\comprobantepdf.html" # 'C:\CODE\AMS\src\templates\comprobantes\comprobante.html'
    #template = "comprobante.html"

    respuesta = creaPdf(ruta_template, compradata,
                       provdata, fechac, fechaf)

    # return render_template("comprobantes/comprobante.html", compra=compradata, provdata=provdata, fechac=fechac, fechaf=fechaf)
    return respuesta 