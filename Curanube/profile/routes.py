from Curanube.profile import bp
from flask import render_template

@bp.route("/<username>/home")
def home(username):
    return render_template("userspace_home.html", username = username)
