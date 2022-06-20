from copyreg import constructor
import json
from operator import itemgetter
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__, template_folder="../templates", static_folder="../static")

database = [
    {"username":"admin","email":"admin@gmail.com","id":1,"pw":"admin","verified":True},
    {"username":"temp1","email":"t1@gmail.com","id":2,"pw":"admin","verified":False},
    {"username":"temp2","email":"t2@gmail.com","id":4,"pw":"admin","verified":True}
]


#REST API


#GET Request
@app.get("/")
def index():
    return render_template("index.html")

@app.get("/about")
def about():
    return render_template("about.html")



@app.get("/user")
def user():
    print("hit endpoint: user")
    username = request.args["user"]

    for user in database:
        if user["username"] == username:
            return jsonify(user)
        else:
            notfound = "%s not found in system!" %(username)
            return jsonify({"user":notfound})

#POST Request



#PATCH Request
@app.patch("/user/update")
def update_user():
    print("hit endpoint: msg")

#DELETE Request
@app.delete("/user/delete")
def delete_user():
    print("hit endpoint: msg")


### --- login routes --- ###

@app.route("/<username>/home")
def home(username):
    return render_template("userspace_home.html", username = username)


#LOGIN
@app.route("/login", methods=["POST", "GET"])
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
            return redirect(url_for("home", username = userjson["credentials"]))
        else:
            error = "Invalid username/password"
    return render_template("login.html", error=error)    #show the login form


#LOGOUT
@app.route("/logout")
def logout():
    return redirect(url_for("index"))


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
@app.route("/accountcreated")
def accountcreated():
    return render_template("accountcreated.html")


@app.route("/createaccount", methods=["POST", "GET"])
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
                return redirect(url_for("accountcreated"))
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
    last_index = max(database, key=itemgetter("id"))["id"]    #search for biggest user id
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

### --- Fileshare --- ###
@app.get("/fileshare")
def fileshare():
    print("hit endpoint: fileshare")
    return render_template("fileshare.html")

@app.post("/upload")
def upload_file():
    return jsonify({"user":"your file was uploaded"})





if __name__ == "__main__":
    app.run(debug=True)