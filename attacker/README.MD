# Attacker

This directory holds the attacker setup.

Installation:

    $ cd Terraform
    $ tf apply --auto-approve
    $ cd ../serverless
    $ sls deploy

## Notes

Depending on the exfiltration method on the victim end, there are different lambda functions that handle the data separately.

### API

If the credentials are posted via API, the attacker will stand an API to receive a POST, and save the credentials into a DynamoDB table (created by the terraform scripts above)

### S3 & BYOC

There is a lambda that triggers whenever a file is put into the S3 bucket. The lambda parses the file (in json), and puts that data into the DynamoDB table

### Cred usage

There are lambda functions that read data from the DynamoDB, and use those credentials to perform actions in the victim account.