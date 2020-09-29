resource "aws_s3_bucket" "attackers_public_bucket" {
  bucket_prefix = var.bucket_prefix
  force_destroy = true
}

resource "aws_s3_bucket_policy" "everyone_can_put" {
  bucket = aws_s3_bucket.attackers_public_bucket.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "Grant Everybody",
  "Statement": [{
    "Sid": "Grant Everybody",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:PutObject",
    "Resource": [
      "${aws_s3_bucket.attackers_public_bucket.arn}/creds*"
    ],
    "Condition": {}
  }]
}
POLICY
}

resource "aws_s3_bucket" "attackers_private_bucket" {
  bucket_prefix = var.bucket_prefix
  force_destroy = true
}
