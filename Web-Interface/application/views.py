from flask import render_template, redirect, request, url_for, session
from application import app
import os


@app.route('/')
@app.route('/index/')
def index():
	payload = {
		"common_captcha_source": "/application/templates/common_image_example/3.jpg"
	}

	return render_template('base.html', doc = '/index.html', payload=payload)

def common_captcha_source():
	pass

# ERRORS
@app.errorhandler(404)
def page_not_found(e):
	return render_template('base.html', doc = 'mistakes/404.html')

@app.errorhandler(500)
def page_not_found(e):
	return render_template('base.html', doc = 'mistakes/500.html')