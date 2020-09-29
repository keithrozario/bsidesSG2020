resource "aws_ssm_parameter" "bucket_name" {
  name = "/attacker/public_bucket/name"
  type = "String"
  value = aws_s3_bucket.attackers_public_bucket.id
}

resource "aws_ssm_parameter" "bucket_arn" {
  name = "/attacker/public_bucket/arn"
  type = "String"
  value = aws_s3_bucket.attackers_public_bucket.arn
}