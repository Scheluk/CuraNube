import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config



db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)



    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    from Curanube.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from Curanube.root import bp as root_bp
    app.register_blueprint(root_bp, url_prefix="/")
    from Curanube.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix="/profile")
    
    
    

    return app


from Curanube import models
