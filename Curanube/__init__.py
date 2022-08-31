import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


#create all static server elements
db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"     #the login view to redirect when a client tries to access a page that needs a logged in user

#factory pattern for app
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)    #initialize the config for the app


    #initialize all static server elements
    db.init_app(app)
    login.init_app(app)

    from Curanube.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from Curanube.root import bp as root_bp
    app.register_blueprint(root_bp, url_prefix="/")
    from Curanube.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix="/profile")
    
    
    

    return app


from Curanube import models
