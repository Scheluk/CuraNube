from Curanube import db
from Curanube import profile
from Curanube.auth.routes import login_required
from Curanube.profile import bp
from Curanube.models import User
from flask import render_template, request, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

@bp.route("/<username>/home", methods=["GET", "PUT"])
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
        data = request.get_json()
        print(data)
        user = User.query.get_or_404(current_user.id)
        print("query successful")
        print(user.id)
        print(user.username)
        print(data["newUsername"])
        username_taken = (User.query.filter_by(username=data["newUsername"]).first() != None)
        if username == data["newUsername"]:
            print("New Username is same as Old Username")
            abort(403)
        elif username_taken:
            print("Username already taken")
            abort(403)
        else:
            user.username = data["newUsername"]
            #current_user.username = user.username
            print(user.username)
            db.session.commit()
            print("PUT WORKS")
            return render_template("profile/userspace_settings.html", username = user.username)
    return render_template("profile/userspace_change_username.html", username = current_user.username)



@bp.route("/<username>/change_password", methods=["PUT", "GET"])
@login_required
def change_password(username):
    message = ""
    if request.method == "PUT":
        print(request.method)
        data = request.get_json()
        print(data)
        user = User.query.get_or_404(current_user.id)
        print("query successful")
        if check_password_hash(user.password, data["oldPassword"]) == False:
            print("Wrong Password")
            message = "Wrong Password"
            abort(403)
        elif data["newPassword"] != data["confPassword"]:
            print("Passwords do not match")
            message = "Passwords do not match"
            abort(403)
        elif data["oldPassword"] == data["newPassword"]:
            print("New Password is same as Old Password")
            message = "New password is same as old Password"
            abort(403)
        elif message == "":
            print(user.password)
            print(data["oldPassword"])
            user.password = generate_password_hash(data["newPassword"])
            db.session.commit()
            message = "Password changed"
            return redirect(url_for("profile.home", username=current_user.username))
        flash(message)
    return render_template("profile/userspace_change_password.html", username = current_user.username)



@bp.route("/<username>/delete_account", methods=["GET", "DELETE"])
@login_required
def delete_account(username):
    if request.method == "DELETE":
        print("DELETE WORKS")
        userToDelete = User.query.get_or_404(current_user.id)
        logout_user()
        db.session.delete(userToDelete)    #delete the user from the database
        db.session.commit()
        return render_template("root/index.html")
    else:
        return render_template("profile/userspace_deleteaccount.html", username = current_user.username)
