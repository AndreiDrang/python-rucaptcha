install:
	pip3 install -e .

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

build:
	pip3 install --upgrade build setuptools
	python3 -m build

# PyPI upload token: create one at https://pypi.org/manage/account/token/
# and save it to the gitignored .pypi-token file:  echo pypi-xxxx > .pypi-token
upload:
	@test -f .pypi-token || { echo "missing .pypi-token (see Makefile comment)"; exit 1; }
	pip3 install twine wheel setuptools build
	@ TWINE_USERNAME=__token__ TWINE_PASSWORD=`cat .pypi-token` twine upload dist/*

tests: install
	coverage run --rcfile=.coveragerc -m pytest --verbose --showlocals --pastebin=all \
	tests/ --disable-warnings && \
	coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	coverage html --precision=3 --skip-empty -d coverage/html/ && \
	coverage xml -o coverage/coverage.xml

doc: install
	cd docs/ && \
	make html -e
