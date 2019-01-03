import datetime
import json

import pytest
import responses
from dateutil.tz import tzutc

from statusbot.sites import github_site


@pytest.fixture
def sample_github_status_good_response():
    with open("tests/fixtures/sample_github_status_good_response.json") as f:
        return json.load(f)


@pytest.fixture
def sample_github_status_bad_response():
    with open("tests/fixtures/sample_github_status_bad_response.json") as f:
        return json.load(f)


@responses.activate
def test_status_good(sample_github_status_good_response):
    responses.add(responses.GET, github_site.STATUS_URL, json=sample_github_status_good_response)
    assert github_site.status() == {"status": "good", "updated": datetime.datetime(2018, 12, 15, 18, 31, 27, 54000, tzinfo=tzutc())}


@responses.activate
def test_status_not_good(sample_github_status_bad_response):
    responses.add(responses.GET, github_site.STATUS_URL, json=sample_github_status_bad_response)
    assert github_site.status() == {"status": "not good", "updated": datetime.datetime(2018, 12, 11, 14, 41, 41, 431000, tzinfo=tzutc())}
