from operator import itemgetter
from Curanube.db import database
from flask import Flask, jsonify, redirect, render_template, request, url_for
from Curanube import app
import sqlite3











#@app.route("/user")
#def user():
 #   print("hit endpoint: user")
  #  username = request.args["user"]
#
 #   for user in database:
  #      if user["username"] == username:
   #         return jsonify(user)
    #    else:
     #       notfound = "%s not found in system!" %(username)
      #      return jsonify({"user":notfound})







### --- Fileshare --- ###
#@app.get("/fileshare")
#def fileshare():
 #   print("hit endpoint: fileshare")
  #  return render_template("fileshare.html")

#@app.post("/upload")
#def upload_file():
 #   return jsonify({"user":"your file was uploaded"})
