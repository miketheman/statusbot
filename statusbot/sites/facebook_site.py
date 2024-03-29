from datetime import datetime

import requests

STATUS_ENDPOINT = "https://www.facebook.com/platform/api-status/"


def status():
    resp = requests.get(STATUS_ENDPOINT).json()

    current_status_report = resp["current"]

    if current_status_report["health"] == 1:
        status = "good"
    else:
        status = "not good"

    updated = datetime.utcnow()

    return {"status": status, "updated": updated}
