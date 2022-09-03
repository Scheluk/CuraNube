import functools
from Curanube import login, db
from Curanube.models import User
from Curanube.auth import bp
from flask import redirect, url_for, render_template, request, jsonify, g, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql.expression import func





### --- login routes --- ###


#LOGIN route
@bp.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:       #wenn der user bereits eingeloggt ist (invalid route)
        return redirect(url_for("root.index"))  #geh zur homepage
    if request.method == "POST":    #if POST, do the login
        error = None  #error message that shows up on incorrect login
        #convert the form data to json response, and then to json data
        userjson = jsonify(
            credentials=request.form["username"],
            pw=request.form["password"]
        ).get_json()
        if "@" in userjson["credentials"]:  #if user logged in with email
            user = User.query.filter_by(email=userjson["credentials"]).first()  #get user with that email
        else:
            user = User.query.filter_by(username=userjson["credentials"]).first()   #else get the user with that username
        
        if user is None:    #if the user doesnt exist
            error = "Incorrect Username/Email"
        elif not check_password_hash(user.password, userjson["pw"]): #if the password is incorrect
            error = "Incorrect password"
        elif not user.confirmed:    #if the user is not comfirmed
            error = "User not verified"
        if error == None:   #if none of the above errors apply
            login_user(user)    #login the user (session handling)
            return redirect(url_for("profile.home", username = user.username))  #go to the users homepage
        
        flash(error)    #flash an error if one exists
    error = None    #clear the error
    return render_template("auth/login.html")    #show the login form



#LOGOUT
@bp.route("/logout")
@login_required #requires user to be logged in (no anonymous calling of that route)
def logout():
    logout_user()   #logout user (session handling)
    return redirect(url_for("root.index"))  #go to index



### --- User Creation Routes --- ###
@bp.route("/accountcreated")
def accountcreated():   #route when user was successfully created
    return render_template("auth/accountcreated.html")


@bp.route("/createaccount", methods=["POST", "GET"])
def createaccount():
    error = None  #error message that shows up if one exists
    if request.method == "POST":    #if POST, do the account creation
        #convert the form data to json response, and then to json data
        userjson = jsonify(
            email=request.form["email"],
            username=request.form["username"],
            pw=request.form["password"]
        ).get_json()
        error = valid_new_account(userjson) #validate if the data for the new user is valid (keine doppelgänger bezüglich username und email)
        if error == None:   
            #create a new user object
            user = User(id=freeUserId(), email=userjson["email"], username=userjson["username"], password=generate_password_hash(userjson["pw"]), confirmed=True)
            user.confirmed = True #ONLY BECAUSE GOOGLE WONT LET US SEND VERIFICATION EMAILS!!!
            db.session.add(user)    #add the created user to the database
            db.session.commit() #commit changes to the database, to take effect

            return redirect(url_for("auth.accountcreated")) 
        flash(error)
    return render_template("auth/createaccount.html", error = error)



#function to dynamically assign user ids
def freeUserId():
    last_index = 0
    for user in User.query.all():
        if user.id > last_index:
            last_index = user.id
    print(last_index)
    if last_index == 0:
        return 1
    
    for i in range(1, int(last_index)):      #from 1 to the biggest user id
        #check if the id is already taken
        result = User.query.filter_by(id=i).first()
        if not result:
            return i
    return last_index+1     #if every id in the range is taken, return the biggest+1


def valid_new_account(userjson):    #check if a user already has that email or username
    if User.query.filter_by(email=userjson["email"]).first() is not None:
        return "Please use a different email address."
    if User.query.filter_by(username=userjson["username"]).first() is not None:
        return "Please use a different username."
    return None



