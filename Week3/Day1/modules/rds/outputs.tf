
output "rds_instance_endpoint" {
  description = "The connection endpoint for the RDS instance"
  value       = aws_db_instance.rds_mysql_server.endpoint
}

output "rds_instance_arn" {
  description = "The ARN of the RDS instance"
  value       = aws_db_instance.rds_mysql_server.arn
}

output "rds_security_group_id" {
  description = "The security group ID for the RDS instance"
  value       = aws_security_group.rds_sg.id
}
    