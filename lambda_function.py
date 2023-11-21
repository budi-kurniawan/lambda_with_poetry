'''
Write a lambda handler that accepts messages of the form:

{
    "serialNumber": "c01234",
    "event": "connect",
    "timestamp": 12345
}

And pushes them into an s3 bucket `{s3bucket}/{day}/{uuid}.json` where
- `s3bucket` name is from environment variable `S3_TARGET_BUCKET_NAME`,
- `day` is the day of the timestamp in format `Y-m-d`, and
- `uuid` is a random uuid.

Bonus points (in no particular order):

- Use `poetry`
- Process multiple messages at once
- Use `asyncio` when writing to s3
- Use `TypedDict` or `Pydantic` for `events` argument
- Make `mypy` and `pylint` happy with your code, avoid `Any`
- Add unit tests
'''

import asyncio
from typing import List, TypedDict
import json
import os
from datetime import datetime
import uuid
import boto3

class Message(TypedDict):
    ''' A class for type hint'''
    serialNumber: str
    event: str
    timestamp: int

class HttpResponse(TypedDict):
    ''' A class for type hint'''
    statusCode: int
    headers: dict
    body: str

async def write_to_s3(bucket_name: str, s3_path: str, message: str) -> None:
    ''' Writes the given message to a file referenced by s3_path'''
    encoded_string = message.encode("utf-8")
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)

async def process(bucket_name: str, events: List[Message]) -> None:
    ''' Starts processing '''
    tasks = []
    for event in events:
        message = build_message(event)
        s3_path = build_s3_path(event)
        task = asyncio.create_task(write_to_s3(str(bucket_name), s3_path, message))
        tasks.append(task)
    for task in tasks:
        await task

def build_s3_path(event: Message) -> str:
    ts = event['timestamp']
    day = timestamp_to_date_string(ts)
    unique_id = uuid.uuid4().hex
    return day + '/' + unique_id + '.json'

def build_message(event: Message) -> str:
    sn = event['serialNumber']
    ev = event['event']
    ts = event['timestamp']
    return '{"serialNumber": "%s", "event": "%s", "timestamp": %d}' % (sn, ev, ts)

def timestamp_to_date_string(ts: int) -> str:
    ''' Converts an int representing a timestamp to a string representing Y-m-d'''
    dt = datetime.fromtimestamp(ts)
    return f'{dt.year}-{dt.month}-{dt.day}'

def build_http_200(events: List[Message]) -> HttpResponse:
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "events ": events
        })
    }

def build_http_400() -> HttpResponse:
    msg = "The request could not be understood by the server due to malformed syntax."
    return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message ": msg
        })
    }

def is_input_valid(events: Message | List[Message]) -> bool:
    if not isinstance(events, dict) and not isinstance(events, list):
        return False
    if isinstance(events, dict):
        events = [events]
    for event in events:
        if 'serialNumber' not in event or 'event' not in event or 'timestamp' not in event:
            return False
    return True

def lambda_handler(events: Message | List[Message], _) -> HttpResponse:
    ''' The main lambda handler'''
    if not is_input_valid(events):
        return build_http_400()
    if isinstance(events, dict): # if there is only one message, enclose in List
        events = [events]
    bucket_name = os.environ['S3_TARGET_BUCKET_NAME']
    asyncio.run(process(bucket_name, events))
    return build_http_200(events)
