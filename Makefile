.PHONY: clean test tox reformat lint docs build publish

PROJECT_DIR=src/bootstrap3
PYTHON_SOURCES=${PROJECT_DIR} tests *.py

clean:
	rm -rf build dist *.egg-info

test:
	coverage run manage.py test
	coverage report

tox:
	rm -rf .tox
	tox

reformat:
	autoflake -ir --remove-all-unused-imports ${PYTHON_SOURCES}
	isort -rc ${PYTHON_SOURCES}
	docformatter -ir --pre-summary-newline --wrap-summaries=0 --wrap-descriptions=0 ${PYTHON_SOURCES}
	black .

lint:
	flake8 ${PYTHON_SOURCES}
	pydocstyle --add-ignore=D1,D202,D301,D413 ${PYTHON_SOURCES}

docs:
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html

build: clean docs
	python setup.py sdist bdist_wheel
	twine check dist/*

publish: build
	twine upload dist/*
