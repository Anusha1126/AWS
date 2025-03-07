variable "region" {
  description = "The AWS region"
  type        = string
}

variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "upload_file" {
  description = "Path to the file to upload to S3"
  type        = string 
}