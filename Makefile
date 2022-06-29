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
				src/
	black src/
	isort src/

lint:
	autoflake --in-place --recursive python_rucaptcha/ examples/ --check
	black python_rucaptcha/ examples/ --check
	isort python_rucaptcha/ examples/ --check-only

upload:
	pip install twine
	python setup.py upload

tests:
	coverage run --rcfile=.coveragerc -m pytest -vv --disable-warnings
	coverage report --precision=1 --sort=cover -m
