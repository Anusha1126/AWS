
---

## AWS Glue Data Catalog (Metadata Management) 

###  What is AWS Glue Data Catalog?
AWS Glue Data Catalog is a centralized metadata repository that automatically discovers, catalogs, and manages metadata for datasets across AWS services. It acts as a catalog for Athena, Redshift Spectrum, and EMR.

###  Why is it used?
- **Automated Schema Discovery**: Detect schema changes automatically.
- **Centralized Metadata**: Unified view of data assets.
- **Multi-Service Support**: Integrates with Athena, Redshift, EMR, and S3.
- **Partition Awareness**: Optimizes partitioned datasets.
- **Serverless & Managed**: AWS handles infrastructure and scaling.

###  When to use Glue Data Catalog?
- When using Athena or Redshift Spectrum to query S3 data.
- For managing large data lakes with schema changes.
- To automate ETL workflows with AWS Glue jobs.

---

##  Directory Structure
```
src/
│── environments/test/
│   ├── terraform.tfvars  # Defines variables specific to the test environment
│
│── modules/
│   ├── glue/
│   │   ├── main.tf       # Contains Glue Catalog and Crawler definitions
│   │   ├── outputs.tf    # Outputs Glue catalog details
│   │   ├── variables.tf  # Defines variables for Glue configurations
│
│── glue.tf               # Deploys Glue using the Glue module
│── variables.tf          # Defines global Terraform variables
```

modules/glue/main.tf

```hcl
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
```

modules/glue/outputs.tf

```hcl
output "glue_database_name" {
  description = "The Glue catalog database name"
  value       = aws_glue_catalog_database.glue_db.name
}

output "glue_crawler_name" {
  description = "The Glue Crawler name"
  value       = aws_glue_crawler.glue_crawler.name
}
```

modules/glue/varaibles.tf

```hcl
variable "glue" {
  description = "Configuration for the Glue setup"
  type        = map(string)
}
```

glue.tf

```hcl
provider "aws" {
  region = "us-east-1" 
}
module "glue" {
  source = "./modules/glue"
  glue   = var.glue
}
```

---

## Amazon Athena (Serverless Query Service) 

###  What is Amazon Athena?
Amazon Athena is a serverless, interactive query service that allows you to run SQL queries directly on data stored in Amazon S3. It uses Presto and Trino as its query engines and does not require infrastructure management.

### Why is it used?
- **Serverless**: No infrastructure management required.
- **Cost-Effective**: Pay only for the data scanned (per TB).
- **Ad-Hoc Analysis**: Ideal for quick data insights.
- **Supports Open Formats**: Query data in CSV, JSON, Parquet, and ORC formats.
- **Integration**: Natively integrates with AWS Glue Data Catalog for metadata management.

###  When to use Athena?
- For ad-hoc queries on data lakes in S3.
- Exploratory data analysis without ETL overhead.
- When quick results are needed for semi-structured data like logs and IoT data.

---

##  Directory Structure
```
src/
│── environments/test/
│   ├── terraform.tfvars  # Defines variables specific to the test environment
│
│── modules/
│   ├── athena/
│   │   ├── main.tf       # Contains Athena database definitions
│   │   ├── outputs.tf    # Outputs Athena database details
│   │   ├── variables.tf  # Defines variables for Athena configurations
│
│── athena.tf             # Deploys Athena using the Athena module
│── variables.tf          # Defines global Terraform variables
```

modules/athena/main.tf

```hcl
resource "random_id" "unique_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "results-athena-anusha" {
  bucket = "my-athena-results-bucket-${random_id.unique_suffix.hex}"
}

resource "aws_s3_bucket_public_access_block" "results-athena-anusha" {
  bucket                  = aws_s3_bucket.results-athena-anusha.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_athena_workgroup" "athena_wg" {
  name = var.athena_workgroup_name

  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.results-athena-anusha.bucket}/results-query-1/"

      encryption_configuration {
        encryption_option = var.athena_enforce_encryption ? "SSE_S3" : "CSE_KMS"
      }
    }
  }
}
```

modules/athena/outputs.tf

```hcl
output "athena_workgroup_arn" {
  description = "ARN of the Athena workgroup"
  value       = aws_athena_workgroup.athena_wg.arn
}

output "s3_athena_results_bucket" {
  description = "S3 bucket for Athena query results"
  value       = aws_s3_bucket.results-athena-anusha.bucket
}
```

modules/athena/varaibles.tf

```hcl
variable "athena_workgroup_name" {
  description = "Name of the Athena workgroup"
  type        = string
}

variable "s3_query_results_bucket" {
  description = "S3 bucket to store Athena query results"
  type        = string
}

variable "athena_enforce_encryption" {
  description = "Enable encryption for Athena query results"
  type        = bool
  default     = true
}
```

athena.tf

```hcl
module "athena" {
  source                   = "./modules/athena"
  athena_workgroup_name     = "my_athena_workgroup"
  s3_query_results_bucket   = "my-athena-results-bucket"
  athena_enforce_encryption = true
}
```

## ECS
---

## Amazon ECS (Elastic Container Service) 🛠️

### What is Amazon ECS?
Amazon ECS is a fully managed container orchestration service that helps deploy, manage, and scale containerized applications. It supports Docker containers and runs on EC2 instances or AWS Fargate.

### Why is it used?
- **Simplified Container Management**: Deploy, monitor, and scale containers easily.
- **Supports Docker**: Run Docker containers natively.
- **Flexible Deployment**: ECS with EC2 or Fargate.
- **Seamless Integration**: Works with ALB, CloudWatch, IAM, and EFS.
- **High Availability**: Multi-AZ container distribution.

### When to use ECS?
- For scalable, containerized applications.
- Microservices architectures.
- Simplified container orchestration without Kubernetes.

---
```
src/
│── environments/test/
│   ├── terraform.tfvars  # Defines variables specific to the test environment
│
│── modules/
│   ├── ecs/
│   │   ├── main.tf       # Contains ECS cluster and task definitions
│   │   ├── outputs.tf    # Outputs ECS cluster details
│   │   ├── variables.tf  # Defines variables for ECS configurations
│   │   ├── task_definition.json  # Contains task definition for the container
│
│── ecs.tf                # Deploys ECS using the ECS module
│── variables.tf          # Defines global Terraform variables
```

modules/ecs/main.tf

```hcl
resource "aws_ecs_cluster" "ecs_cluster" {
  name = var.cluster_name
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = replace("${var.cluster_name}-ecs-task-execution-role", "/[^a-zA-Z0-9-_]/", "")

  assume_role_policy = jsonencode({
    Version = "2012-10-17", 
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "ecs_task" {
  family                   = var.task_family
  container_definitions    = file("${path.module}/task_definition.json")
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
}

resource "aws_ecs_service" "ecs_service" {
  name            = var.service_name
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = var.security_group_ids
    assign_public_ip = true
  }
}
```

modules/ecs/outputs.tf

```hcl
output "ecs_cluster_id" {
  value = aws_ecs_cluster.ecs_cluster.id
}

output "ecs_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "ecs_task_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}
```

modules/ecs/varaibles.tf

```hcl
variable "cluster_name" {
  description = "Name of the ECS cluster"
  default     = "ecs-cluster-prod"
  type        = string
}
variable "task_family" {
  type        = string
  default     = "ecs-task-family"
  description = "Family name of the ECS task definition"
}
variable "execution_role_arn" {
  description = "ARN of the IAM role for ECS task execution"
}
variable "task_role_arn" {
    description = "ARN of the IAM role for ECS task"
}
variable "cpu" {
    type        = string
    default     = "512"
    description = "CPU units for the ECS task"
}
variable "memory" {
  description = "The amount of memory for the ECS task"
  type        = string
  default     = "1024"
}
variable "container_definitions" {
    description = "Container definitions in JSON format"
    type        = string
}
variable "service_name" {
    description = "Name of the ECS service"
}
variable "desired_count" {
    description = "Number of desired task instances"
}
variable "subnet_ids" { 
    type = list(string) 
    description = "List of subnet IDs for the ECS service"
    }
variable "security_group_ids" { 
    type = list(string) 
    description = "List of security group IDs for the ECS service"
}
```

variables.tf

```hcl
variable "athena_workgroup_name" {
  description = "Athena workgroup name"
  type        = string
  default     = "my_athena_workgroup"
}

variable "s3_query_results_bucket" {
  description = "S3 bucket for Athena query results"
  type        = string
  default     = "my-athena-results-bucket1122"
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-2"
}

variable "cluster_name" {
  type        = string
  description = "Name of the ECS Cluster"
  default     = "my-ecs-cluster"
}

variable "task_family" {
  type        = string
  description = "ECS Task Family Name"
  default     = "my-ecs-task"
}

variable "execution_role_arn" {
  description = "IAM Role ARN for ECS Execution"
}

variable "task_role_arn" {
  description = "IAM Role ARN for ECS Task"
}

variable "cpu" {
  type        = string
  description = "CPU for ECS Task"
  default     = "512"
}

variable "memory" {
  type        = string
  description = "Memory for ECS Task"
  default     = "1024"
}

variable "container_definitions" {
  description = "JSON-formatted container definitions"
}

variable "service_name" {
  type        = string
  description = "ECS Service Name"
  default     = "my-ecs-service"
}

variable "desired_count" {
  description = "Number of ECS tasks to run"
  type        = number
  default     = 2
}

variable "subnet_ids" {
  description = "List of subnet IDs for ECS service"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of security groups for ECS service"
  type        = list(string)
}
variable "glue" {
  description = "Configuration for the Glue setup"
  type        = map(string)
}
```

ecs.tf

```hcl
module "ecs" {
  source = "./modules/ecs"
  cluster_name = var.cluster_name
  task_family = var.task_family
  execution_role_arn = var.execution_role_arn
  task_role_arn = var.task_role_arn
  cpu = var.cpu
  memory = var.memory
  container_definitions = var.container_definitions
  service_name = var.service_name
  desired_count = var.desired_count
  subnet_ids = var.subnet_ids
  security_group_ids = var.security_group_ids
}
```

environments/test/terraform.tfvars

```hcl

#athena vars
athena = {
    workgroup_name          = "test-athena-workgroup"
    database_name           = "test_database"
    query_results_location  = "s3://test-athena-results-bucket/"
    encryption_configuration = "SSE_S3"
}


athena_workgroup_name = "athena_workgroup"


glue = {
  database_name  = "glue_db"
  crawler_name   = "glue_crawler"
  iam_role       = "arn:aws:iam::970547378939:role/gluerole"
  s3_target_path = "s3://data-processed-anusha/"
}
aws_region          = "us-east-1"
cluster_name        = "ecs-cluster-prod"
task_family         = "ecs-task-family"
cpu                = "512"
memory             = "1024"
service_name       = "ecs-service"
desired_count      = 1

execution_role_arn = "arn:aws:iam::970547378939:role/ecs-task-execution-role"
task_role_arn      = "arn:aws:iam::970547378939:role/ecs-task-role"

# Subnet IDs and Security Groups for ECS Deployment in the test environment
subnet_ids         = ["subnet-0d2988fb6c33e42ee", "subnet-06657ebcd43872469", "subnet-086fd4f92aa5393d2"]
security_group_ids = ["sg-01be7c620263ea11f"]

container_definitions = "[{\"name\":\"test-container\",\"image\":\"nginx\",\"cpu\":512,\"memory\":1024,\"essential\":true,\"portMappings\":[{\"containerPort\":80,\"hostPort\":80}]}]"
```

![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/1.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/2.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/3.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/4.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/5.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/6.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/7.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/8.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week3/Day2/images/9.png?raw=true) 
