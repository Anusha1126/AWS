module "iam" {
  source     = "./modules/iam"
  iam_user   = var.iam["user_name"]
  iam_role   = var.iam["role_name"]
  policy_name = var.iam["policy_name"]
  inline_policy_name = var.iam["inline_policy_name"]
  bucket            = var.bucket
}