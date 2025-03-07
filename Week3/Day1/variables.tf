#s3 vars
variable "bucket" {
  description = "Configuration for the S3 bucket"
  type = map(string)
}

variable "upload_file" {
  description = "Path to the file that should be uploaded to S3"
  type        = map(string)
}

#iam vars
variable "iam" {
  description = "IAM configuration settings"
  type        = map(string)
  default = {
    user_name   = "my-iam-user"
    role_name   = "my-iam-role"
    policy_name = "my-iam-policy"
    inline_policy_name = "my-inline-policy"
  }
}

# rds

variable "rds" {
  description = "RDS configuration"
  type = map(any)
  default = {
    db_identifier         = "rds-mysql"
    db_allocated_storage  = 20
    db_storage_type       = "gp2"
    db_instance_class     = "db.t3.micro"
    db_username           = "admin"
    db_password           = "993132Ray"
    vpc_id                = "vpc-04ea66058deab0279"
    db_publicly_accessible = true
    db_skip_final_snapshot = true
    
    db_multi_az            = false
  }
}

# Redshift Configuration
variable "redshift" {
  description = "Redshift Configuration"
  type = map(string)
}
variable "aws_region" {
  description = "AWS region"
  type        = string
}



variable "athena" {
  description = "Athena configurations"
  type = map(any)
  default = {
    workgroup_name          = "test-athena-workgroup"
    database_name           = "test_database"
    query_results_location  = "s3://test-athena-results-bucket/"
    encryption_configuration = "SSE_S3"
  }
}

variable "glue" {
  description = "Configuration for the Glue setup"
  type        = map(string)
}