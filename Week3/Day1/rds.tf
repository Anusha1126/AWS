module "rds_mysql" {
  source                = "./modules/rds"
  db_identifier         = var.rds["db_identifier"]
  db_allocated_storage  = var.rds["db_allocated_storage"]
  db_storage_type       = var.rds["db_storage_type"]
  db_instance_class     = var.rds["db_instance_class"]
  db_username           = var.rds["db_username"]
  db_password           = var.rds["db_password"]
  vpc_id                = var.rds["vpc_id"]
  db_publicly_accessible = var.rds["db_publicly_accessible"]
  db_skip_final_snapshot = var.rds["db_skip_final_snapshot"]
  db_multi_az            = var.rds["db_multi_az"]
}
    