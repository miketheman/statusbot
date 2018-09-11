from datetime import datetime

import requests

BASE_URL = "https://status-api.heroku.com/api/ui/systems"
WEBSITE = "https://status.heroku.com/"


def status():
    # TODO: Is it worth checking response codes and handling?
    resp = requests.get(BASE_URL).json()

    # API reports multiple service statuses, collect them all into a set()
    status_set = {i["attributes"]["color"] for i in resp["data"]}

    if status_set == {"green"}:
        status = "good"
    else:
        status = "not good"

    # API doesn't contain any date information, use current
    updated = datetime.utcnow()

    return {"status": status, "updated": updated}
