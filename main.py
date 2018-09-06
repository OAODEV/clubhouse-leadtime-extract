from pprint import pprint as pp
import requests
import os

try:
    from google.cloud import logging
    logging_client = logging.Client()
    logger = logging_client.logger("LeadTimeLogger").log_struct
except:
    print("using pp logger")
    logger = pp


CLUBHOUSE_API_TOKEN = os.environ["CLUBHOUSE_API_TOKEN"]
host = "https://api.clubhouse.io"
api_version = "beta"


def get(resource, resource_code):
    return requests.get(
        "{}/api/{}/{}/{}?token={}".format(
            host,
            api_version,
            resource,
            resource_code,
            CLUBHOUSE_API_TOKEN,
        )
    ).json()


def id_to_code(name):
    if name.endswith("id"):
        return "".join([name[:-2], "code"])
    if name.endswith("ids"):
        return "".join([name[:-3], "codes"])
    return name


def process(value):
    """
    Change all keys that end in id or ids to code or codes

    for TYM ;)
    """

    if isinstance(value, list):
        return list(map(process, value))
    if isinstance(value, dict):
        processed = {}
        for k, v in value.items():
            processed[id_to_code(k)] = process(v)
        return processed
    return value


def search(query):
    return requests.get(
        "{}/api/beta/search/stories?token={}".format(
            host,
            CLUBHOUSE_API_TOKEN,
        ),
        data={
            "query": query,
        }
    ).json()


def get_next(results):
    url = "{}{}".format(host, results["next"])
    return requests.get(
        url,
        data={
            "token": CLUBHOUSE_API_TOKEN
        }
    ).json()


def extract_lead_time(request):
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        print(e)
        return "This endpoint is intended for Clubhouse webhook calls"

    for action in payload["actions"]:
        is_completed = action["changes"].get("completed", {"new": False})["new"]
        if is_completed:
            story = process(get("stories", action["id"]))
            logger(story)
    return "OK"


def log_all(stories):
    for story in stories:
        logger(process(get("stories", story["id"])))


def backfill_done_cards(request):
    result = search("is:done")
    log_all(result["data"])
    count = len(result["data"])
    while result["next"]:
        result = get_next(result)
        log_all(result["data"])
        count += len(result["data"])
    return "Logged {} done stories".format(count)


