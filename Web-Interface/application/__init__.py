from flask import Flask
from .dbconnect import Database

app = Flask(__name__)
app.config.from_object('config')

from application import views