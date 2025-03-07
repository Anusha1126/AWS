import boto3

# AWS Configuration
AWS_REGION = "us-east-1"  # Change as needed
ECS_CLUSTER_NAME = "my-elastic-cluster-1"
TASK_DEFINITION_NAME = "my-task-definition1"
ECS_SERVICE_NAME = "my-ecs-service-1"
CONTAINER_NAME = "my-app-1"

# Use a Public ECR Image (Example: Nginx)
ECR_PUBLIC_IMAGE_URI = "public.ecr.aws/nginx/nginx:latest"

# Initialize AWS Clients
ecs_client = boto3.client("ecs", region_name=AWS_REGION)

# Step 1: Create ECS Cluster
def create_ecs_cluster():
    try:
        ecs_client.create_cluster(clusterName=ECS_CLUSTER_NAME)
        print(f"✅ ECS Cluster Created: {ECS_CLUSTER_NAME}")
    except Exception as e:
        print(f"⚠️ Cluster already exists or error: {e}")

# Step 2: Register Task Definition using Public ECR Image
def register_task_definition():
    response = ecs_client.register_task_definition(
        family=TASK_DEFINITION_NAME,
        networkMode="awsvpc",
        executionRoleArn="arn:aws:iam::970547378939:role/ecsTaskExecutionRole",  # Update with your IAM Role
        containerDefinitions=[
            {
                "name": CONTAINER_NAME,
                "image": ECR_PUBLIC_IMAGE_URI,  # Using a public ECR image
                "memory": 512,
                "cpu": 256,
                "essential": True,
                "portMappings": [{"containerPort": 80, "hostPort": 80}],  # Change ports as needed
            }
        ],
        requiresCompatibilities=["FARGATE"],
        memory="512",
        cpu="256"
    )
    print(f"✅ Task Definition Registered: {TASK_DEFINITION_NAME}")

# Step 3: Create ECS Service
def create_ecs_service():
    try:
        ecs_client.create_service(
            cluster=ECS_CLUSTER_NAME,
            serviceName=ECS_SERVICE_NAME,
            taskDefinition=TASK_DEFINITION_NAME,
            desiredCount=1,
            launchType="FARGATE",
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": ["subnet-0d2988fb6c33e42ee"],  # Update with your subnet ID
                    "securityGroups": ["sg-01be7c620263ea11f"],  # Update with your security group
                    "assignPublicIp": "ENABLED"
                }
            }
        )
        print(f"✅ ECS Service Created: {ECS_SERVICE_NAME}")
    except ecs_client.exceptions.ServiceAlreadyExistsException:
        print(f"⚠️ ECS Service '{ECS_SERVICE_NAME}' already exists.")

# Step 4: Deploy Everything
def deploy_to_ecs():
    create_ecs_cluster()
    register_task_definition()
    create_ecs_service()
    print("🚀 ECS Deployment Completed Successfully!")

# Run Deployment
deploy_to_ecs()