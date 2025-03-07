variable "athena_workgroup_name" {
  description = "Athena workgroup name"
  type        = string
  default     = "my_athena_workgroup"
}

variable "s3_query_results_bucket" {
  description = "S3 bucket for Athena query results"
  type        = string
  default     = "my-athena-results-bucket1122"
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-2"
}

variable "cluster_name" {
  type        = string
  description = "Name of the ECS Cluster"
  default     = "my-ecs-cluster"
}

variable "task_family" {
  type        = string
  description = "ECS Task Family Name"
  default     = "my-ecs-task"
}

variable "execution_role_arn" {
  description = "IAM Role ARN for ECS Execution"
}

variable "task_role_arn" {
  description = "IAM Role ARN for ECS Task"
}

variable "cpu" {
  type        = string
  description = "CPU for ECS Task"
  default     = "512"
}

variable "memory" {
  type        = string
  description = "Memory for ECS Task"
  default     = "1024"
}

variable "container_definitions" {
  description = "JSON-formatted container definitions"
}

variable "service_name" {
  type        = string
  description = "ECS Service Name"
  default     = "my-ecs-service"
}

variable "desired_count" {
  description = "Number of ECS tasks to run"
  type        = number
  default     = 2
}

variable "subnet_ids" {
  description = "List of subnet IDs for ECS service"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of security groups for ECS service"
  type        = list(string)
}
variable "glue" {
  description = "Configuration for the Glue setup"
  type        = map(string)
}