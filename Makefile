init:
	virtualenv -p python3 venv; \
	. venv/bin/activate; \
	pip install -r requirements_dev.txt; \

test:
	pytest tests/ --ignore=tests/integration

integration:
	pytest tests/

pypi:
	python setup.py upload

package:
	python setup.py build
