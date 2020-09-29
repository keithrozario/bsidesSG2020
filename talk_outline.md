# Talk Outline

## Introduction to Serverless Architectures

* Covering terminologies and high level overview of what 'serverless' means, in comparison to regular 3-tier architectures.
* Focus on FaaS (Lambda), Storage (S3) and Databases (dynamoDB)

## Deep dive into Access Keys in AWS Lambda

* Understand the basics of an AWS Access Key and how they're populated into a Lambda function
* Talk about IAM roles of a lambda
* What this looks like in CloudTrail (AWS's EventLog)

## Compromising a Lambda

* DEMO: Use a malicious 3rd-party dependency to compromise a function and exfiltrate the access keys of the function


## Circumventing Network level controls

* For Lambda functions in a Virtual Private Cloud (VPC) with no internet access
* We use the VPC-endpoints to exfiltrate data within AWS, from the victims account to an S3 bucket owned by the attacker
* This can be done via using the victims loosely defined permissions, or using a Bring-your-own-credential attack
* We can also exfiltrate the code of the function to the bucket as well, especially useful for script languages typical in Lambda
* DEMO: Demonstrate exfil credentials and code from a locked-down function via VPC-endpoint to an attacker controlled S3 bucket.

## Exploiting loose permissions

* Once in possession of the access keys, we can then iterate through the permissions
* And then move laterally by accessing resources using the functions credentials
* Here we demonstrate how, an attacker can access confidential data attributes in DynamoDB, by exploiting loose permissions typical a Single-table designs
* Finally we can also demonstrate how we're able to trigger other lambda functions -- by placing events onto EventBridge
* EventBridge permissions are all-or-nothing, and hence any compromised credential to put events on the bridge, can put any event on the bridge
* DEMO: Using credentials from previous example to access sensitive attributes on a DynamoDB table

## Detecting Stolen keys

* Access Keys in Lambda are injected into the function at cold-start, from there they have a tight affinity to the IP address (it never changes)
* Using this we're able to detect a compromised credential, a technique popularized by Security engineers at Netflix
* From there, we also demonstrate how we're able to remediate the issue, by redeploying a new version of the function with a new role, while deleting the previous IAM role rendering all previous keys invalid -- but keeping the function working.

## Conclusion

* Modern serverless architectures no longer treat the cloud as a simple Data center to put servers, but we're now consuming more higher level resources from them
* Understanding how to protect these cloud architecture requires a deep understanding of the platform, and specifically for AWS, how Lambda works, and more importantly how IAM roles should be configured.
