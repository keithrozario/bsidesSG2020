import boto3
import json

target_table = 'employee-db'

session = boto3.session.Session(profile_name="Serverless", region_name='ap-southeast-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(target_table)


with open('data_prefixed.json', 'r') as migration_file:
    items = json.loads(migration_file.read())['records']

with table.batch_writer() as batch:
    for k, item in enumerate(items):
        batch.put_item(Item=item)

# client = session.client('dynamodb')
# response = client.query(
#     TableName=target_table,
#     IndexName="GSI-1",
#     Select='ALL_ATTRIBUTES',
#     KeyConditionExpression="sk = :building AND colA = :seat",
#     ExpressionAttributeValues={":building": {"S": "LOC#WA | SEATTLE"},
#                                ":seat": {"S": "B01|f07|A27|R05"}}
# )

# print(response['Items'])

# employee_id = 'HRCONF#HR-EMPLOYEE1'
# response = client.query(
#     TableName=target_table,
#     IndexName="GSI-1",
#     Select='ALL_ATTRIBUTES',
#     KeyConditionExpression="sk = :employeeID",
#     ExpressionAttributeValues={":employeeID": {"S": employee_id}}
# )
# print(response['Items'])


