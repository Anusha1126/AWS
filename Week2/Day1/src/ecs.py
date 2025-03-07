import boto3
import docker
import time
import subprocess

# AWS Configuration
AWS_REGION = "us-east-1"  # Change as needed
ECR_REPO_NAME = "my-app-repo"
ECS_CLUSTER_NAME = "my-ecs-cluster"
TASK_DEFINITION_NAME = "my-task-definition"
ECS_SERVICE_NAME = "my-ecs-service"
CONTAINER_NAME = "my-app"
IMAGE_TAG = "latest"

# Initialize AWS Clients
ecr_client = boto3.client("ecr", region_name=AWS_REGION)
ecs_client = boto3.client("ecs", region_name=AWS_REGION)
iam_client = boto3.client("iam")
docker_client = docker.from_env()

# Define the AWS region and ECR URI
region = "us-east-1"
ecr_uri = "970547378939.dkr.ecr us-east-1.amazonaws.com/my-app-repo"

# Command to get the login password
command = f"aws ecr get-login-password --region {region}"

try:
    # Get login password from AWS ECR
    password = subprocess.check_output(command, shell=True).strip()

    # Docker login command
    login_command = f"docker login --username AWS --password-stdin {ecr_uri}"

    # Execute the docker login command with the password passed to stdin
    login_process = subprocess.Popen(login_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = login_process.communicate(input=password)

    if login_process.returncode != 0:
        print(f"Error: {stderr.decode()}")
    else:
        print(f"Success: {stdout.decode()}")

except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")

# Step 1: Create an ECR Repository
def create_ecr_repo():
    try:
        response = ecr_client.create_repository(repositoryName=ECR_REPO_NAME)
        ecr_uri = response["repository"]["repositoryUri"]
        print(f"ECR Repository Created: {ecr_uri}")
        return ecr_uri
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        ecr_uri = f"{AWS_REGION}.dkr.ecr.amazonaws.com/{ECR_REPO_NAME}"
        print(f"ECR Repository already exists: {ecr_uri}")
        return ecr_uri

# Step 2: Authenticate Docker to AWS ECR
def authenticate_docker(ecr_uri):
    login_cmd = f"aws ecr get-login-password --region {AWS_REGION} | docker login --username AWS --password-stdin {ecr_uri}"
    subprocess.run(login_cmd, shell=True, check=True)
    print("Docker authenticated with ECR")

# Step 3: Build & Tag the Docker Image
def build_docker_image(ecr_uri):
    print("Building Docker image...")
    docker_client.images.build(path="/Users/sweetyrachupallechinnaboreddy/Desktop/my-app", tag=f"{ecr_uri}:{IMAGE_TAG}")
    print("Docker Image Built Successfully")

# Step 4: Push Image to ECR
def push_docker_image(ecr_uri):
    print("⏳ Pushing Docker image to ECR...")
    subprocess.run(f"docker tag {CONTAINER_NAME}:latest {ecr_uri}:latest", shell=True, check=True)
    subprocess.run(f"docker push {ecr_uri}:latest", shell=True, check=True)
    print("✅ Docker Image Pushed to ECR")

# Step 5: Create ECS Cluster
def create_ecs_cluster():
    try:
        ecs_client.create_cluster(clusterName=ECS_CLUSTER_NAME)
        print(f"ECS Cluster Created: {ECS_CLUSTER_NAME}")
    except Exception as e:
        print(f"Cluster already exists or error: {e}")

# Step 6: Register Task Definition
def register_task_definition(ecr_uri):
    response = ecs_client.register_task_definition(
        family=TASK_DEFINITION_NAME,
        networkMode="awsvpc",
        executionRoleArn="arn:aws:iam::970547378939:role/ecsTaskExecutionRole",  # Update with your role
        containerDefinitions=[
            {
                "name": CONTAINER_NAME,
                "image": f"{ecr_uri}:latest",
                "memory": 512,
                "cpu": 256,
                "essential": True,
                "portMappings": [{"containerPort": 5000, "hostPort": 5000}],
            }
        ],
        requiresCompatibilities=["FARGATE"],
        memory="512",
        cpu="256"
    )
    print(f"✅ Task Definition Registered: {TASK_DEFINITION_NAME}")

# Step 7: Create ECS Service
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
                    "subnets": ["subnet-04f40ac67b7b5d800"],  # Update with your subnet IDs
                    "securityGroups": ["sg-0ee9220ccb0441046"],  # Update with your security group
                    "assignPublicIp": "ENABLED"
                }
            }
        )
        print(f"ECS Service Created: {ECS_SERVICE_NAME}")
    except ecs_client.exceptions.ServiceAlreadyExistsException:
        print(f"ECS Service '{ECS_SERVICE_NAME}' already exists.")

# Step 8: Deploy Everything
def deploy_to_ecs():
    ecr_uri = create_ecr_repo()
    authenticate_docker(ecr_uri)
    build_docker_image(ecr_uri)
    push_docker_image(ecr_uri)
    create_ecs_cluster()
    register_task_definition(ecr_uri)
    create_ecs_service()
    print("🚀 ECS Deployment Completed Successfully!")

# Run Deployment
deploy_to_ecs()
