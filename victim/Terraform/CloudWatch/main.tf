resource "aws_cloudwatch_log_group" "ct_log" {
  name = var.log_group_name
  retention_in_days = 1
  tags = {
    Environment = "victim"
  }
}


resource "aws_iam_role" "ct_role" {
  name = var.iam_role_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


resource "aws_iam_role_policy" "ct_policy" {
  name = "CloudTrailtoCloudWatch"
  role = aws_iam_role.ct_role.id

  policy = <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailCreateLogStream2014110",
      "Effect": "Allow",
      "Action": "logs:CreateLogStream",
      "Resource": "arn:aws:logs:*:*:log-group:${var.log_group_name}:log-stream:*"

    },
    {
      "Sid": "AWSCloudTrailPutLogEvents20141101",
      "Effect": "Allow",
      "Action": [
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:*:*:log-group:${var.log_group_name}:log-stream:*"
      ]
    }
  ]
}
  EOF
}
