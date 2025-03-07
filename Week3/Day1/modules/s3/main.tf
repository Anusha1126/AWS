resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name
  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_object" "uploaded_file" {
  bucket = var.bucket_name  # Use the existing bucket variable
  key    = basename(var.upload_file)  # Extract filename to use as object key
  source = var.upload_file  # Local file to upload
  acl    = "private"
}