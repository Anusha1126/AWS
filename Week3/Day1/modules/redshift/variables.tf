variable "redshift_identifier" {
  description = "Redshift cluster identifier"
  type        = string
}

variable "redshift_node_type" {
  description = "Instance type for Redshift cluster"
  type        = string
}

variable "redshift_cluster_type" {
  description = "Cluster type (single-node or multi-node)"
  type        = string
}

variable "redshift_number_of_nodes" {
  description = "Number of nodes (only for multi-node clusters)"
  type        = number
  default     = 1
}

variable "redshift_db_name" {
  description = "Database name for Redshift"
  type        = string
}

variable "redshift_master_username" {
  description = "Master username for Redshift"
  type        = string
}

variable "redshift_master_password" {
  description = "Master password for Redshift"
  type        = string
  sensitive   = true
}

variable "vpc_id" {
  description = "VPC ID where the Redshift cluster will be deployed"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

