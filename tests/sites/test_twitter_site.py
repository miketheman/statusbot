import datetime
import json

import pytest
import responses
from dateutil.tz import tzutc

from statusbot.sites import twitter_site


@pytest.fixture
def sample_twitter_status_response():
    with open("tests/fixtures/sample_twitter_status_response.json") as f:
        return json.load(f)


@pytest.fixture
def sample_twitter_status_bad_response():
    with open("tests/fixtures/sample_twitter_status_bad_response.json") as f:
        return json.load(f)


@responses.activate
def test_status_good(sample_twitter_status_response):
    responses.add(
        responses.GET,
        "https://mongocache.asm.ca.com/synth/current/39657/monitor/125017/?fields=cur",
        match_querystring=True,
        json=sample_twitter_status_response,
    )
    assert twitter_site.status() == {"status": "good", "updated": datetime.datetime(2017, 3, 19, 15, 27, 17, tzinfo=tzutc())}


@responses.activate
def test_status_not_good(sample_twitter_status_bad_response):
    responses.add(
        responses.GET,
        "https://mongocache.asm.ca.com/synth/current/39657/monitor/125017/?fields=cur",
        match_querystring=True,
        json=sample_twitter_status_bad_response,
    )
    assert twitter_site.status() == {"status": "not good", "updated": datetime.datetime(2017, 3, 19, 15, 27, 17, tzinfo=tzutc())}
