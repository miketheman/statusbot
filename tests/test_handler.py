import json
import sys

import pytest

from handler import check


@pytest.fixture
def apiai_event():
    with open("tests/fixtures/sample_api_gw_payload.json") as f:
        return json.load(f)


@pytest.fixture
def apiai_event_unimplemented():
    with open("tests/fixtures/sample_apiai_unimplemented.json") as f:
        return json.load(f)


def test_handler_missing_event_raises():
    with pytest.raises(RuntimeError):
        check(None, None)


def test_handler_missing_params_raises():
    with pytest.raises(KeyError):
        check({"result": {}}, None)
    with pytest.raises(KeyError):
        check({"result": {"parameters": {}}}, None)


def test_handler_status_check(mocker, apiai_event):
    def mock_status():
        return {"status": "good", "updated": "now"}

    mocker.patch("statusbot.sites.github_site.status", mock_status)
    response = check(apiai_event, None)
    assert response["statusCode"] == 200
    assert response["headers"]["Content-type"] == "application/json"
    assert json.loads(response["body"])["speech"] == "The status of github site is good"


def test_handler_status_unknown_site(mocker, apiai_event_unimplemented):
    response = check(apiai_event_unimplemented, None)
    assert response["statusCode"] == 200
    assert response["headers"]["Content-type"] == "application/json"
    assert json.loads(response["body"])["speech"] == "The 'example.com' site has not yet been implemented."


def test_handler_xray_patches_with_env(mocker, monkeypatch):
    mocked_xray = mocker.patch("aws_xray_sdk.core.patch_all")
    monkeypatch.setenv("LAMBDA_TASK_ROOT", "/some/path")
    monkeypatch.setenv("AWS_EXECUTION_ENV", "AWS_Lambda_python3.6")

    del sys.modules["handler"]
    import handler  # noqa: F401

    assert mocked_xray.call_count == 1


def test_handler_xray_does_not_patch_without_env(mocker):
    mocked_xray = mocker.patch("aws_xray_sdk.core.patch_all")

    del sys.modules["handler"]
    import handler  # noqa: F401

    assert mocked_xray.call_count == 0
