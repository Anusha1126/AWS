variable "athena_workgroup_name" {
  description = "Name of the Athena workgroup"
  type        = string
}

variable "s3_query_results_bucket" {
  description = "S3 bucket to store Athena query results"
  type        = string
}

variable "athena_enforce_encryption" {
  description = "Enable encryption for Athena query results"
  type        = bool
  default     = true
}