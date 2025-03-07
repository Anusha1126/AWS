output "iam_user" {
  value = aws_iam_user.user.name
}

output "iam_role_arn" {
  value = aws_iam_role.role.arn
}

output "policy_arn" {
  value = aws_iam_policy.policy.arn
}

output "inline_policy_name" {
  value = aws_iam_role_policy.inline_policy.name
}