install:
	cd src/ && pip3 install -e .

remove:
	pip3 uninstall python_rucaptcha -y

refactor:
	black docs/
	isort docs/

	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				src/ tests/ && \
	black src/ tests/ && \
	isort src/ tests/

lint:
	autoflake --in-place --recursive src/ --check && \
	black src/ --check && \
	isort src/ --check-only

upload:
	pip3 install twine wheel
	cd src/ && python setup.py upload

tests: install
	coverage run --rcfile=.coveragerc -m pytest --verbose --showlocals --pastebin=all \
	tests/ --disable-warnings && \
	coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	coverage html --precision=3 --skip-empty -d coverage/html/ && \
	coverage xml -o coverage/coverage.xml

doc: install
	cd docs/ && \
	make html -e
