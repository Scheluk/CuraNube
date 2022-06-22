import functools
from Curanube import login, db
from Curanube.models import User
from Curanube.auth import bp
from Curanube.auth.token import generate_verification_token, verify_token
from Curanube.auth.email import send_email
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
            user = User(id=freeUserId(), email=userjson["email"], username=userjson["username"], password=generate_password_hash(userjson["pw"]), confirmed=False)
            user.confirmed = True #ONLY BECAUSE GOOGLE WONT LET US SEND VERIFICATION EMAILS!!!
            db.session.add(user)    #add the created user to the database
            db.session.commit() #commit changes to the database, to take effect
            token = generate_verification_token(userjson["email"])  #generate a token from the newly created users email address
            
            #create the url that should be sent to the users registered email, so he can activate his account
            verify_url = url_for("auth.verify_email", token = token, _external=True)    
            html = render_template("profile/activate.html", verify_url = verify_url)    #content of the email
            subject = "Please confirm your email"   #subject of the email
            #NOT LONGER AVAILABLE AS OF 30th OF MAY, 2022
            #send_email(userjson["email"], subject, html)

            #login_user(user)

            return redirect(url_for("auth.accountcreated")) 
        flash(error)
    return render_template("auth/createaccount.html", error = error)



#function to dynamically assign user ids
def freeUserId():
    #print(User.__table__.c)
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


def valid_new_account(userjson):
    if User.query.filter_by(email=userjson["email"]).first() is not None:
        return "Please use a different email address."
    if User.query.filter_by(username=userjson["username"]).first() is not None:
        return "Please use a different username."
    return None

@bp.route("/deleteuser")
@login_required
def deleteuser():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for("root.index"))

@bp.route("/verify/<token>")
#@login_required
def verify_email(token):
    try:
        email = verify_token(token)
    except:
        print("Verification Link is invalid or has expired")
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        print("Account already verified, please login")
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        print("You have been confirmed")
    return redirect(url_for("root.index"))