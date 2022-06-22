import os


basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
print(os.path.join(basedir, "curanube.db"))

class Config(object):
    SECRET_KEY=os.environ.get("SECRET_KEY") or "camembert",
    TEMPLATES_AUTO_RELOAD = True,
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "curanube.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    SECURITY_PASSWORD_SALT = "ambrosia",
    #DATABASE = os.path.join(basedir, "instance\curanube.sqlite"),
    MAIL_SERVER = "smtp.googlemail.com",
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "Cura Nube",#os.environ["APP_MAIL_USERNAME"],
    MAIL_PASSWORD = "curanube325",#os.environ["APP_MAIL_PASSWORD"],
    MAIL_DEFAULT_SENDER = "curanube@gmail.com"