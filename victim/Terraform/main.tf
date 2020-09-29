provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}

module "VPC" {
    source = "./VPC"
}

module "secret_S3" {
  source = "./s3"
}

module "DynamoDB" {
    source     = "./DynamoDB"
    table_name = var.employee_table
}

module "CloudWatch"{
  source = "./CloudWatch"
  log_group_name = var.ct_log_group_name
  iam_role_name  = var.ct_iam_role_name
}

module "cloudtrail_s3_bucket" {
  source    = "git::https://github.com/cloudposse/terraform-aws-cloudtrail-s3-bucket.git?ref=master"
  namespace = var.aws_profile
  stage     = "victim"
  name      = "app"
  region    = var.aws_region
}

module "cloudtrail" {
  source                        = "git::https://github.com/cloudposse/terraform-aws-cloudtrail.git?ref=master"
  namespace                     = var.aws_profile
  stage                         = "victim"
  name                          = "app"
  enable_log_file_validation    = "false"
  include_global_service_events = "true"
  is_multi_region_trail         = "false"
  enable_logging                = "true"
  s3_bucket_name                = module.cloudtrail_s3_bucket.bucket_id
  cloud_watch_logs_group_arn    = module.CloudWatch.cloudwatch_log_group_arn
  cloud_watch_logs_role_arn     = module.CloudWatch.cloudwatch_role_arn
}

resource "aws_ssm_parameter" "foo" {
  name  = "/production/variable/foo"
  type  = "String"
  value = "bar"
}