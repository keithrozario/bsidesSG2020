resource "aws_iam_user_policy" "byoc_policy" {
  name = "ByoCredsPolicy"
  user = aws_iam_user.byoc-user.name

  policy = <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ByoCreds",
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::${aws_s3_bucket.attackers_private_bucket.id}/you_got_hacked_*"

    },
    {
      "Sid": "DenyDangerousThings",
      "Effect": "Deny",
      "Action": "ec2:*",
      "Resource": "*"
    }
  ]
}
  EOF
}

resource "aws_iam_user" "byoc-user" {
  name = "serverless-attacker-user"
}

resource "aws_iam_access_key" "byoc-access-key" {
  user    = aws_iam_user.byoc-user.name
}