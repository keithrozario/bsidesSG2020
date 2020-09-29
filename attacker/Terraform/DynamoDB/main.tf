resource "aws_dynamodb_table" "t" {

  name             = var.table_name
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "AWS_LAMBDA_FUNCTION_NAME"
  range_key        = "AWS_ACCESS_KEY_ID"
  stream_enabled   = false
  
  attribute {
    name = "AWS_LAMBDA_FUNCTION_NAME"
    type = "S"
  }

  attribute {
    name = "AWS_ACCESS_KEY_ID"
    type = "S"
  }

}

resource "aws_ssm_parameter" "table_arn" {
  type  = "String"
  description = "Arn of DynamoDB Table"
  name  = "/attacker/dynamo_table/arn"
  value = aws_dynamodb_table.t.arn
}

resource "aws_ssm_parameter" "table_name" {
  type  = "String"
  description = "Arn of DynamoDB Table"
  name  = "/attacker/dynamo_table/name"
  value = aws_dynamodb_table.t.id
}