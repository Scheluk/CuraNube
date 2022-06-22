from operator import itemgetter
from flask import Flask, jsonify, redirect, render_template, request, url_for, flash, send_from_directory
from Curanube import app
from werkzeug.utils import secure_filename
import sqlite3
import os



#FILESHARING TRY 2:
UPLOAD_FOLDER = 'profile/<username>/library'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'xlsx', 'adb', 'pub'}

#Checks if file extensions are allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Does the uploading part
@app.route('profile/<username>/library', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('There must be a file part.')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the upload is aborted
        if file.filename == '':
            flash('A file must be selected for upload.')
            return
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <--Insert HTML here!-->
    '''

#Does the downloading part
@app.route('profile/<username>/library')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)




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
