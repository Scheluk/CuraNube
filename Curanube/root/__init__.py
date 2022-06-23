from flask import Blueprint
bp = Blueprint("root", __name__)        #create a blueprint for root
from Curanube.root import routes        #import the routes of root/routes