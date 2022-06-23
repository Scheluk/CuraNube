from flask import Blueprint
bp = Blueprint("auth", __name__)    #create a blueprint for auth
from Curanube.auth import routes    #import the routes of auth