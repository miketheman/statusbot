import datetime
import json

import pytest
import responses
from dateutil.tz import gettz

from statusbot.sites import datadog_site

NYC = gettz("America/New_York")


@pytest.fixture
def sample_datadog_status_good_response():
    with open("tests/fixtures/sample_datadog_status_good_response.json") as f:
        return json.load(f)


@pytest.fixture
def sample_datadog_status_bad_response():
    with open("tests/fixtures/sample_datadog_status_bad_response.json") as f:
        return json.load(f)


@responses.activate
def test_status_good(sample_datadog_status_good_response):
    responses.add(
        responses.GET, datadog_site.STATUS_URL, json=sample_datadog_status_good_response
    )
    assert datadog_site.status() == {
        "status": "good",
        "updated": datetime.datetime(2018, 12, 15, 18, 31, 27, 54000, tzinfo=NYC),
    }


@responses.activate
def test_status_not_good(sample_datadog_status_bad_response):
    responses.add(
        responses.GET, datadog_site.STATUS_URL, json=sample_datadog_status_bad_response
    )
    assert datadog_site.status() == {
        "status": "not good",
        "updated": datetime.datetime(2018, 12, 11, 14, 41, 41, 431000, tzinfo=NYC),
    }
