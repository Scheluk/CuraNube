from flask import Blueprint
bp = Blueprint("root", __name__)
from Curanube.root import routes