resource "aws_ssm_parameter" "bucket_name" {
  name = "/victim/endpoint_bucket/name"
  type = "String"
  value = aws_s3_bucket.test_endpoint.id
}

resource "aws_ssm_parameter" "bucket_arn" {
  name = "/victim/endpoint_bucket/arn"
  type = "String"
  value = aws_s3_bucket.test_endpoint.arn
}

resource "aws_ssm_parameter" "private_subnet" {
  name = "/victim/private_subnet/id"
  type = "String"
  value = aws_subnet.private.id
}

resource "aws_ssm_parameter" "lambda_security_group" {
  name = "/victim/lambda_security_group/id"
  type = "String"
  value = aws_security_group.lambda_security_group.id
}
