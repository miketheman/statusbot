all: test

clean:
	@find . -name \*.pyc -delete
	@find . -name __pycache__ -delete
	@rm -fr .cache/ .coverage* .pytest_cache/ .requirements/ htmlcov/

deploy: clean
	@serverless deploy

setup:
	@yarn install
	@pipenv install --dev

test:
	@pytest
