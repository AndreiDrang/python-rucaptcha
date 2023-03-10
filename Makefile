install:
	cd src/ && python setup.py install

remove:
	pip uninstall python_rucaptcha -y

refactor:
	cd src/ && \
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				python_rucaptcha/ tests/ && \
	black python_rucaptcha/ tests/ && \
	isort python_rucaptcha/ tests/

lint:
	cd src/ && \
	autoflake --in-place --recursive python_rucaptcha/ --check && \
	black python_rucaptcha/ --check && \
	isort python_rucaptcha/ --check-only

upload:
	pip install twine
	cd src/ && python setup.py upload

tests:
	cd src/ && \
	coverage run --rcfile=.coveragerc -m pytest -s tests --disable-warnings && \
	coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	coverage html --precision=3 --skip-empty -d coverage/html/ && \
	coverage xml -o coverage/coverage.xml
