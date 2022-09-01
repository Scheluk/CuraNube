from Curanube import db
from Curanube.auth.routes import login_required
from Curanube.profile import bp
from Curanube.models import User
from flask import render_template, request
from flask_login import login_required, current_user

@bp.route("/<username>/home")
#login is required, so if no user is currently logged in (current_user = None), redirect to auth.login,
#and after login, redirect to the page that the user wanted to access before
@login_required     
def home(username):
    return render_template("profile/userspace_home.html", username = current_user.username)


@bp.route("/<username>/library")
@login_required
def library(username):
    return render_template("profile/userspace_library.html", username = current_user.username)



@bp.route("/<username>/account")
@login_required
def myaccount(username):
    return render_template("profile/userspace_myaccount.html", username = current_user.username)




@bp.route("/<username>/settings")
@login_required
def settings(username):
    return render_template("profile/userspace_settings.html", username = current_user.username)


@bp.route("/<username>/change_username", methods=["PUT", "GET"])
@login_required
def change_username(username):
    error = None    #error message
    if request.method == "PUT":
        print(request.method)
        data = request.get_json()
        print(data)
        user = User.query.get_or_404(current_user.id)
        print("query successful")
        print(user.id)
        print(user.username)
        user.username = data["username"]
        print(user.username)
        db.session.commit()
        #user2.update_from_json(data)
        print("PUT WORKS")
        return render_template("profile/userspace_settings.html", username = current_user.username)
    return render_template("profile/userspace_change_username.html", username = current_user.username)



@bp.route("/<username>/change_password")
@login_required
def change_password(username):
    return render_template("profile/userspace_change_password.html", username = current_user.username)



@bp.route("/<username>/delete_account")
@login_required
def delete_account(username):
    return render_template("profile/userspace_deleteaccount.html", username = current_user.username)