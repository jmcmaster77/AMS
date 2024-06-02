from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from utils.log import logger

home = Blueprint("home", __name__)


@home.route('/home')
@login_required
def home_page():
    logger.info("Home page session id " + current_user.fullname)
    flash("All OK")
    return render_template("home.html", fullname=current_user.fullname)


@home.route("/acercade")
@login_required
def acercade():
    return render_template("acerca.html")
