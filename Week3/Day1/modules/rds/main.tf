
resource "aws_security_group" "rds_sg" {
  name        = "${var.db_identifier}-sg"
  description = "Allow MySQL inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.db_identifier}-sg"
  }
}

resource "aws_db_instance" "rds_mysql_server" {
  identifier             = var.db_identifier
  allocated_storage      = var.db_allocated_storage
  storage_type           = var.db_storage_type
  engine                 = "mysql"
  instance_class         = var.db_instance_class
  username               = var.db_username
  password               = var.db_password
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = var.db_publicly_accessible
  skip_final_snapshot    = var.db_skip_final_snapshot
  multi_az               = var.db_multi_az

  tags = {
    Name = var.db_identifier
  }
}
