resource "random_id" "unique_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "results-athena-anusha" {
  bucket = "my-athena-results-bucket-${random_id.unique_suffix.hex}"
}

resource "aws_s3_bucket_public_access_block" "results-athena-anusha" {
  bucket                  = aws_s3_bucket.results-athena-anusha.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_athena_workgroup" "athena_wg" {
  name = var.athena_workgroup_name

  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.results-athena-anusha.bucket}/results-query-1/"

      encryption_configuration {
        encryption_option = var.athena_enforce_encryption ? "SSE_S3" : "CSE_KMS"
      }
    }
  }
}