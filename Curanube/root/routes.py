from Curanube.root import bp
from flask import render_template


#GET Request
@bp.route("/") 
def index():
    return render_template("index.html")

@bp.route("/about")
def about():
    return render_template("about.html")