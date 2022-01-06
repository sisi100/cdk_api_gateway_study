import os
from time import sleep

SLEEP_TIME = int(os.getenv("SLEEP_TIME", 0))


def handler(event, context):
    sleep(SLEEP_TIME)
    return {"statusCode": 200}
