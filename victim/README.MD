# Victim

This directory holds the victim setup.

Installation:

    $ cd Terraform
    $ tf apply --auto-approve
    $ cd ../serverless
    $ sls deploy

## Notes

We simulate a compromised package (lambda-cache), the compromised package is in `serverless/evil_lambda_cache/caching_logic.py` from line 30 onwards. There are 4 possible data exfiltration methods, API, S3, BYOC & BYOC_wCode.

### API

In the API method, the credentials are exfiltrated via a simple HTTP POST to an API the attacker controls. This attack method is the simplest, but requires the lambda to have internet access (not an unusual thing)

### S3

In the S3 method, the credentials are exfiltrated via putting a file (with the credentials) into a public S3 bucket that the attacker controls. This method requires the lambda function to have access to S3 (either via internet, or an VPC endpoint with no restrictions). It also requires the lambda to have the `s3:PutObject` and `s3:PutObjectACL` permissions on any S3 bucket (rare!)

### BYOC

In the Bring-your-Credential (BYOC) attack, we use the same approach as the 'S3', but instead we use the attackers credentials to bypass the need of the `s3:PutObject` and `s3:PutObjectAcl` permission -- the bucket in question can also be private (since it's using the attackers credentials).

### BYOC_wCode

Same as BYOC, but in this attack scenario, we exfiltrate the code as well as the credentials. Especially for scripted languages this can be very useful.

### credential encryption

In this specific case, I encrypted the attacker credentials, using the account ID of the victim accounts, this was done for novel purposes as I never actually published this package.

## Uninstall

    $ cd Terraform
    $ tf destroy --auto-approve
    $ cd ../serverless
    $ sls remove