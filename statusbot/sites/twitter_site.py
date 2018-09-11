from datetime import datetime

import requests
from dateutil.tz import tzutc

STATUS_ENDPOINT = "https://mongocache.asm.ca.com/synth/current/39657/monitor/125017/?fields=cur"
WEBSITE = "https://status.twitterstat.us/"


def status():
    resp = requests.get(STATUS_ENDPOINT, verify=False).json()

    current_status_report = resp["result"][0]["cur"]

    if current_status_report["status"] == 0:
        status = "good"
    else:
        status = "not good"

    updated = datetime.utcfromtimestamp(current_status_report["period"]["until"]["sec"])
    updated = updated.replace(tzinfo=tzutc())

    return {"status": status, "updated": updated}
