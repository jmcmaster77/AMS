from flask import Blueprint, request, render_template, flash

# instanciando ruta en blueprint 

glogin = Blueprint("login", __name__)

@glogin.route('/login')
def login():
    print("Login")
    return ("login")
