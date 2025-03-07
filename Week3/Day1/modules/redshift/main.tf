resource "aws_security_group" "redshift_sg" {
  name        = "redshift-security-group"
  description = "Allow Redshift access"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Open access (Restrict in production)
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "redshift-security-group"
  }
}

resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier    = var.redshift_identifier
  node_type            = var.redshift_node_type
  cluster_type         = var.redshift_cluster_type
  number_of_nodes      = var.redshift_cluster_type == "multi-node" ? var.redshift_number_of_nodes : null
  database_name        = var.redshift_db_name
  master_username      = var.redshift_master_username
  master_password      = var.redshift_master_password
  publicly_accessible  = true
  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet.name
  vpc_security_group_ids    = [aws_security_group.redshift_sg.id]
  skip_final_snapshot       = true

  tags = {
    Name        = var.redshift_identifier
    Environment = "Dev"
  }
}

resource "aws_redshift_subnet_group" "redshift_subnet" {
  name       = "redshift-subnet-group"
  subnet_ids = ["subnet-0d2988fb6c33e42ee", "subnet-086fd4f92aa5393d2", "subnet-0d45fd32a8e45595b"	]

  tags = {
    Name = "redshift-subnet-group"
  }
}