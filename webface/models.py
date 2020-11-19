# from datetime import datetime
from pony.orm import PrimaryKey, Required, Optional, Set

# Import Flask-Pony instance from __init__.py module
from . import pony

# Get a reference to the base class of Pony entities
db = pony.db


class User(db.Entity):
    login = PrimaryKey(str)
    password = Required(str)
    email = Optional(str)
    addresses = Set("Shortener")


class Shortener(db.Entity):
    shortcut = PrimaryKey(str)
    url = Required(str)
    user = Optional(User)
