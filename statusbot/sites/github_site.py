import requests
from dateutil.parser import parse

BASE_URL = "https://status.github.com/api"


def status():
    # TODO: Is it worth checking response codes and handling?
    resp = requests.get(BASE_URL + "/status.json").json()

    status = resp["status"]
    updated = parse(resp["last_updated"])

    return {"status": status, "updated": updated}
