install:
	python setup.py install

remove:
	pip uninstall python_rucaptcha -y

refactor:
	pip install black isort
	black python_rucaptcha/ examples/
	isort -rc python_rucaptcha/

upload:
	pip install twine
	python setup.py upload
