import json
import os
import time
from datetime import datetime

# Patch all supported libraries for X-Ray - More info: https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-patching.html
from aws_xray_sdk.core import patch_all

from statusbot import status_check

# Only instrument libraries if running in Lambda
if os.getenv("LAMBDA_TASK_ROOT") and os.getenv("AWS_EXECUTION_ENV"):
    patch_all()


def check(event, _context):
    start_time = time.time()
    # TODO: It feels like there should be a better way to validate a dict
    # if not event or 'result' not in event or 'parameters' not in event['result'] or 'Site' not in event['result']['parameters']:
    #     raise(RuntimeError)
    if not event:
        raise (RuntimeError)

    req_body = json.loads(event["body"])
    site = req_body["queryResult"]["parameters"]["Site"]

    try:
        site_name, check_response = status_check.check_site(site)

        now = time.time()
        duration = now - start_time
        report(duration, "aws.lambda.statusbot.handler.duration_secs", tags=[f"site:{site_name}"])

        check_status = check_response["status"]
        response_content = {"fulfillment_text": f"The status of {site_name} site is {check_status}"}
    except NotImplementedError:
        response_content = {"fulfillment_text": f"The '{site}' site has not yet been implemented."}

    response = {"statusCode": 200, "headers": {"Content-type": "application/json"}, "body": json.dumps(response_content)}

    print("Response:\n")
    print(json.dumps(response))
    return response


def report(metric_value, metric_name, tags=[]):
    """Print to stdout a formatted message that the Datadog Lambda integration
    knows how to retrive. Follows this format:

    MONITORING|unix_epoch_timestamp|metric_value|metric_type|my.metric.name|#tag1:value,tag2

    See https://www.datadoghq.com/blog/monitoring-lambda-functions-datadog/
    """
    now_in_epoch = int(datetime.utcnow().strftime("%s"))

    tags_string = ",".join(tags)
    print(f"MONITORING|{now_in_epoch}|{metric_value}|gauge|{metric_name}|#{tags_string}")


if __name__ == "__main__":
    print("DEBUG: Will test github.com status")
    print(check({"body": '{"result": {"parameters": {"Site": "github"}}}'}, None))
