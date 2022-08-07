install:
	python setup.py install

remove:
	pip uninstall python_rucaptcha -y

refactor:
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				src/ setup.py
	black src/ setup.py
	isort src/ setup.py

lint:
	autoflake --in-place --recursive src/ --check
	black src/ --check
	isort src/ --check-only

upload:
	pip install twine
	python setup.py upload

tests:
	coverage run --rcfile=.coveragerc -m pytest -vv --disable-warnings
	coverage report --precision=3 --sort=cover -m
