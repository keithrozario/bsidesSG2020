import boto3
import json
import os

def main(event, context):
    print(event)

    s3 = boto3.client('s3')
    tmp_file = '/tmp/creds.json'

    with open(tmp_file, 'wb') as f:
        s3.download_fileobj(
            event['Records'][0]['s3']['bucket']['name'],
            event['Records'][0]['s3']['object']['key'],
            f
        )

    with open(tmp_file, 'r') as f:
        creds = json.loads(f.read())
    
    write_to_dynamo(creds)

    return

def write_to_dynamo(creds: dict()):

    client =  boto3.client('dynamodb')

    Item = dict()
    for k in creds.keys():
        Item[k] = {'S': creds[k]}

    response = client.put_item(
    TableName=os.environ['DYNAMO_TABLE'],
    Item=Item)

    return response