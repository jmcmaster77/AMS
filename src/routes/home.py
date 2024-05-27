from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user

home = Blueprint("home", __name__)

@home.route('/home')
@login_required
def home_page():
    return 'Logged in as: ' + current_user.id