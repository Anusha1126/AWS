variable "iam_user" {
  description = "IAM User Name"
  type        = string
}

variable "iam_role" {
  description = "IAM Role Name"
  type        = string
}

variable "policy_name" {
  description = "IAM Policy Name"
  type        = string
}

variable "inline_policy_name" {
  description = "Inline policy"
  type        = string
}

variable "bucket" {
  description = "Configuration for the S3 bucket"
  type        = map(string)
}