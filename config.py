import os


basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
print(os.path.join(basedir, "curanube.db"))

class Config(object):
    SECRET_KEY="camembert"
    TEMPLATES_AUTO_RELOAD = True,
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "curanube.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    SECURITY_PASSWORD_SALT = "ambrosia",