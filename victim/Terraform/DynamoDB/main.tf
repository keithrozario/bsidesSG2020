resource "aws_dynamodb_table" "t" {

  name             = var.table_name
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "pk"
  range_key        = "sk"
  stream_enabled   = false
  
  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  attribute {
    name = "colA"
    type = "S"
  }

  global_secondary_index {
    name            = "GSI-1"
    hash_key        = "sk"
    range_key       = "colA"
    projection_type = "ALL"
  }

  provisioner "local-exec" {
    command = "cd DynamoDB/data && python3 load_data.py"  # ensure you have an aws profile named 'Serverless' for victim account
  }

}

resource "aws_ssm_parameter" "table_arn" {
  type  = "String"
  description = "Arn of DynamoDB Table"
  name  = "/victim/${var.table_name}/arn"
  value = aws_dynamodb_table.t.arn
}