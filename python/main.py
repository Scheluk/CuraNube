from copyreg import constructor
import json
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__, template_folder="../templates", static_folder="../static")

database = [
    {"username":"admin","email":"admin@gmail.com","id":"0000","pw":"admin"},
    {"username":"temp1","email":"","id":"0001","pw":"0000"},
    {"username":"temp2","email":"","id":"0002","pw":"0000"}
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
@app.post("/register")
def register():
    print("hit endpoint: msg")


#PATCH Request
@app.patch("/user/update")
def update_user():
    print("hit endpoint: msg")

#DELETE Request
@app.delete("/user/delete")
def delete_user():
    print("hit endpoint: msg")






### --- login routes --- ###

@app.route("/home/<username>")
def home(username):
    return render_template("home.html", username = username)


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
    return render_template("index.html")


def valid_login(userjson):  #check if login is valid
    for user in database:
        if userjson["credentials"] == user["username"] or userjson["credentials"] == user["email"]:   #if user with that username or email exists
            if userjson["pw"] == user["pw"]:    #if password is correct
                return True
            else:
                print("DEBUG: wrong password")
                return False
        else:
            print("DEBUG: wrong username, user doesn't exist")
            return False
    print("ERROR, user database is empty")
    return False







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