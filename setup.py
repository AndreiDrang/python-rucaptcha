
from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='python_rucaptcha',
    version='0.5.a1',
    author='AndreiDrang, redV0ID',
    
    packages=find_packages(),
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