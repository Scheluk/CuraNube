import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail



from . import db

db = db
login = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        TEMPLATES_AUTO_RELOAD = True,
        SECRET_KEY="camembert",
        SECURITY_PASSWORD_SALT = "ambrosia",
        DATABASE = os.path.join(app.instance_path, "curanube.sqlite"),
        MAIL_SERVER = "smtp.googlemail.com",
        MAIL_PORT = 465,
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_USERNAME = "Cura Nube",#os.environ["APP_MAIL_USERNAME"],
        MAIL_PASSWORD = "curanube325",#os.environ["APP_MAIL_PASSWORD"],
        MAIL_DEFAULT_SENDER = "curanube@gmail.com"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print(os.path.join(app.instance_path, "curanube.sqlite"))

    
    db.init_app(app)
    #login.init_app(app)
    mail.init_app(app)

    from Curanube.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from Curanube.root import bp as root_bp
    app.register_blueprint(root_bp, url_prefix="/")
    from Curanube.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix="/profile")
    

    

    return app

