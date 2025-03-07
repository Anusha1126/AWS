glue = {
  database_name  = "my_glue_db"
  crawler_name   = "my_glue_crawler"
  iam_role       = "arn:aws:iam::970547378939:role/gluerole"
  s3_target_path = "s3://my-test-terraform9/"
}

lambda = {
  region           = "us-east-1"
  function_name    = "my_lambda_function"
  runtime         = "python3.8"
  handler         = "lambda_function.lambda_handler"
  s3_bucket       = "my-terraform-test-bucket6"
  s3_key          = "lambda_function.zip"
  memory_size     = "128"
  timeout         = "15"
  role_name       = "roleforlambdatest"
  role_policy     = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}