import pytest

from statusbot import status_check


def test_check_site_unknown_site():
    with pytest.raises(NotImplementedError):
        status_check.check_site('example.com')


@pytest.mark.parametrize("test_site", [
    'github',
    'heroku',
    'twitter',
    'facebook',
])
def test_check_site_known_site(mocker, test_site):
    mocked_site_status = mocker.patch('statusbot.sites.{}_site.status'.format(test_site))
    status_check.check_site(test_site)
    assert mocked_site_status.call_count == 1


@pytest.mark.parametrize("test_input, expected", [
    ('github', 'github'),
    ('github.com', 'github'),
    ('heroku', 'heroku'),
    ('heroku.com', 'heroku'),
    ('twitter', 'twitter'),
    ('twitter.com', 'twitter'),
    ('facebook', 'facebook'),
    ('facebook.com', 'facebook'),
    ('', ''),
])
def test_site_name_input_returns_slug(test_input, expected):
    assert status_check.normalize_site_name(test_input) == expected
