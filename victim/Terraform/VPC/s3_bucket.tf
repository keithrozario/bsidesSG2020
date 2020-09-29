resource "aws_s3_bucket" "test_endpoint" {
  bucket_prefix = "test-endpoint-bucket"
  acl    = "private"
}

resource "aws_s3_bucket_policy" "only_vpc" {
  bucket = aws_s3_bucket.test_endpoint.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "VPCe and SourceIP",
  "Statement": [{
    "Sid": "VPCe and SourceIP",
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": [
      "${aws_s3_bucket.test_endpoint.arn}/*"
    ],
    "Condition": {
      "StringNotLike": {
        "aws:sourceVpce": "${aws_vpc_endpoint.s3.id}"
      }
    }
  }]
}
POLICY
}