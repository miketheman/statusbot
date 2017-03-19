import datetime
import responses
from dateutil.tz import tzutc

from statusbot.sites import github_site


@responses.activate
def test_status_good():
    responses.add(responses.GET, 'https://status.github.com/api/status.json',
                  json={"status": "good", "last_updated": "2017-03-12T02:32:08Z"}, status=200)
    assert github_site.status() == {'status': 'good', 'updated': datetime.datetime(2017, 3, 12, 2, 32, 8, tzinfo=tzutc())}


@responses.activate
def test_status_minor():
    responses.add(responses.GET, 'https://status.github.com/api/status.json',
                  json={"status": "minor", "last_updated": "2017-03-12T03:32:08Z"}, status=200)
    assert github_site.status() == {'status': 'minor', 'updated': datetime.datetime(2017, 3, 12, 3, 32, 8, tzinfo=tzutc())}
