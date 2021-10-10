install:
	python setup.py install

remove:
	pip uninstall python_rucaptcha -y

refactor:
	pip install black isort autoflake
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				python_rucaptcha/ examples/
	black python_rucaptcha/ examples/
	isort python_rucaptcha/ examples/

lint:
	autoflake --in-place --recursive python_rucaptcha/ examples/ --check
	black python_rucaptcha/ examples/ --check
	isort python_rucaptcha/ examples/ --check-only

upload:
	pip install twine
	python setup.py upload
