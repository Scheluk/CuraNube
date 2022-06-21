from Curanube.root import bp
from flask import render_template
from Curanube.db import delete_user, print_users


#GET Request
@bp.route("/") 
def index():
    return render_template("root/index.html")

@bp.route("/about")
def about():
    return render_template("root/about.html")


@bp.route("/printusers")
def show_users():
    delete_user(2)
    print_users()
    return "Printed Users"