.PHONY: clean test tox reformat publish

clean:
	rm -rf build dist *.egg-info

test:
	python manage.py test

tox:
	rm -rf .tox
	tox

reformat:
	isort -rc bootstrap3
	isort -rc demo
	autoflake -ir bootstrap3 demo --remove-all-unused-imports
	black .
	flake8 bootstrap3 demo

publish: clean
	cd docs && make html
	python setup.py sdist bdist_wheel upload
