from flask import Response, render_template, redirect, request, url_for, session
from application import app
import os
import random
import json
import requests

from .dbconnect import Database


@app.route('/', methods = ["GET", "POST"])
@app.route('/index/', methods = ["GET", "POST"])
def index():

	payload = {
		"common_captcha_source": common_captcha_source()
	}
	# Обработка форм
	if request.method == 'POST':
		# Скрытие записки
		if "common_captcha_btn" in request.form:
			# Проверяем капчу и ответ на соответсвие
			return common_captcha_answer(request.form["common_captcha_src"],
			                               request.form["common_captcha_answer"])
		elif "recaptcha_new_btn" in request.form:
			return recaptcha_v2_new_answer(request.form["g-recaptcha-response"])
			

	return render_template('base.html', doc = '/index.html', payload=payload)


# Функция которая возвращает рандомное изображение обычной капчи
def common_captcha_source():
	# Получаем список всех изображений и возвращаем рандомную картинку
	images_list = os.listdir('application/static/image/common_image_example/')
	return random.choice(images_list)
	
'''
API response
'''
# Обработчик капчи изображением
def common_captcha_answer(captcha_name, user_answer):
	if user_answer == captcha_name.split(".")[0]:
		data = {'request': 'OK'}
		
		js = json.dumps(data)
		
		response = Response(js, status=200, mimetype='application/json')
		response.headers['Link'] = 'http://127.0.0.1:5000'
		
		return response
	else:
		data = {'request': 'FAIL'}
		
		js = json.dumps(data)
		
		response = Response(js, status=200, mimetype='application/json')
		response.headers['Link'] = 'http://127.0.0.1:5000'
		
		return response
# Обработчик новой рекапчи версии 2
def recaptcha_v2_new_answer(g_recaptcha_response):
	# Проверяем решил ли юзер капчу
	payload = {
				"secret": "6Lf77CsUAAAAAMJ1yJWbEG1VyVYKIQZWVQJRg25t",
				"response": g_recaptcha_response,
			}
	# Отсылаем запрос на правильность капчи
	captcha_answer = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)

	if captcha_answer.json()["success"]=="true":
		data = {'request': 'OK'}
		
		js = json.dumps(data)
		
		response = Response(js, status=200, mimetype='application/json')
		response.headers['Link'] = 'http://127.0.0.1:5000'
		
		return response
	else:
		data = {'request': 'FAIL'}
		# Если есть ошибки - высылаем и их
		if "error-codes" in captcha_answer.json() and captcha_answer.json()["error-codes"]!=[]:
			data.update({"recaptcha_error": captcha_answer.json()["error-codes"]})
		
		js = json.dumps(data)
		
		response = Response(js, status=200, mimetype='application/json')
		response.headers['Link'] = 'http://127.0.0.1:5000'
		
		return response

# ERRORS
@app.errorhandler(404)
def page_not_found(e):
	return render_template('base.html', doc = 'mistakes/404.html')

@app.errorhandler(500)
def page_not_found(e):
	return render_template('base.html', doc = 'mistakes/500.html')