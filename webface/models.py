# from datetime import datetime
from pony.orm import PrimaryKey, Required, Optional, Set, Database

# Import Flask-Pony instance from __init__.py module

# Get a reference to the base class of Pony entities
db = Database()
db.bind(provider="sqlite", filename="./database.sqlite", create_db=True)


class User(db.Entity):
    user_id = PrimaryKey(str) 
    username = Required(str, unique=True)
    password = Required(str)
    addresses = Set("Shortener")


class Shortener(db.Entity):
    shortened_id = PrimaryKey(str)
    shortcut = Required(str)
    url = Required(str)
    user = Optional(User)

db.generate_mapping(create_tables=True)