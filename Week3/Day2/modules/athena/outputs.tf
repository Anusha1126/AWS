output "athena_workgroup_arn" {
  description = "ARN of the Athena workgroup"
  value       = aws_athena_workgroup.athena_wg.arn
}

output "s3_athena_results_bucket" {
  description = "S3 bucket for Athena query results"
  value       = aws_s3_bucket.results-athena-anusha.bucket
}