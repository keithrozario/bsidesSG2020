import logging
import boto3
import os
from evil_lambda_cache import ssm

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@ssm.cache(parameter='/production/variable/foo', max_age_in_seconds=120)
def main(event, context):
    var = getattr(context, 'foo')

    client = boto3.client('s3')
    response = client.put_object(
        Bucket=os.environ['bucket_name'],
        Body="Driving in my car".encode('utf-8'),
        Key=context.function_name.split("-")[-1]
    )

    response = client.list_objects(
        Bucket=os.environ['bucket_name']
    )

    return [item['Key'] for item in response['Contents']]
