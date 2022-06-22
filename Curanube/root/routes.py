from Curanube.root import bp
from flask import render_template
from Curanube import db
from Curanube.models import User
from werkzeug.security import generate_password_hash


#GET Request
@bp.route("/") 
def index():
    return render_template("root/index.html")

@bp.route("/about")
def about():
    return render_template("root/about.html")


@bp.route("/printusers")
def show_users():
    users = User.query.all()
    for u in users:
        print("####################")
        print("ID:", u.id)
        print("Username:", u.username)
        print("Email:",u.email)
        print("Password:",u.password)
        print("Confirmed:",u.confirmed)
        print("####################")
    
    #user = User.query.filter_by(id=1).first()
    #user.confirmed = True
    #user.password = generate_password_hash("admin")
    User.query.filter(User.id > 1).delete()
    db.session.commit()
    return "Printed Users"