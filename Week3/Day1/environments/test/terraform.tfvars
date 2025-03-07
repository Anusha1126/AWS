#bucket vars
bucket={
    name     ="anusha-unique-testing-bucket-021725",
    region   ="us-east-1"
}

upload_file = {
    upload_file = "./modules/s3/file_to_s3.txt"
}

iam = {
  user_name   = "iam-user"
  role_name   = "iam-role"
  policy_name = "iam-policy"
  inline_policy_name = "inline-policy"
}

#rds vars
rds =  {
    db_identifier         = "rds-mysql"
    db_allocated_storage  = 20
    db_storage_type       = "gp2"
    db_instance_class     = "db.t3.micro"
    db_username           = "admin"
    db_password           = "993132Ray"
    vpc_id                = "vpc-073fc5ebc5ada6517"
    db_publicly_accessible = true
    db_skip_final_snapshot = true
    db_multi_az            = false
}

aws_region = "us-east-1"
redshift = {
  identifier      = "my-redshift-cluster"
  node_type       = "dc2.large"
  cluster_type    = "single-node"
  number_of_nodes = "1"
  db_name         = "myredshiftdb"
  master_username = "awsadmin"
  master_password = "SecurePassword123"
  vpc_id          = "vpc-073fc5ebc5ada6517"
  
}
