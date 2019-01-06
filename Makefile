all: lint test

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:  ## Remove any generated artifacts
	@find . -name \*.pyc -delete
	@find . -name __pycache__ -delete
	@rm -fr .cache/ .coverage* .pytest_cache/ .requirements/ htmlcov/

deploy: clean  ## Deploy application to production
	@serverless deploy

setup:  ## Install node and python packagesa for development
	@yarn install
	@pipenv install --dev

lint:  ## Run code linter
	@black --line-length=160 *.py statusbot/ tests/

test:  ## Run tests
	@pytest
