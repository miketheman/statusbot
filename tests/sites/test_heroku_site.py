import datetime
import json

import pytest
import responses
from freezegun import freeze_time

from statusbot.sites import heroku_site


@pytest.fixture
def sample_heroku_status_good_response():
    with open('tests/fixtures/sample_heroku_status_good_response.json') as f:
        return json.load(f)


@pytest.fixture
def sample_heroku_status_bad_response():
    with open('tests/fixtures/sample_heroku_status_bad_response.json') as f:
        return json.load(f)


@responses.activate
@freeze_time('2017-09-20')
def test_status_good(sample_heroku_status_good_response):
    responses.add(responses.GET, 'https://status-api.heroku.com/api/ui/systems',
                  json=sample_heroku_status_good_response)
    assert heroku_site.status() == {'status': 'good', 'updated': datetime.datetime.utcnow()}


@responses.activate
@freeze_time('2017-09-20')
def test_status_not_good(sample_heroku_status_bad_response):
    responses.add(responses.GET, 'https://status-api.heroku.com/api/ui/systems',
                  json=sample_heroku_status_bad_response)
    assert heroku_site.status() == {'status': 'not good', 'updated': datetime.datetime.utcnow()}
