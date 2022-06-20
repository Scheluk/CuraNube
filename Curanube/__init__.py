import imp
from multiprocessing.spawn import import_main_path
import os
from flask import Flask



app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_mapping(
    TEMPLATES_AUTO_RELOAD = True,
    SECRET_KEY="dev"
)

import Curanube.main
