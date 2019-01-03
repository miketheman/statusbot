import requests
from dateutil.parser import parse

STATUS_URL = "https://www.githubstatus.com/api/v2/status.json"


def status():
    # TODO: Is it worth checking response codes and handling?
    resp = requests.get(STATUS_URL).json()

    status_indicator = resp["status"]["indicator"]
    updated = parse(resp["page"]["updated_at"])

    if status_indicator == "none":
        status = "good"
    else:
        status = "not good"

    return {"status": status, "updated": updated}
