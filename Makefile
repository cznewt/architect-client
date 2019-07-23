CWD=$(shell pwd)

VERSION = "0.8.4"

.PHONY: build publish

all: build publish

help:
	@echo "Available actions:"
	@echo "  build                Build architect-client source distribution"
	@echo "  publish                Publish architect-client to PyPi"

clean:
	rm dist/* -rf

build:
	python setup.py sdist

publish:
	twine upload dist/*

