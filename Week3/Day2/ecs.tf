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