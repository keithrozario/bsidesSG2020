import json
import boto3
import os
import logging
from evil_lambda_cache import ssm
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@ssm.cache(parameter='/production/variable/foo', max_age_in_seconds=120)
def query_location(event, context):

    building = event['building']
    seat = event['seat']

    client = boto3.client('dynamodb')
    response = client.query(
        TableName=os.environ['db_name'],
        IndexName="GSI-1",
        Select='SPECIFIC_ATTRIBUTES',
        ProjectionExpression="pk, sk, colA, EmployeeName",
        KeyConditionExpression="sk = :building AND colA = :seat",
        ExpressionAttributeValues={":building": {"S": building},
                                ":seat": {"S": seat}}
    )
    return response['Items']


@ssm.cache(parameter='/production/variable/foo', max_age_in_seconds=120)
def query_confidential(event, context):

    employee_id = event['employee_id']

    client = boto3.client('dynamodb')
    response = client.query(
        TableName=os.environ['db_name'],
        IndexName="GSI-1",
        Select='ALL_ATTRIBUTES',
        KeyConditionExpression="sk = :employeeID",
        ExpressionAttributeValues={":employeeID": {"S": employee_id}}
    )
    return response['Items']
