module "redshift_cluster" {
  source                  = "./modules/redshift"
  redshift_identifier     = var.redshift["identifier"]
  redshift_node_type      = var.redshift["node_type"]
  redshift_cluster_type   = var.redshift["cluster_type"]
  redshift_number_of_nodes = var.redshift["number_of_nodes"]
  redshift_db_name        = var.redshift["db_name"]
  redshift_master_username = var.redshift["master_username"]
  redshift_master_password = var.redshift["master_password"]
  vpc_id                 = var.redshift["vpc_id"]
  aws_region = var.aws_region

}