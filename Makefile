init:
	virtualenv -p python3 venv; \
	. venv/bin/activate; \
	pip install -r requirements_dev.txt; \

test:
	py.test tests

pypi:
	python setup.py upload
