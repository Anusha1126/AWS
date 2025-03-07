# Create IAM User
resource "aws_iam_user" "user" {
  name = var.iam_user
}

# Create IAM Role
resource "aws_iam_role" "role" {
  name = var.iam_role

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# Create IAM Policy (Full Access)
resource "aws_iam_policy" "policy" {
  name        = var.policy_name
  description = "Full access to all resources"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

# Attach Policy to IAM User
resource "aws_iam_user_policy_attachment" "user_policy_attach" {
  user       = aws_iam_user.user.name
  policy_arn = aws_iam_policy.policy.arn
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "role_policy_attach" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn
}

# Attach an Inline Policy to the IAM Role
resource "aws_iam_role_policy" "inline_policy" {
  name = var.inline_policy_name
  role = aws_iam_role.role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = [
        "s3:ListBucket",
        "s3:GetObject"
      ]
      Resource = [
        "arn:aws:s3:::${var.bucket["name"]}",  
        "arn:aws:s3:::${var.bucket["name"]}/*"
      ]
    }]
  })
}
