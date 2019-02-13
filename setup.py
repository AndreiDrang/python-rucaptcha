import os
import io

from setuptools import setup

# Package meta-data.
NAME = 'python-rucaptcha'
DESCRIPTION = 'Python 3.6+ RuCaptcha library with AIO module.'
URL = 'https://github.com/AndreiDrang/python-rucaptcha'
EMAIL = 'drang.andray@gmail.com'
AUTHOR = 'AndreiDrang, redV0ID'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '2.5.3'
REQUIRED = [
        'requests==2.21.0',
        'aiohttp==3.5.4',
        'pika==0.13.0'
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name = NAME,
    version = VERSION,
    author = AUTHOR,
    packages = ['python_rucaptcha'],
    install_requires = REQUIRED,
    description = DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email = EMAIL,
    package_dir={'python-rucaptcha': 'python_rucaptcha'},
    include_package_data=True,
    url = URL,
    license = 'AGPL-3.0',
    keywords = '''
                captcha 
				rucaptcha 
				python3
				flask
				recaptcha
				captcha
				security
				api
				python-library
				python-rucaptcha
				rucaptcha-client
               ''',
    python_requires = REQUIRES_PYTHON,
    zip_safe=False,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 5',
        'Framework :: AsyncIO',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS'
    ],
    )
