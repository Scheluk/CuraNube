from flask import Blueprint
bp = Blueprint("auth", __name__)
from Curanube.auth import routes