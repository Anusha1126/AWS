module "lambda" {
  source         = "./modules/lambda"

  region         = var.lambda["region"]
  function_name  = var.lambda["function_name"]
  runtime        = var.lambda["runtime"]
  handler        = var.lambda["handler"]
  s3_bucket      = var.lambda["s3_bucket"]
  s3_key         = var.lambda["s3_key"]
  memory_size    = var.lambda["memory_size"]
  timeout        = var.lambda["timeout"]
  role_name      = var.lambda["role_name"]
  role_policy    = var.lambda["role_policy"]
}