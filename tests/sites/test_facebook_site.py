import datetime
import json

import pytest
import responses
from freezegun import freeze_time

from statusbot.sites import facebook_site


@pytest.fixture
def sample_facebook_status_good_response():
    with open("tests/fixtures/sample_facebook_status_good_response.json") as f:
        return json.load(f)


@pytest.fixture
def sample_facebook_status_bad_response():
    with open("tests/fixtures/sample_facebook_status_bad_response.json") as f:
        return json.load(f)


@responses.activate
@freeze_time("2017-10-11")
def test_status_good(sample_facebook_status_good_response):
    responses.add(responses.GET, "https://www.facebook.com/platform/api-status/", json=sample_facebook_status_good_response)
    assert facebook_site.status() == {"status": "good", "updated": datetime.datetime.utcnow()}


@responses.activate
@freeze_time("2017-10-11")
def test_status_not_good(sample_facebook_status_bad_response):
    responses.add(responses.GET, "https://www.facebook.com/platform/api-status/", json=sample_facebook_status_bad_response)
    assert facebook_site.status() == {"status": "not good", "updated": datetime.datetime.utcnow()}
