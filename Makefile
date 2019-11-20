.PHONY: clean test tox reformat lint publish docs build publish

clean:
	rm -rf build dist *.egg-info

test:
	coverage run manage.py test && coverage report

tox:
	rm -rf .tox
	tox

reformat:
	isort -rc bootstrap3
	isort -rc demo
	isort -rc *.py
	autoflake -ir *.py bootstrap3 demo --remove-all-unused-imports
	docformatter -ir --pre-summary-newline --wrap-summaries=0 --wrap-descriptions=0 *.py bootstrap3 demo
	black .

lint:
	flake8
	pydocstyle --add-ignore=D1,D202,D301,D413 *.py bootstrap3/ demo/

docs:
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html

build: clean docs
	python setup.py sdist bdist_wheel
	twine check dist/*

publish: build
	twine upload dist/*
