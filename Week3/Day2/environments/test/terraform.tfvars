
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