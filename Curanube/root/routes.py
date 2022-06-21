from Curanube.root import bp
from flask import render_template
from Curanube.db import print_users


#GET Request
@bp.route("/") 
def index():
    return render_template("index.html")

@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/printusers")
def show_users():
    print_users()
    return "Printed Users"