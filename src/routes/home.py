from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user
from utils.log import logger

home = Blueprint("home", __name__)


@home.route('/home')
@login_required
def home_page():
    logger.info("Home page session id " + str(current_user.id) + " | "+ current_user.fullname)
    # flash("Todo OK", 'success')
    # example 
    # flash("All OK")
    # flash("All OK", 'success')
    # flash("All Normal", 'info')
    # flash("Not So OK", 'error')
    # flash("So So", 'warning')
    # example custom titles  
    # flash("Message", 'Custom Title')
    # flash({'title': "Custom Title", 'message': "Error Message"}, 'error')
    # print ("current app:TOASTR_CLOSE_BUTTON | ", current_app.config.get('TOASTR_CLOSE_BUTTON'))
    # print ("current app.config: ", current_app.config)
    current_app.config['TOASTR_CLOSE_BUTTON'] = 'false'
    current_app.config['TOASTR_TIMEOUT'] = '1500'
    # print ("current app: TOASTR_CLOSE_BUTTON |", current_app.config.get('TOASTR_CLOSE_BUTTON'))
    flash({'title': "AMS", 'message': "Bienvenido " + current_user.fullname}, 'success')
    
    # app.config['TOASTR_CLOSE_BUTTON'] = 'false'
    # app.config['TOASTR_TIMEOUT'] = '1000'
    
    return render_template("home.html", fullname=current_user.fullname)


@home.route("/acercade")
@login_required
def acercade():
    return render_template("acerca.html")

@home.route("/error")
@login_required
def error():
    flash({'title': "AMS", 'message': "Recurso no encontrado"}, 'error')
    return render_template("error.html")
