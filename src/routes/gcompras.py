from flask import Blueprint, request, redirect, url_for, render_template, flash, send_from_directory
from flask_login import login_required, current_user
from models.ModelComprasdb import Compras
from models.ModelProveedoresdb import Proveedores
from models.ModelProductosdb import Productos
from models.ModelReversosdb import Reversos
from datetime import datetime
from utils.db import db
from utils.log import logger
import json
import jinja2
import pdfkit
import os
from config import ipserver


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
            registro.fechaf = registro.fechaf.strftime("%d/%m/%y")

        return render_template("gcompras/compras.html", compras=registros, deleted=True)
    else:
        return render_template("gcompras/compras.html", compras=registros, deleted=True)


def cal_porcentaje(precio, costo):

    diferencia = (float(precio) - float(costo))
    porcentaje = (diferencia / float(precio))*100
    return porcentaje


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
                    # almacenando los datos existente antes de la compra
                    cantidaexi = pdata.cantidad
                    costoexi = pdata.costo
                    precioexi = pdata.precio
                    pdata.cantidad = int(request.form["cantidad"])
                    pdata.costo = float(request.form["costo"])
                    # el precio ahora se esta definiendo en el registro del producto
                    # pdata.precio = float(
                    #     request.form["costo"]) * ((pdata.porcentaje/100)+1)
                    pdata.porcentaje = cal_porcentaje(pdata.precio, pdata.costo)
                    # insertando en la base de datos de reverso el movimiento
                    fechar = datetime.now()
                    fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                    reverso = Reversos(None, pdata.id, cantidaexi, costoexi,
                                       precioexi, "compra", fechar, current_user.id, True, False)
                    db.session.add(reverso)
                    db.session.commit()
                else:
                    cantidaexi = pdata.cantidad
                    costoexi = pdata.costo
                    precioexi = pdata.precio
                    pdata.cantidad = pdata.cantidad + \
                        int(request.form["cantidad"])
                    pdata.costo = float(request.form["costo"])
                    pdata.porcentaje = cal_porcentaje(pdata.precio, pdata.costo)

                totalc = float(request.form["costo"]) * \
                    int(request.form["cantidad"])
                fechar = datetime.now()
                fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                reverso = Reversos(None, pdata.id, cantidaexi, costoexi,
                                   precioexi, "compra", fechar, current_user.id, True, False)
                db.session.add(reverso)
                db.session.commit()
            else:
                # print(f"Producto "+str(x)+": ",request.form[f"producto"+str(x)], "Cantidad: ", request.form[f"cantidad"+str(x)], "Costo: ", request.form[f"costo"+str(x)])
                pdata = Productos.query.filter_by(
                    nombre=request.form[f"producto"+str(x)]).first()
                if pdata.cantidad == 0:
                    cantidaexi = pdata.cantidad
                    costoexi = pdata.costo
                    precioexi = pdata.precio
                    data["productos"].append({
                        "id": pdata.id,
                        "nombre": request.form[f"producto"+str(x)],
                        "cantidad": int(request.form[f"cantidad"+str(x)]),
                        "costo": float(request.form[f"costo"+str(x)])
                    })
                    pdata.cantidad = int(request.form[f"cantidad"+str(x)])
                    pdata.costo = float(request.form[f"costo"+str(x)])
                    pdata.porcentaje = cal_porcentaje(pdata.precio, pdata.costo)
                    fechar = datetime.now()
                    fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                    reverso = Reversos(None, pdata.id, cantidaexi, costoexi,
                                       precioexi, "compra", fechar, current_user.id, True, False)
                    db.session.add(reverso)
                    db.session.commit()
                else:
                    cantidaexi = pdata.cantidad
                    costoexi = pdata.costo
                    precioexi = pdata.precio
                    data["productos"].append({
                        "id": pdata.id,
                        "nombre": request.form[f"producto"+str(x)],
                        "cantidad": int(request.form[f"cantidad"+str(x)]),
                        "costo": float(request.form[f"costo"+str(x)])
                    })
                    pdata.cantidad = pdata.cantidad + \
                        int(request.form[f"cantidad"+str(x)])
                    pdata.costo = float(request.form[f"costo"+str(x)])
                    pdata.porcentaje = cal_porcentaje(pdata.precio, pdata.costo)

                totalc = totalc + \
                    (float(request.form[f"costo"+str(x)])
                     * int(request.form[f"cantidad"+str(x)]))
                fechar = datetime.now()
                fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                reverso = Reversos(None, pdata.id, cantidaexi, costoexi,
                                   precioexi, "compra", fechar, current_user.id, True, False)
                db.session.add(reverso)
                db.session.commit()
        # listo los item de la compra
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
        # sess.query(User).filter(User.age == 25).\
        # update({User.age: User.age - 10}, synchronize_session=False)
        # ajusta los reversos de esta compra a procesados registrados a True
        db.session.query(Reversos).filter(Reversos.registrando == True).update(
            {Reversos.registrando: False, Reversos.id_t: compra.id})
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
    # compradata = Compras.query.get(id)
    compradata = db.session.get(Compras, id)

    # obteniendo datos del proveedor
    # provdata = Proveedores.query.get(compradata.id_p)
    provdata = db.session.get(Proveedores, compradata.id_p)
    fechac = compradata.fecha.strftime("%d/%m/%Y")
    fechaf = compradata.fechaf.strftime("%d/%m/%Y")

    return render_template("comprobantes/comprobante.html", compra=compradata, provdata=provdata, fechac=fechac, fechaf=fechaf)


def creaPdf(ruta_template, compradata, provdata, fechac, fechaf, id):
    template_name = ruta_template.split('\\')[-1]
    ruta_template = ruta_template.replace(template_name, '')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(template_name)
    rutaimglogo = os.path.abspath(f"src/static/ico/store-svgrepo-com2.svg")
    html = template.render(
        compra=compradata, provdata=provdata, fechac=fechac, fechaf=fechaf, ipserver=ipserver)

    options = {
        "page-size": "Letter",
        "margin-top": "0.5in",
        "margin-bottom": "0.5in",
        "margin-right": "0.5in",
        "margin-left": "0.5in",
        "encoding": "UTF-8",
        "enable-local-file-access": None
    }
    # para posible implementacion
    file_name = f"ams_cc_{id}.pdf"
    # pdf_path = os.path.join(settings.BASE_DIR, 'static', 'pdf', file_name)

    # ummm
    # return FileResponse(open(pdf_path, 'rb'), filename=file_name, content_type='application/pdf')

    # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf")
    rutaarchivo = os.path.abspath(f"src/static/ext/bin/wkhtmltopdf.exe")
    config = pdfkit.configuration(wkhtmltopdf=rutaarchivo)
    ruta_salida = os.path.abspath(f"src/static/pdf/{file_name}")
    cssfile = os.path.abspath(f"src/static/css/comprobante.css")
    pdfkit.from_string(html, ruta_salida, options=options,
                       configuration=config)

    # print(html)
    return file_name


@gcomp.route("/comprobantectpdf/<id>")
@login_required
def comprobantectpdf(id):
    # obteniendo datos de la compra
    # compradata = Compras.query.get(id)
    compradata = db.session.get(Compras, id)
    # obteniendo datos del proveedor
    # provdata = Proveedores.query.get(compradata.id_p)
    provdata = db.session.get(Proveedores, compradata.id_p)
    fechac = compradata.fecha.strftime("%d/%m/%Y")
    fechaf = compradata.fechaf.strftime("%d/%m/%Y")

    # rutaarchivo = os.path.abspath(f"src/static/img/productos/")
    # 'C:\CODE\AMS\src\templates\comprobantes\comprobante.html'
    ruta_template = "C:\\CODE\\AMS\\src\\templates\\comprobantes\\comprobantepdf.html"
    # template = "comprobante.html"

    pdf_file = creaPdf(ruta_template, compradata,
                       provdata, fechac, fechaf, id)

    # return render_template("comprobantes/comprobante.html", compra=compradata, provdata=provdata, fechac=fechac, fechaf=fechaf)
    # return redirect(url_for("static", filename="/pdf/" + pdf_file), code=301)
    # OHS
    return send_from_directory("static/pdf", pdf_file, as_attachment=True)


@gcomp.route("/modcompra/<id>", methods=["GET", "POST"])
@login_required
def editarCompra(id):
    # datacompra = Compras.query.get(id)
    datacompra = db.session.get(Compras, id)
    fechaf = datacompra.fechaf.strftime("%d/%m/%Y")
    # proveedor = Proveedores.query.get(datacompra.id_p)
    proveedor = db.session.get(Proveedores, datacompra.id_p)
    dataproveedor = Proveedores.query.all()
    productos = Productos.query.all()
    if current_user.rol == 0:
        if request.method == "POST":
            itemdb = datacompra.productos
            # nitem = len(itemdb["productos"])
            itemlist = itemdb["productos"]
            # revertir la transaccion en los productos
            for item in itemlist:
                # print("item id", item["id"], item["nombre"], item["cantidad"],item["costo"])
                # db.session.query(Reversos).filter(Reversos.registrando == True).update({Reversos.registrando : False, Reversos.id_t : compra.id})
                # get({"id_t" : datacompra.id, "id_p" : item["id"]})
                # datareverso = db.session.query(Reversos).filter(Reversos.id_t == datacompra.id ).filter(Reversos.id_t == item["id"])

                datareverso = Reversos.query.filter(
                    Reversos.id_t == datacompra.id).filter(Reversos.id_p == item["id"])
                # print("busqueda reverso", datareverso)
                for data in datareverso:
                    # print("datareverso", data.id, data.id_t, data.id_p, data.cantidad, data.costo, data.precio,
                    #       data.transaccion, data.fecha, data.id_u, data.registrando, data.reversado)
                    producto = db.session.get(Productos, item["id"])
                    producto.cantidad = data.cantidad
                    producto.costo = data.costo
                    producto.precio = data.precio
                    reverso = db.session.get(Reversos, data.id)
                    db.session.delete(reverso)
                    db.session.commit()

            # y realizado el reverso continuamos agregando los nuevos item de la compra 24/07/23
            data = {}
            data["productos"] = []
            # registrando cada productos y actualizando catidad costo y precio
            for x in range(int(request.form["item"])):
                if x == 0:
                    pdata = Productos.query.filter_by(
                        nombre=request.form['producto']).first()
                    data["productos"].append({
                        "id": pdata.id,
                        "nombre": request.form["producto"],
                        "cantidad": int(request.form["cantidad"]),
                        "costo": float(request.form["costo"])
                    })

                    if pdata.cantidad == 0:
                        # almacenando los datos existente antes de la compra
                        cantidaexi = pdata.cantidad
                        costoexi = pdata.costo
                        precioexi = pdata.precio
                        pdata.cantidad = int(request.form["cantidad"])
                        pdata.costo = float(request.form["costo"])
                        pdata.porcentaje = cal_porcentaje(pdata.precio, pdata.costo)
                        # pdata.precio = float(
                        #     request.form["costo"]) * ((pdata.porcentaje/100)+1)
                        # insertando en la base de datos de reverso el movimiento
                        fechar = datetime.now()
                        fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                        reverso = Reversos(None, pdata.id, cantidaexi, costoexi,
                                           precioexi, "compra", fechar, current_user.id, True, False)
                        db.session.add(reverso)
                        db.session.commit()
                    else:
                        cantidaexi = pdata.cantidad
                        costoexi = pdata.costo
                        precioexi = pdata.precio
                        pdata.cantidad = pdata.cantidad + \
                            int(request.form["cantidad"])
                        pdata.costo = float(request.form["costo"])
                        pdata.porcentaje = cal_porcentaje(pdata.precio, pdata.costo)
                        # pdata.precio = float(
                        #     request.form["costo"]) * ((pdata.porcentaje/100)+1)

                    totalc = float(request.form["costo"]) * \
                        int(request.form["cantidad"])
                    fechar = datetime.now()
                    fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                    reverso = Reversos(None, pdata.id, cantidaexi, costoexi,
                                       precioexi, "compra", fechar, current_user.id, True, False)
                    db.session.add(reverso)
                    db.session.commit()
                else:
                    pdata = Productos.query.filter_by(
                        nombre=request.form[f"producto"+str(x)]).first()
                    if pdata.cantidad == 0:
                        cantidaexi = pdata.cantidad
                        costoexi = pdata.costo
                        precioexi = pdata.precio
                        data["productos"].append({
                            "id": pdata.id,
                            "nombre": request.form[f"producto"+str(x)],
                            "cantidad": int(request.form[f"cantidad"+str(x)]),
                            "costo": float(request.form[f"costo"+str(x)])
                        })
                        pdata.cantidad = int(request.form[f"cantidad"+str(x)])
                        pdata.costo = float(request.form[f"costo"+str(x)])
                        pdata.porcentaje = cal_porcentaje(pdata.precio, pdata.costo)
                        fechar = datetime.now()
                        fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                        reverso = Reversos(None, pdata.id, cantidaexi, costoexi,
                                           precioexi, "compra", fechar, current_user.id, True, False)
                        db.session.add(reverso)
                        db.session.commit()
                    else:
                        cantidaexi = pdata.cantidad
                        costoexi = pdata.costo
                        precioexi = pdata.precio
                        data["productos"].append({
                            "id": pdata.id,
                            "nombre": request.form[f"producto"+str(x)],
                            "cantidad": int(request.form[f"cantidad"+str(x)]),
                            "costo": float(request.form[f"costo"+str(x)])
                        })
                        pdata.cantidad = pdata.cantidad + \
                            int(request.form[f"cantidad"+str(x)])
                        pdata.costo = float(request.form[f"costo"+str(x)])
                        pdata.porcentaje = cal_porcentaje(pdata.precio, pdata.costo)

                    totalc = totalc + \
                        (float(request.form[f"costo"+str(x)])
                         * int(request.form[f"cantidad"+str(x)]))
                    fechar = datetime.now()
                    fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                    reverso = Reversos(None, pdata.id, cantidaexi, costoexi,
                                       precioexi, "compra", fechar, current_user.id, True, False)
                    db.session.add(reverso)
                    db.session.commit()

            provdata = Proveedores.query.filter_by(
                fullname=request.form['proveedor']).first()
            fecha = datetime.now()
            fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
            if request.form["tcompra"] == "Contado":
                pagado = True
            else:
                pagado = False
            nfact = request.form["nfact"]
            fechaf = datetime.strptime(request.form["fechaf"], "%d/%m/%Y")
            # cambio del codigo de compras a editar la compra
            datacompra.id_p = provdata.id
            datacompra.nfact = nfact
            datacompra.fechaf = fechaf
            datacompra.productos = data
            datacompra.tcompra = request.form["tcompra"]
            datacompra.mpago = request.form["mpago"]
            datacompra.pagada = pagado
            datacompra.totalc = totalc
            datacompra.fecha = fecha
            datacompra.deleted = False
            datacompra.id_u = current_user.id
            # compra = Compras(provdata.id, nfact, fechaf, data,
            #                  request.form["tcompra"], request.form["mpago"], pagado, totalc, fecha, False,  current_user.id)

            db.session.commit()
            # sess.query(User).filter(User.age == 25).\
            # update({User.age: User.age - 10}, synchronize_session=False)
            # ajusta los reversos de esta compra a procesados registrados a True
            db.session.query(Reversos).filter(Reversos.registrando == True).update(
                {Reversos.registrando: False, Reversos.id_t: datacompra.id})
            db.session.commit()
            logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                        " | Modifico compra id " + str(datacompra.id))
            flash({'title': "AMS", 'message': "Compra: " +
                   "id " + str(datacompra.id) + " modificado satisfactoriamente"}, 'success')
            return redirect(url_for("gcompras.compras"))
        else:

            return render_template("gcompras/mcompras.html", fechaf=fechaf, datacompra=datacompra, dataproveedor=dataproveedor, productos=productos, provee=proveedor)
    else:

        flash({'title': "AMS", 'message': "Un administrador solo puede modificar compras"}, 'error')
        return redirect(url_for("gcompras.compras"))


@gcomp.route("/elcompra/<id>")
@login_required
def deletedCompra(id):
    if current_user.rol == 0:
        datacompra = db.session.get(Compras, id)
        itemdb = datacompra.productos
        itemlist = itemdb["productos"]
        # revertir la transaccion en los productos
        for item in itemlist:
            datareverso = Reversos.query.filter(
                Reversos.id_t == datacompra.id).filter(Reversos.id_p == item["id"])
            # print("busqueda reverso", datareverso)
            for data in datareverso:
                # print("datareverso", data.id, data.id_t, data.id_p, data.cantidad, data.costo, data.precio,
                #       data.transaccion, data.fecha, data.id_u, data.registrando, data.reversado)
                producto = db.session.get(Productos, item["id"])
                producto.cantidad = data.cantidad
                producto.costo = data.costo
                producto.precio = data.precio
                reverso = db.session.get(Reversos, data.id)
                db.session.delete(reverso)
                datacompra.deleted = True
                db.session.commit()

        # realizado el reverso continuamos marcando la compra como deleted

        flash({'title': "AMS", 'message': "Compra: " +
               "id " + str(datacompra.id) + " marcada como borrada"}, 'info')
        return redirect(url_for("gcompras.compras"))
    else:
        flash(
            {'title': "AMS", 'message': "Un administrador solo puede eliminar compras"}, 'error')
        return redirect(url_for("gcompras.compras"))
