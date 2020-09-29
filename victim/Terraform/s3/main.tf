resource "aws_s3_bucket" "b" {
  bucket_prefix = "serverless-victim"
  acl    = "private"
  force_destroy = true
}

resource "aws_ssm_parameter" "bucket_name" {
  name  = "/victim/bucket/name"
  type  = "String"
  value = aws_s3_bucket.b.id
}

resource "aws_ssm_parameter" "bucket_arn" {
  name  = "/victim/bucket/arn"
  type  = "String"
  value = aws_s3_bucket.b.arn
}

resource "aws_s3_bucket_object" "object" {
  bucket = aws_s3_bucket.b.id
  key    = "secret.txt"
  source = "s3/secret.txt"
}
