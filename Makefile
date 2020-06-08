install:
	python setup.py install

remove:
	pip uninstall python3-anticaptcha -y

refactor:
	pip install black isort
	black python_rucaptcha/
	isort -rc python_rucaptcha/

upload:
	pip install twine
	python setup.py upload
