# statusbot

A microservice to check the status of sites.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Known Sites

Known sites can be found in `statusbot.status_check.KNOWN_SITES`.

Individual site-handling code can be found in the `statusbot/sites/` subdirectory.

## Components

- Serverless (AWS Lambda, API Gateway)
- api.ai

## Requirments

- Node.js & `yarn`
- Python 3.6
- Libraries per `Pipfile` files.
- Serverless 1.x

## Actions

See `Makefile` for common tasks.

## License

MIT. See `LICENSE` for details.

## Authors

- Mike Fiedler, [@miketheman](https://github.com/miketheman)
