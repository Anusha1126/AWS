provider "aws" {
  region = "us-east-1" 
}
module "glue" {
  source = "./modules/glue"
  glue   = var.glue
}