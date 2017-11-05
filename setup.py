from setuptools import setup

setup(
    name = 'python-rucaptcha',
    version = '1.5',
    author = 'AndreiDrang, redV0ID',

    packages = ['python_rucaptcha'],
    install_requires = [
        'requests>=2.18',
        'aiohttp>=2.3'
        ],
    description = 'Python 3 RuCaptcha library.',
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
    python_requires = '>=3.3',
    )
