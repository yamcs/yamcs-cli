.PHONY: clean lint build deploy

clean:
	rm -rf build dist *.egg-info

lint:
	flake8 yamcs --exclude '*pb2.py' --count --show-source --statistics

build: lint
	python setup.py sdist bdist_wheel

deploy: build
	twine upload -r pypi dist/*
