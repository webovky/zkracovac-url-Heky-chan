from flask import Flask
from pony.orm import set_sql_debug


app = Flask(__name__)
app.secret_key = "\n\x81\x83\xae\xdc'\x198b\x8dK\x87rM'\xda+\x0e\xae\xc2\xa0\x05V" 
if app.env == "development":
    set_sql_debug(True)

from . import routes
from . import models