output "redshift_endpoint" {
  value = aws_redshift_cluster.redshift_cluster.endpoint
}

output "redshift_identifier" {
  value = aws_redshift_cluster.redshift_cluster.cluster_identifier
}

output "security_group_id" {
  value = aws_security_group.redshift_sg.id
}