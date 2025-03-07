provider "aws" {
  region = var.bucket["region"]
}

module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = var.bucket["name"]
  region      = var.bucket["region"]
  upload_file = var.upload_file["upload_file"]
}
