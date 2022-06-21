import functools
from Curanube.auth import bp
from Curanube.db import database, get_db
from operator import itemgetter
from Curanube.auth.token import generate_verification_token, verify_token
from Curanube.profile.email import send_email
from flask import redirect, url_for, render_template, request, jsonify, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

### --- login routes --- ###



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()



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
        db = get_db()
        if "@" in userjson["credentials"]:
            user = db.execute("SELECT * FROM user WHERE email = (?)", (userjson["credentials"],)).fetchone()
        else:
            user = db.execute("SELECT * FROM user WHERE username = (?)", (userjson["credentials"],)).fetchone()
        

        if user is None:
            error = "Incorrect Username/Email"
        elif not check_password_hash(user["pw"], userjson["pw"]):
            error = "Incorrect password"
        elif not user["verified"]:
            error = "User not verified"
        if error == "":
            session.clear()
            session["user_id"] = user["id"]
            return redirect (url_for("profile.home", username = user["username"]))
        
        flash(error)

    return render_template("auth/login.html", error=error)    #show the login form



#LOGOUT
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("root.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)
    return wrapped_view


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
                db.execute("INSERT INTO user (id, email, username, pw, verified) VALUES (?, ?, ?, ?, ?)",
                    (freeUserId(db), userjson["email"], userjson["username"], generate_password_hash(userjson["pw"]), False),
                )
                db.commit()

                #token = generate_verification_token(userjson["email"])
                #verify_url = url_for("verify_email", token = token, _external=True)
                #html = render_template("auth/email_account_verification.html", verify_url = verify_url)
                #subject = "Please confirm your email"
                #send_email(userjson["email"], subject, html)

            except db.IntegrityError:
                error = "User or E-Mail already registered."
            else:
                return redirect(url_for("auth.accountcreated"))

    return render_template("auth/createaccount.html", error = error)



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





@bp.route("/verify/<token>")
def verify_email(token):
    try:
        email = verify_token(token)
    except:
        print("Verification Link is invalid or has expired")
    db = get_db()
    db.execute("SELECT verified FROM user WHERE email = (?)", (email,))
    result = db.fetchone()
    if result == True:
        print("Account already verified, please login")
    else:
        db.execute("UPDATE user SET verified = True WHERE email = (?)", (email,))
        db.commit()
        print("You have been confirmed")
    return redirect(url_for("root.index"))