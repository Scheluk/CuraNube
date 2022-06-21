from audioop import add
from Curanube.auth import bp
from Curanube.db import database, get_db
from operator import itemgetter
from flask import redirect, url_for, render_template, request, jsonify
from werkzeug.security import generate_password_hash

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
    return render_template("auth/login.html", error=error)    #show the login form


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
    return render_template("auth/accountcreated.html")


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
        db = get_db()
        print(db)
        if error == "":
            try:
                add_user(userjson, db)
                db.commit()
            except db.IntegrityError:
                error = "User or E-Mail already registered."
            else:
                return redirect(url_for("auth.accountcreated"))

    return render_template("auth/createaccount.html", error = error)



def valid_accountcreation(userjson):
    for user in database:
        if userjson["username"] == user["username"]:
            print("DEBUG: User with that username already exists")
            return 1
        if userjson["email"] == user["email"]:
            print("DEBUG: User with that email already exists")
            return 2
    return 0

def add_user(userjson, db):
    db.execute("INSERT INTO user (id, email, username, pw, verified) VALUES (?, ?, ?, ?, ?)",
        (freeUserId(db), userjson["email"], userjson["username"], generate_password_hash(userjson["pw"]), False),
    )


#function to dynamically assign user ids
def freeUserId(db):
    cursor = db.cursor()
    cursor.execute("SELECT MAX(id) AS maximum FROM user")   #search for biggest user id
    result = cursor.fetchall()
    for i in result:
        last_index = i[0]
    print(last_index)
    if last_index is None:
        return 1
    
    for i in range(1, int(last_index)):      #from 1 to the biggest user id
        #check if the id is already taken
        cursor.execute("SELECT id FROM user WHERE id=?", (i,))
        result = cursor.fetchall()
        if not result:
            return i
    return last_index+1     #if every id in the range is taken, return the biggest+1

