from setuptools import setup, find_packages
from os.path import join, dirname

setup(
	name='python-rucaptcha',
	version='0.6.a1',
	author='AndreiDrang, redV0ID',
	
	packages=['python_rucaptcha'],
	install_requires=[
		'requests==2.18',
	],
	description='Python 3 RuCaptcha library.',
	author_email='drang.andray@gmail.com',
	url='https://github.com/AndreiDrang/python-rucaptcha',
	license='MIT',
	keywords='captcha rucaptcha',
	python_requires='>=3.4',
)