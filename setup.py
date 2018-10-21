from setuptools import setup

setup(
    name = 'python-rucaptcha',
    version = '2.3',

    author = 'AndreiDrang, redV0ID',

    packages = ['python_rucaptcha'],
    install_requires = [
        'requests>=2.18',
        'aiohttp>=3'
        ],
    description = 'Python 3 RuCaptcha library with AIO module.',
    author_email = 'drang.andray@gmail.com',
    url = 'https://github.com/AndreiDrang/python-rucaptcha',
    license = 'MIT',
    keywords = '''captcha 
				rucaptcha 
				python3
				flask
				recaptcha
				captcha
				security
				api
				python-library
				python-rucaptcha
				rucaptcha-client''',
    python_requires = '>=3.6',
    )
