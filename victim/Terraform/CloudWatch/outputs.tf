
output "cloudwatch_log_group_arn" {
  value       = aws_cloudwatch_log_group.ct_log.arn
  description = "ARN of the log group"
}

output "cloudwatch_role_arn" {
  value       = aws_iam_role.ct_role.arn
  description = "ARN of role to assume"
}

output "cloudwatch_role_name" {
  value       = aws_iam_role.ct_role.name
  description = "Name of role to assume"
}