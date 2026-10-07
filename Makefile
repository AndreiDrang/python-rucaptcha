.PHONY: install remove refactor lint build upload tests doc

install:
	uv sync --all-groups

remove:
	pip uninstall python-rucaptcha -y

refactor: install
	uv run black docs/
	uv run isort docs/

	uv run autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				src/ tests/
	uv run black src/ tests/
	uv run isort src/ tests/

lint: install
	uv run autoflake --in-place --recursive src/ --check
	uv run black src/ --check
	uv run isort src/ --check-only

build:
	uv build

# PyPI upload token: create one at https://pypi.org/manage/account/token/
# and save it to the gitignored .pypi-token file:  echo pypi-xxxx > .pypi-token
upload:
	@test -f .pypi-token || { echo "missing .pypi-token (see Makefile comment)"; exit 1; }
	@ UV_PUBLISH_TOKEN=`cat .pypi-token` uv publish

tests: install
	uv run coverage run --rcfile=.coveragerc -m pytest --verbose --showlocals --disable-warnings \
	tests/ && \
	uv run coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	uv run coverage html --precision=3 --skip-empty -d coverage/html/ && \
	uv run coverage xml -o coverage/coverage.xml

doc: install
	cd docs/ && \
	uv run --group docs make html -e
