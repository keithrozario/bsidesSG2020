output "iam_acess_key_id" {
  value = aws_iam_access_key.byoc-access-key.id
}

output "iam_secret_access_key" {
  value = aws_iam_access_key.byoc-access-key.secret
}