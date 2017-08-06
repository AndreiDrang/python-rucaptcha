from flask import render_template, redirect, request, url_for, session
from application import app
import os
import random
from application import Database


@app.route('/', methods = ["GET", "POST"])
@app.route('/index/', methods = ["GET", "POST"])
def index():

	payload = {
		"common_captcha_source": common_captcha_source()
	}
	# Обработка форм
	if request.method == 'POST':
		# Скрытие записки
		if "common_captcha_btn" in request.method:
			print(request.form["common_captcha_src"])
			print(request.form["common_captcha_answer"])
		return render_template('base.html', doc='/index.html', payload=payload)
	else:
		return render_template('base.html', doc = '/index.html', payload=payload)


# Функция которая возвращает рандомное изображение обычной капчи
def common_captcha_source():
	# Получаем список всех изображений и возвращаем рандомную картинку
	images_list = os.listdir('application/static/image/common_image_example/')
	return random.choice(images_list)
	

# ERRORS
@app.errorhandler(404)
def page_not_found(e):
	return render_template('base.html', doc = 'mistakes/404.html')

@app.errorhandler(500)
def page_not_found(e):
	return render_template('base.html', doc = 'mistakes/500.html')