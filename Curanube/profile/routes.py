from Curanube.auth.routes import login_required
from Curanube.profile import bp
from flask import render_template
from flask_login import login_required, current_user

@bp.route("/<username>/home")
@login_required
def home(username):
    return render_template("profile/userspace_home.html", username = current_user.username)


@bp.route("/<username>/library")
@login_required
def library(username):
    return "Library"



@bp.route("/<username>/account")
@login_required
def myaccount(username):
    return "My Account"




@bp.route("/<username>/settings")
@login_required
def settings(username):
    return "Settings"



@bp.route("/<username>/delete_account")
@login_required
def delete_account(username):
    return "Delete Account"