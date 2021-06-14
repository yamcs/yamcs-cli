.PHONY: clean lint build deploy

clean:
	rm -rf build dist *.egg-info

lint:
	flake8 src --count --show-source --statistics

build: lint
	python setup.py sdist bdist_wheel

deploy: build
	twine upload -r pypi dist/*
