from Curanube.auth import bp
from Curanube.db import database
from operator import itemgetter
from flask import redirect, url_for, render_template, request, jsonify

### --- login routes --- ###


#LOGIN
@bp.route("/login", methods=["POST", "GET"])
def login():
    error = ""  #error message that shows up on incorrect login
    if request.method == "POST":    #if POST, do the login
        #convert the form data to json response, and then to json data
        userjson = jsonify(
            credentials=request.form["username"],
            pw=request.form["password"]
        ).get_json() 
        print(userjson)
        if valid_login(userjson):   #check if the login is valid
            print("Valid Login")
            error=""
            return redirect(url_for("profile.home", username = userjson["credentials"]))
        else:
            error = "Invalid username/password"
    return render_template("login.html", error=error)    #show the login form


#LOGOUT
@bp.route("/logout")
def logout():
    return redirect(url_for("root.index"))


def valid_login(userjson):  #check if login is valid
    for user in database:
        if userjson["credentials"] == user["username"] or userjson["credentials"] == user["email"]:   #if user with that username or email exists
            if userjson["pw"] == user["pw"] and user["verified"]:    #if password is correct and user is verified
                return True
            else:
                print("DEBUG: wrong password")
                return False
    print("DEBUG: wrong username, user doesn't exist")
    return False





### --- User Creation Routes --- ###
@bp.route("/accountcreated")
def accountcreated():
    return render_template("accountcreated.html")


@bp.route("/createaccount", methods=["POST", "GET"])
def createaccount():
    error = ""  #error message that shows up on incorrect login
    print(error)
    if request.method == "POST":    #if POST, do the login
        #convert the form data to json response, and then to json data
        userjson = jsonify(
            email=request.form["email"],
            username=request.form["username"],
            pw=request.form["password"]
        ).get_json() 
        print(userjson)
        match valid_accountcreation(userjson):   #check if the login is valid
            case 0:
                print("Valid New Account")
                add_user(userjson)
                return redirect(url_for("auth.accountcreated"))
            case 1:
                error = "Username already taken"
            case 2:
                error = "E-Mail already taken"
    return render_template("createaccount.html", error = error)



def valid_accountcreation(userjson):
    for user in database:
        if userjson["username"] == user["username"]:
            print("DEBUG: User with that username already exists")
            return 1
        if userjson["email"] == user["email"]:
            print("DEBUG: User with that email already exists")
            return 2
    return 0

def add_user(userjson):
    database.append({
        "username":userjson["username"],
        "email":userjson["email"],
        "pw":userjson["pw"],
        "id":freeUserId(),
        "verified":False
    })
    print(database)


#function to dynamically assign user ids
def freeUserId():
    last_index = max(database, key=itemgetter("id"))["id"] if len(database) != 0 else 1   #search for biggest user id
    for i in range(1, int(last_index)):      #from 1 to the biggest user id
        #check if the id is already taken
        for user in database:
            idExists = False
            if i == user["id"]:
                idExists = True
                break
        if(not idExists):   #if not, return it
            return i
    return last_index+1     #if every id in the range is taken, return the biggest+1

