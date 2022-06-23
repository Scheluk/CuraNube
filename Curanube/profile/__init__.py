from flask import Blueprint
bp = Blueprint("profile", __name__)     #create a blueprint for profile
from Curanube.profile import routes     #import the routes from profile/routes