variable "cluster_name" {
  description = "Name of the ECS cluster"
  default     = "ecs-cluster-prod"
  type        = string
}
variable "task_family" {
  type        = string
  default     = "ecs-task-family"
  description = "Family name of the ECS task definition"
}
variable "execution_role_arn" {
  description = "ARN of the IAM role for ECS task execution"
}
variable "task_role_arn" {
    description = "ARN of the IAM role for ECS task"
}
variable "cpu" {
    type        = string
    default     = "512"
    description = "CPU units for the ECS task"
}
variable "memory" {
  description = "The amount of memory for the ECS task"
  type        = string
  default     = "1024"
}
variable "container_definitions" {
    description = "Container definitions in JSON format"
    type        = string
}
variable "service_name" {
    description = "Name of the ECS service"
}
variable "desired_count" {
    description = "Number of desired task instances"
}
variable "subnet_ids" { 
    type = list(string) 
    description = "List of subnet IDs for the ECS service"
    }
variable "security_group_ids" { 
    type = list(string) 
    description = "List of security group IDs for the ECS service"
}