from flask import render_template, redirect, request, url_for, session
from application import app
import os


@app.route('/')
@app.route('/index/')
def index():
    return render_template('base.html', doc = '/index.html', menu = True)

