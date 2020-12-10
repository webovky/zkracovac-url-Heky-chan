from flask import Flask
from pony.orm import set_sql_debug

app = Flask(__name__)
app.secret_key = "123456" 
if app.env == "development":
    set_sql_debug(True)

from . import routes
from . import models
