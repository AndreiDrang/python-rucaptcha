from setuptools import setup

setup(
    name = 'python-rucaptcha',
    version = '2.5.3',

    author = 'AndreiDrang, redV0ID',

    packages = ['python_rucaptcha'],
    install_requires = [
        'requests==2.21.0',
        'aiohttp==3.5.4',
        'pika==0.13.0'
        ],
    description = 'Python 3 RuCaptcha library with AIO module.',
    author_email = 'drang.andray@gmail.com',
    package_dir={'python-rucaptcha': 'python_rucaptcha'},
    include_package_data=True,
    url = 'https://github.com/AndreiDrang/python-rucaptcha',
    license = 'AGPL-3.0',
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
    zip_safe=False
    )
