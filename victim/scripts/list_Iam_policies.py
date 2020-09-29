import boto3
import json
from parliament import analyze_policy_string

session = boto3.session.Session(profile_name="Serverless", region_name='ap-southeast-1')
client = session.client('iam')

inline_documents = list()
response = client.list_roles()
for role in response['Roles']:
    role_policies = client.list_role_policies(RoleName=role['RoleName'])['PolicyNames']
    for policy in role_policies:
        inline_document = client.get_role_policy(
            RoleName=role['RoleName'],
            PolicyName=policy,
        )['PolicyDocument']
        inline_documents.append(inline_document)

for doc in inline_documents:
    analyze_policy = analyze_policy_string(json.dumps(doc))
    for f in analyze_policy.findings:
        print(f)

