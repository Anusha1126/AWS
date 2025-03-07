# Amazon Athena and ECS Demo

## Introduction
Amazon Athena is a **serverless interactive query service** that allows you to analyze data in **Amazon S3** using **SQL**. It is built on **Presto** and provides a cost-effective solution for querying large datasets without managing infrastructure.

## Key Benefits
- **Serverless** – No infrastructure management.
- **Cost-Effective** – Pay-per-query pricing.
- **Flexible** – Supports multiple formats (CSV, JSON, Parquet, ORC, Avro).
- **Scalable** – Handles large-scale queries efficiently.
- **Integrated** – Works with AWS Glue, QuickSight, and BI tools.

---

## Core Components
- **Amazon S3** – Stores raw data.
- **Schema-on-Read** – No predefined schema required.
- **Presto Query Engine** – High-speed distributed querying.
- **AWS Glue** – Manages metadata & schema.
- **JDBC/ODBC Connectivity** – Connects to BI tools (Tableau, QuickSight, Power BI).

---

## AWS Glue and Athena Setup

### Data Storage and Crawling
Initially, data is stored in AWS Glue and fetched from S3.

![Crawler](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/24.png?raw=true)

---

### Setting Up Athena
If using Athena for the first time, setup is required. The results are stored in a specified S3 location.

![Athena Setup](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/25.png?raw=true)

---

### Query Execution in Athena
Results after executing a query in Athena:

![Athena Result](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/26.png?raw=true)

Results are stored in the location:

![Athena Result](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/1.png?raw=true)

Now, the database and table are created directly in Athena:

![Athena Result](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/2.png?raw=true)

Query execution result:

![Athena Result](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/3.png?raw=true)

---

## Creating Table, Database, and Query Execution Using Python (Boto3)

```python
import boto3
import time

# AWS Configuration
AWS_REGION = "us-east-1"  # Change to your AWS region
S3_OUTPUT = "s3://glue-bucket-products/query-results/"  # Change to your S3 bucket for Athena query results
S3_CSV_PATH = "s3://my-employees/employee/"  # Path to your CSV file in S3 (directory)

# Initialize Athena Client
athena_client = boto3.client("athena", region_name=AWS_REGION)

def run_athena_query(query, database="default"):
    """Execute an Athena query and return the execution ID."""
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": database},
        ResultConfiguration={"OutputLocation": S3_OUTPUT},
    )
    return response["QueryExecutionId"]

def wait_for_query(query_execution_id):
    """Wait until the query execution completes."""
    while True:
        response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response["QueryExecution"]["Status"]["State"]
        print(f"Query status: {status}")  # Debug print

        if status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            if status != "SUCCEEDED":
                print(f"Query failed with status: {status}")
                print("Error message:", response["QueryExecution"]["Status"]["StateChangeReason"])
            return status
        time.sleep(2)

def get_query_results(query_execution_id):
    """Fetch and display the results of the query."""
    response = athena_client.get_query_results(QueryExecutionId=query_execution_id)
    rows = response["ResultSet"]["Rows"]
    for row in rows:
        print([col.get("VarCharValue", "") for col in row["Data"]])

# 1️⃣ **Create Database**
create_db_query = "CREATE DATABASE IF NOT EXISTS employeee;"
query_id = run_athena_query(create_db_query)
if wait_for_query(query_id) == "SUCCEEDED":
    print("✅ Database 'employeee' created successfully!")

# 2️⃣ **Create Table**
create_table_query = f"""
CREATE EXTERNAL TABLE IF NOT EXISTS employeee.Employees (
    EMPLOYEE_ID INT,
    FIRST_NAME STRING,
    LAST_NAME STRING,
    EMAIL STRING,
    PHONE_NUMBER STRING,
    HIRE_DATE STRING,
    JOB_ID STRING,
    SALARY DOUBLE,
    COMMISSION_PCT STRING,
    MANAGER_ID INT,
    DEPARTMENT_ID INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ',',
    'field.delim' = ','
)
LOCATION '{S3_CSV_PATH}'
TBLPROPERTIES ('has_encrypted_data'='false');
"""

query_id = run_athena_query(create_table_query, database="employeee")
if wait_for_query(query_id) == "SUCCEEDED":
    print("✅ Table 'Employees' created successfully!")

# 3️⃣ **Query Data**
query_data_sql = "SELECT * FROM employeee.Employees LIMIT 10;"
query_id = run_athena_query(query_data_sql, database="employeee")

query_status = wait_for_query(query_id)
if query_status == "SUCCEEDED":
    print("✅ Data queried successfully! Check results in:", S3_OUTPUT)
    get_query_results(query_id)
else:
    print(f"❌ Query failed with status: {query_status}")
```

![Athena Result](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/4.png?raw=true)

---

## Executing Queries via AWS CLI

```sh
# Create Database
aws athena start-query-execution \
    --query-string "CREATE DATABASE my_employee;" \
    --result-configuration "OutputLocation=s3://glue-bucket-products/query-results/"

# Create External Table in Database
aws athena start-query-execution \
    --query-string "CREATE EXTERNAL TABLE my_employee.my_employees (
        EMPLOYEE_ID INT,
        FIRST_NAME STRING,
        LAST_NAME STRING,
        EMAIL STRING,
        PHONE_NUMBER STRING,
        HIRE_DATE STRING,
        JOB_ID STRING,
        SALARY DOUBLE,
        COMMISSION_PCT STRING,
        MANAGER_ID INT,
        DEPARTMENT_ID INT
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION 's3://my-employees/employee/';" \
    --result-configuration "OutputLocation=s3://glue-bucket-products/query-results/"--result-configuration "OutputLocation=s3://glue-bucket-products/query-resul

```

![Athena Result](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/5.png?raw=true) 

# AWS ECS: Elastic Container Service

## Overview
Elastic Container Service (ECS) is a container orchestration service that automates the deployment, management, and scaling of Docker containers without the complexity of maintaining your own container infrastructure.

## Key Features
- Maintains the desired count of tasks
- Integrates with AWS Fargate (serverless) and EC2 instances for container management

## Key Components of AWS ECS

### 1. Clusters
Logical group of ECS resources (EC2 or Fargate) that manage groups of tasks or services.
- **EC2:** Register and manage the EC2 instances yourself.
- **Fargate:** Serverless, managed automatically.
- **External (ECS Anywhere):** For on-premise servers, register and manage remotely.

### 2. Task Definitions
Blueprint that defines how a container should run, including:
- CPU and memory allocation
- Environment variables
- IAM roles

### 3. Tasks
A running instance of a task definition.

### 4. Services
Ensures the desired number of tasks are running, supports auto-scaling, and integrates with Elastic Load Balancer (ELB).

### 5. Container Agent
Runs on EC2 instances and manages communication with ECS.

### 6. Load Balancing
Uses ALB/NLB for distributing traffic to ECS tasks:
- **Application Load Balancer (ALB):** Handles HTTP/HTTPS traffic with advanced routing.
- **Network Load Balancer (NLB):** Manages TCP/UDP traffic for high performance and low latency.
- **Classic Load Balancer (CLB):** Legacy load balancer.

## ECS vs Docker
![Athena Result](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/6.png?raw=true) 
| Feature  | Docker | ECS |
|----------|--------|-----|
| Management | Manual container management, networking, and scaling | Automated deployment, scaling, networking, and monitoring |
| Scaling | Manual unless combined with Kubernetes or Swarm | Automated scaling with AWS Auto Scaling and Fargate |
| Deployment | Single-machine and multi-environment container management | Orchestration, scheduling, and scaling across multiple instances in a serverless environment |

## Demo Flow: Deploying an Application on AWS ECS

### Step 1: Set Up an ECS Cluster
1. Navigate to AWS ECS Console → Create Cluster
2. Choose Fargate (serverless) or EC2-based cluster

### Step 2: Define a Task Definition
1. Go to Task Definitions → Create new
2. Define:
   - Container image (from ECR or Docker Hub)
   - Resource allocation (CPU, memory)
   - Logging (AWS CloudWatch)
   - IAM roles

### Step 3: Create a Service
1. Select cluster → Create Service
2. Choose:
   - Deployment type: Fargate or EC2
   - Load balancer (ALB for HTTP/HTTPS apps)
   - Auto-scaling policies

### Step 4: Deploy and Monitor
1. Use `aws ecs list-tasks` to check running containers
2. View logs via AWS CloudWatch
3. Scale tasks dynamically based on CPU/Memory utilization

## Backend Framework Considerations for ECS
ECS supports various backend frameworks (Node.js, Python, Java, etc.), with the following considerations:
- **Statelessness:** Use Redis or RDS for persistent data.
- **Logging & Monitoring:** Use CloudWatch logs and AWS X-Ray for request tracing.
- **Health Checks:** Define health check endpoints for ALB.
- **Security:** Implement IAM roles, Security Groups, and Secrets Manager for authentication.

## Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Container Startup Failures | Check ECS task logs in CloudWatch for errors. Verify task definition settings. |
| Networking Issues | Ensure correct VPC, subnets, security groups, and service discovery settings. |
| Scaling Bottlenecks | Use Application Auto Scaling with CPU/memory metrics. |
| Task Placement Issues | Use EC2 capacity providers or switch to Fargate for on-demand scaling. |
| Long Deployment Times | Optimize container build using multi-stage Docker builds and Amazon ECR caching. |
| Persistent Storage Needs | Use EFS (Elastic File System) integration with ECS tasks. |


## Created Cluster
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/7.png?raw=true)

## Created Task Definition
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/8.png?raw=true)

## Created Service
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/9.png?raw=true)

## Opened the Task and Retrieved Public IP (NGINX Created)
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/10.png?raw=true)

### Cleanup Steps:
- Stop the task
- Delete the service
- Delete the cluster
- Deregister the task definition

---

## Deploying an Application on ECS Using Python (Boto3)

```python
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
                "image": ECR_PUBLIC_IMAGE_URI,
                "memory": 512,
                "cpu": 256,
                "essential": True,
                "portMappings": [{"containerPort": 80, "hostPort": 80}]
            }
        ]
    )
    print(f"✅ Task Definition Registered: {TASK_DEFINITION_NAME}")

# Step 3: Deploy Service
def create_service():
    response = ecs_client.create_service(
        cluster=ECS_CLUSTER_NAME,
        serviceName=ECS_SERVICE_NAME,
        taskDefinition=TASK_DEFINITION_NAME,
        launchType="FARGATE",
        desiredCount=1,
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": ["subnet-xxxxxxxx"],  # Replace with your subnet ID
                "securityGroups": ["sg-xxxxxxxx"],  # Replace with your security group ID
                "assignPublicIp": "ENABLED"
            }
        }
    )
    print(f"✅ ECS Service Created: {ECS_SERVICE_NAME}")

# Run Deployment
deploy_to_ecs()    

# Execute Steps
create_ecs_cluster()
register_task_definition()
create_service()
```
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/21.png?raw=true)
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/22.png?raw=true)

## Using AWS CLI:

### Create an Amazon Elastic Container Registry (ECR)
```sh
aws ecr create-repository --repository-name my-app-repo --region us-east-1
```
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/12.png?raw=true)

### Get Repository URI
```sh
aws ecr describe-repositories --query "repositories[?repositoryName=='my-app-repo'].repositoryUri" --output text
```
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/13.png?raw=true)

### Authenticate Docker with ECR
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/14.png?raw=true)
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/15.png?raw=true)

### Pull the Image
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/16.png?raw=true)

#### Run the following command in CMD to pull the image:
```sh
docker pull public.ecr.aws/nginx/nginx:latest
```

#### Check if the image is downloaded:
```sh
docker images
```

### Tag the Image (Optional)
```sh
docker tag public.ecr.aws/nginx/nginx:latest my-nginx:latest
```

### Run the Docker Container
```sh
docker run -d -p 8080:80 public.ecr.aws/nginx/nginx:latest
```
- `-d`: Runs in detached mode (background)
- `-p 8080:80`: Maps port 8080 on your local machine to 80 inside the container

### Check Running Containers
```sh
docker ps
```

### Access the Running Container
Open a web browser and go to:
```
http://localhost:8080
```
You should see the default NGINX welcome page.
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/17.png?raw=true)

---

## Created the Cluster
```sh
aws ecs create-cluster --cluster-name my-elastic-cluster
```
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/18.png?raw=true)
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/19.png?raw=true)

## Task Definition
![Docker](https://github.com/Anusha1126/AWS/blob/main/Week2/Day1/images/20.png?raw=true)


## Best Practices for AWS ECS
- Use **Fargate** for serverless, managed compute.
- Leverage **ECS service discovery** for microservices.
- Secure containers with **IAM roles** and **Secrets Manager**.
- Monitor with **AWS CloudWatch, X-Ray, and CloudTrail**.
- Optimize costs using **Spot Instances** for EC2 clusters.







