import json
import time
from datetime import datetime

from statusbot import status_check


def check(event, context):
    start_time = time.time()
    # TODO: It feels like there should be a better way to validate a dict
    # if not event or 'result' not in event or 'parameters' not in event['result'] or 'Site' not in event['result']['parameters']:
    #     raise(RuntimeError)
    if not event:
        raise(RuntimeError)

    req_body = json.loads(event['body'])
    site = req_body['result']['parameters']['Site']

    try:
        site_name, check_response = status_check.check_site(site)

        now = time.time()
        duration = now - start_time
        report(duration, 'aws.lambda.statusbot.handler.duration_secs', tags=['site:{}'.format(site_name)])

        response_content = {
            'speech': "The status of {} site is {}".format(site_name, check_response['status']),
        }
    except NotImplementedError:
        response_content = {
            'speech': "The '{}' site has not yet been implemented.".format(site)
        }

    response = {
        'statusCode': 200,
        'headers': {'Content-type': 'application/json'},
        'body': json.dumps(response_content),
    }

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

    print("MONITORING|{}|{}|gauge|{}|#{}".format(
        now_in_epoch,
        metric_value,
        metric_name,
        ",".join(tags)
    ))


if __name__ == "__main__":
    print('DEBUG: Will test github.com status')
    print(check({'body': "{\"result\": {\"parameters\": {\"Site\": \"github\"}}}"}, None))
