from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from utils.log import logger

home = Blueprint("home", __name__)


@home.route('/home')
@login_required
def home_page():
    logger.info("Home page session id " + current_user.fullname)
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
    flash({'title': "AMS", 'message': "Bienvenido "}, 'success')
    return render_template("home.html", fullname=current_user.fullname)


@home.route("/acercade")
@login_required
def acercade():
    return render_template("acerca.html")
