provider "aws" {
  profile = "ServerlessAttacker"
  region = "ap-southeast-1"
}

module s3 {
  source = "./s3"
  bucket_prefix  = "attackers-bucket"
  iam_role_name = "attacker-byoc"
}

module DynamoDB {
  source = "./DynamoDB"
  table_name  = "access_keys"
}

output "iam_acess_key_id" {
  value = module.s3.iam_acess_key_id
}

output "iam_secret_access_key" {
  value = module.s3.iam_secret_access_key
}