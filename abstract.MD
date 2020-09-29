# Attacking Lambda Functions

Serverless is a new paradigm for building apps, and requires us to forget about the old ideas, while learning new ones. But as developers learn new ways to build on serverless so too much must attackers and defenders.

We cover methods for attacking (and defending) serverless functions and architectures, focusing on the AWS ecosystem (Lambda, S3, DynamoDB and EventBridge).

Since functions in serverless are ephemeral, network scans are useless as there are no 'servers' or IPs to scan with serverless functions. For most lambda functions outside of a VPC -- there won't even be a victim network, as the functions run on shared VPC hosted by Amazon. 

Instead most of the attacks occur at the application level, by first extracting the Access Keys from the function, we're able to impersonate that function from outside of the victims network -- or even outside of AWS. For Lambda functions protected by VPC and Security Groups, we show how you might use the victims VPC-endpoints to exfiltrate data to an attackers S3 bucket. Using this, an attacker can then move laterally across the service, by exploiting loosely defined permissions, a common mistake with Lambda Functions.

Finally, We show, how defenders can detect stolen keys, by referencing CloudTrail logs, and how we might invalidate compromised keys.