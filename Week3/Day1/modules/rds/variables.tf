
variable "db_identifier" {
  description = "The identifier for the RDS instance"
  type        = string
}

variable "db_allocated_storage" {
  description = "The allocated storage in gigabytes"
  type        = number
}

variable "db_storage_type" {
  description = "The storage type (e.g., gp2, io1)"
  type        = string
}


variable "db_instance_class" {
  description = "The instance class for the RDS instance"
  type        = string
}

variable "db_username" {
  description = "Username for the database"
  type        = string
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "vpc_id" {
  description = "VPC ID where RDS will be created"
  type        = string
}

variable "db_publicly_accessible" {
  description = "Whether the database instance is publicly accessible"
  type        = bool
  default     = true
}

variable "db_skip_final_snapshot" {
  description = "Determines whether a final DB snapshot is created before the instance is deleted"
  type        = bool
  default     = true
}

variable "db_multi_az" {
  description = "Specifies if the RDS instance is multi-AZ"
  type        = bool
  default     = false
}
    