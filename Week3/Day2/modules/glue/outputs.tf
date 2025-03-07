output "glue_database_name" {
  description = "The Glue catalog database name"
  value       = aws_glue_catalog_database.glue_db.name
}

output "glue_crawler_name" {
  description = "The Glue Crawler name"
  value       = aws_glue_crawler.glue_crawler.name
}