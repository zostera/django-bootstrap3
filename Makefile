VERSION := $(shell hatch version)

.PHONY: test
test:
	hatch run test

.PHONY: tests
tests:
	hatch run all:test

.PHONY: reformat
reformat:
	hatch run lint:fmt

.PHONY: lint
lint:
	hatch run lint:style

.PHONY: docs
docs:
	hatch run docs:build

.PHONY: example
example:
	hatch run example:runserver

.PHONY: porcelain
porcelain:
ifeq ($(shell git status --porcelain),)
	@echo "Working directory is clean."
else
	@echo "Error - working directory is dirty. Commit those changes!";
	@exit 1;
endif

.PHONY: branch
branch:
ifeq ($(shell git rev-parse --abbrev-ref HEAD),main)
	@echo "On branch main."
else
	@echo "Error - Not on branch main!"
	@exit 1;
endif

.PHONY: build
build: docs
	rm -rf build dist src/*.egg-info
	hatch build

.PHONY: publish
publish: porcelain branch build
	hatch publish
	git tag -a v${VERSION} -m "Release ${VERSION}"
	git push origin --tags
