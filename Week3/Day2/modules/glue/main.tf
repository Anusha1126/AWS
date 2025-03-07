resource "aws_glue_catalog_database" "glue_db" {
  name = var.glue["database_name"]
}

resource "aws_glue_crawler" "glue_crawler" {
  name          = var.glue["crawler_name"]
  role          = var.glue["iam_role"]
  database_name = aws_glue_catalog_database.glue_db.name

  s3_target {
    path = var.glue["s3_target_path"]
  }
}