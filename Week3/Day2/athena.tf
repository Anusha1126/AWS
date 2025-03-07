module "athena" {
  source                   = "./modules/athena"
  athena_workgroup_name     = "my_athena_workgroup"
  s3_query_results_bucket   = "my-athena-results-bucket"
  athena_enforce_encryption = true
}