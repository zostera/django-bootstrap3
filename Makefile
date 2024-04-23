VERSION := $(shell sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml)

.PHONY: test
test:
	coverage run manage.py test
	coverage report

.PHONY: tests
tests:
	tox

.PHONY: reformat
reformat:
	ruff format .
	ruff check . --fix

.PHONY: lint
lint:
	ruff check .

.PHONY: docs
docs: clean
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html

.PHONY: example
example:
	cd example && python manage.py runserver

.PHONY: porcelain
porcelain:
ifeq ($(shell git status --porcelain),)
	@echo "Working directory is clean."
else
	@echo "Error - working directory is dirty. Commit your changes.";
	@exit 1;
endif

.PHONY: branch
branch:
ifeq ($(shell git rev-parse --abbrev-ref HEAD),main)
	@echo "On branch main."
else
	@echo "Error - Not on branch main."
	@exit 1;
endif

.PHONY: build
build:
	python -m build
	twine check dist/*
	check-manifest
	pyroma .
	check-wheel-contents dist

.PHONY: publish
publish: porcelain branch docs build
	twine upload dist/*
	git tag -a v${VERSION} -m "Release ${VERSION}"
	git push origin --tags

.PHONY: clean
clean:
	rm -rf build dist src/*.egg-info .coverage*

.PHONY: version
version:
	@echo ${VERSION}
