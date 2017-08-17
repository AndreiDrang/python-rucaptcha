from bs4 import BeautifulSoup
import requests
import re, json


def key_captcha_data_handler():
	'''
	Открывает страницу с KeyCaptcha, парсит параметры требуемы для РуКапчи при решении
	:return: Вовзвращает словарь с ключами и параметрами
	'''
	html_doc = requests.get('https://www.keycaptcha.com/signup/').content
	soup = BeautifulSoup(html_doc, "html.parser")
	script = soup.find_all('script')[-4].string
	
	key_captcha_data = {
						"s_s_c_user_id": re.findall("var s_s_c_user_id = '(\w.*?)';", script)[0],
						"s_s_c_session_id": re.findall("var s_s_c_session_id = '(\w.*?)';", script)[0],
						"s_s_c_web_server_sign": re.findall("var s_s_c_web_server_sign = '(\w.*?)';", script)[0],
						"s_s_c_web_server_sign2": re.findall("var s_s_c_web_server_sign2 = '(\w.*?)';", script)[0],
						}
	return key_captcha_data
