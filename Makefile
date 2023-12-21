VERSION := $(shell python -c "import bootstrap3;print(bootstrap3.__version__)")

.PHONY: test
test:
	python manage.py test

.PHONY: tests
tests:
	nox

.PHONY: reformat
reformat:
	ruff --fix .
	ruff format .

.PHONY: lint
lint:
	ruff .

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
build: docs
	python -m build

.PHONY: publish
publish: porcelain branch build
	twine check dist/*
	twine upload dist/*
	git tag -a v${VERSION} -m "Release ${VERSION}"
	git push origin --tags

.PHONY: clean
clean: docs
	rm -rf build dist src/*.egg-info .coverage*

.PHONY: version
version:
	@echo ${VERSION}
