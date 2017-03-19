all: test

clean:
	@find . -name \*.pyc -delete
	@find . -name __pycache__ -delete
	@rm -fr .cache/ .coverage .requirements/ htmlcov/

setup:
	@yarn install
	@pip install -r dev-requirements.txt

test:
	@pytest
