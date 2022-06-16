from copyreg import constructor
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__, template_folder="../templates", static_folder="../static")

database = [
    {"username":"admin","email":"","id":"0000","psw":"admin"},
    {"username":"temp1","email":"","id":"0001","psw":"0000"},
    {"username":"temp2","email":"","id":"0002","psw":"0000"}
]




#REST API


#GET Request
@app.get("/")
def index():
    print(app.root_path)
    print(app.static_url_path)
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
@app.post("/user/register")
def create_user():
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

@app.route("/success/<name>")
def success(name):
    return "welcome %s" %name

#LOGIN
@app.route("/login", methods=["POST", "GET"])
def login():
    print("hit endpoint: login")
    if request.method == "POST":
        user = request.form["username"]
        print(request.form["password"])
        return redirect(url_for("success", name = user))
    else:
        user = request.args.get("username")
        #return redirect(url_for("success", name = user))
    return render_template("login.html")



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