from flask import Flask


app = Flask(__name__)
app.secret_key = "kajlsdhfhjkasdhfkjhk"

from . import routes
