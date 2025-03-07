# AWS Lambda  

## Introduction to AWS Lambda
AWS Lambda is a **serverless computing service** that runs code in response to events without the need to provision or manage servers. When an event occurs, AWS Lambda automatically triggers the code execution and manages the underlying compute resources.

### Key Features:
- Supports multiple languages: **Python, Node.js, Java, Go, .NET, Ruby**.
- Seamlessly integrates with AWS services like S3, DynamoDB, API Gateway, etc.
- **Scales automatically** based on demand.
- **Pay-as-you-go** pricing model.

## Distributed Application Architecture (DAA)
For any application, resources are allocated across three main components:
- **Frontend**
- **Backend**
- **Database**

If the frontend consumes **80% of resources** and the backend **only 20%**, it may lead to a deadlock situation. **Distributed Application Architecture (DAA)** resolves this by allocating dedicated resources to each component and scaling as needed. **AWS Lambda follows DAA principles** to ensure efficient scaling.

## Key Components of AWS Lambda
### Triggering Events
Lambda functions are invoked by:
- **API Gateway** – for REST APIs
- **S3 Events** – e.g., file uploads
- **DynamoDB Streams** – data changes
- **SNS/SQS** – asynchronous messaging
- **EventBridge** – scheduled jobs, event-driven workflows
- **CloudWatch** – monitoring & alerts

### Execution Environment
- Runs inside a secure, ephemeral container.
- Automatically scales with incoming requests.
- Configurable timeout, memory allocation, and concurrency.

### Permissions & Security
- IAM Roles & Policies control access.
- VPC Integration allows connections to RDS, Elasticache, etc.

### Backend Framework Integration
- Works with **Express.js** (Node.js) using API Gateway.
- Can be integrated with **FastAPI, Flask (Python)**.
- Uses **AWS SDK** to interact with AWS services (S3, DynamoDB, etc.).

## Real-Time Use Cases
1. **API Backend for Microservices**
   - Acts as a backend function behind API Gateway.
   - Handles user authentication, data processing, and database updates.
   - **Example:** Serverless e-commerce checkout integrating Stripe.

2. **Automated File Processing**
   - Lambda triggers on **S3 file uploads**.
   - **Example:** Image resizing service that processes images and stores them in another S3 bucket.

3. **Real-Time Data Processing**
   - Processes **streaming data** using **Kinesis & DynamoDB Streams**.
   - **Example:** Log analytics system that ingests logs and triggers alerts.

4. **Chatbots & AI Integration**
   - Powers serverless chatbots via **Amazon Lex**.
   - **Example:** A customer support chatbot retrieving data from DynamoDB.

5. **Scheduled Jobs & Alerts**
   - CloudWatch Events trigger Lambda at specific intervals.
   - **Example:** Daily database cleanup & report generation.

## Common Challenges & Solutions
| **Challenge**                   | **Solution**                                              |
|----------------------------------|----------------------------------------------------------|
| **Cold Start Issues**            | Use **Provisioned Concurrency** for reduced latency.    |
| **Limited Execution Time (15 min max)** | Use **Step Functions** for long-running tasks. |
| **Memory & CPU Limits**          | Optimize code, offload processing to S3, RDS, DynamoDB. |
| **Debugging & Logging**          | Use **AWS X-Ray & CloudWatch Logs** for monitoring.     |
| **Concurrency Limits**           | Implement **SQS or EventBridge** for controlled processing. |

## AWS Lambda vs Other AWS Compute Services
### AWS Lambda (Serverless)
- **Platform-as-a-Service (PaaS)**.
- Runs backend code without managing servers.
- No flexibility to log into compute instances.
- **Stateless system**.

### Amazon EC2 (Infrastructure-as-a-Service - IaaS)
- Offers **virtualized computing resources**.
- Requires manual OS selection and software installation.
- Provides flexibility with instance types, OS, and security configurations.
- **Stateful system**.

### AWS Elastic Beanstalk
- Deploy & manage applications without worrying about infrastructure.
- Requires selection of **EC2 instance type**.
- **Stateful system**.

## Benefits & Limitations of AWS Lambda
### Benefits
- **Serverless architecture** – No need to manage infrastructure.
- **Write and deploy code freely**.
- **No need to create VMs**.
- **Pay-as-you-go** model reduces costs.
- **Monitors performance automatically**.

### Limitations
- Maximum **disk space**: **512 MB** for runtime environment.
- Memory allocation: **128 MB - 3008 MB**.
- Function timeout: **Max 15 minutes (900 sec)**.
- Only supports **Python, C#, Java, Node.js, Go, Ruby** in the Lambda editor.

## How AWS Lambda Works
1. **Upload code** to AWS Lambda as one or more functions.
2. **Lambda executes the code** on behalf of the user.
3. After invocation, **Lambda provisions and manages the required servers**.
4. **Monitors & manages** the underlying infrastructure.

## Key Concepts in AWS Lambda
- **Functions** – Core execution unit.
- **Runtimes** – Execution environments.
- **Layers** – Reusable components for libraries, dependencies.
- **Log Streams** – Monitors function invocations via CloudWatch.

## AWS Lambda with S3 Integration
### Flow
1. **User** uploads an image to a **website**.
2. Image is stored in **S3**.
3. **S3 triggers** a Lambda function.
4. Lambda processes the image and invokes **microservices** as needed.

# AWS Lambda Function with S3 and CloudWatch Integration

## Overview
This project demonstrates the creation and deployment of an AWS Lambda function integrated with S3 for data storage and CloudWatch for logging. The Lambda function makes HTTP requests and handles errors gracefully. Additionally, we use an IAM role with basic Lambda policies and create a layer to include external dependencies.

## Steps Implemented

### 1. Creation of AWS Lambda Function
- Created a new AWS Lambda function via the AWS Console.
- Chose a new IAM role with basic Lambda policies.

![Lambda Function Creation](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/7.png?raw=true)
=======
![Lambda Function Creation](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/8.png?raw=true)

### 2. Destination Handling and S3 Integration
- Configured the Lambda function to save failed executions back to an S3 bucket.

=======
![S3 Failure Handling](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/9.png?raw=true)


### 3. CloudWatch Logging
- Logs are stored in CloudWatch, accessible for debugging after test execution.


![CloudWatch Logs](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/10.png?raw=true)
=======



## Lambda Function Code
The Lambda function makes an HTTP GET request to Google and returns the response.
```python
import json
import requests

def lambda_handler(event, context):
    url = "https://www.google.com"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            return {
                'status_code': 200,
                'body': json.dumps({
                    'message': 'Request success',
                    'content': response.text
                })
            }
        else:
            return {
                'status_code': response.status_code,
                'body': json.dumps({
                    'message': 'Request failed',
                    'error': response.reason
                })
            }
    except Exception as e:
        return {
            'status_code': 500,
            'body': json.dumps({
                'message': 'An error occurred',
                'error': str(e)
            })
        }
```

## 4. Handling External Dependencies with Lambda Layers
- Encountered an issue where `requests` module could not be imported.
- Created a Lambda Layer by installing `requests`:
```sh
pip install requests -t "C:\\Program Files\\Python313\\Lib\\site-packages"
```

![Lambda Layer Creation](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/11.png?raw=true)

Lambda Layers
![Lambda Layer Creation](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/30.png?raw=true)
![Lambda Layer Creation](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/31.png?raw=true)
=======


## 5. Deploying Lambda Function Using SDK (Boto3)
```python
import boto3
import json
import zipfile

# Initialize AWS Clients
lambda_client = boto3.client('lambda', region_name="us-east-1")

# Package Lambda Function
with zipfile.ZipFile("function.zip", "w") as zf:
    zf.write("C:\\Path\\To\\lambda.py")

# Deploy Lambda Function
response = lambda_client.create_function(
    FunctionName="Lambda-S3-Function",
    Runtime="python3.9",
    Role="arn:aws:iam::970547378939:role/service-role/HelloWorldPythonLambda-role-e61pistk",
    Handler="lambda_function.lambda_handler",
    Code={"ZipFile": open("function.zip", "rb").read()}
)

print(f"✅ Lambda Function Created: {response['FunctionArn']}")
```

![Lambda Deployment](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/12.png?raw=true)
=======


## 6. Uploading Data to S3 Using Boto3
```python
import boto3

bucket_name = "s3-bucket-lambda"
region = "us-east-1"
file_name = "C:\\Path\\To\\employees.csv"
s3_key = "input/employees.csv"

s3_client = boto3.client("s3", region_name=region)

try:
    s3_client.upload_file(file_name, bucket_name, s3_key)
    print(f"File {file_name} successfully uploaded to s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"Error uploading file: {e}")
```

![S3 Upload](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/15.png?raw=true)
Data in s3 bucket
![S3 Upload](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/19.png?raw=true)
## 7. UI Preview
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/16.png?raw=true)
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/17.png?raw=true)
=======
![S3 Upload](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/15.png?raw=true)
Data in s3 bucket
![S3 Upload](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/19.png?raw=true)
## 7. UI Preview

![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/18.png?raw=true)

Lambda_destination

```python
import boto3

# Initialize AWS clients
sns_client = boto3.client("sns")
sqs_client = boto3.client("sqs")
lambda_client = boto3.client("lambda")

# Replace with actual values
lambda_function_name = "S3ToDynamoDBLambda"
email_address = "anusha.careers.r@gmail.com"  # Replace with your email

### STEP 1: Create an SNS topic
sns_topic_response = sns_client.create_topic(Name="LambdaSuccessTopic")
sns_topic_arn = sns_topic_response["TopicArn"]
print(f"✅ SNS Topic Created: {sns_topic_arn}")

### STEP 2: Subscribe EMAIL to SNS for Notifications
sns_client.subscribe(
    TopicArn=sns_topic_arn,
    Protocol="email",
    Endpoint=email_address
)
print(f"✅ Email Subscription Created: {email_address} (Check your inbox to confirm!)")

### STEP 3: Create an SQS queue (Dead Letter Queue)
sqs_queue_response = sqs_client.create_queue(QueueName="LambdaFailureQueue")
sqs_queue_url = sqs_queue_response["QueueUrl"]

# Get SQS ARN
sqs_queue_attributes = sqs_client.get_queue_attributes(
    QueueUrl=sqs_queue_url,
    AttributeNames=["QueueArn"]
)
sqs_queue_arn = sqs_queue_attributes["Attributes"]["QueueArn"]
print(f"✅ SQS Dead Letter Queue Created: {sqs_queue_arn}")

### STEP 4: Subscribe SQS to SNS
sns_client.subscribe(
    TopicArn=sns_topic_arn,
    Protocol="sqs",
    Endpoint=sqs_queue_arn
)
print(f"✅ SQS Queue Subscribed to SNS Topic")

### STEP 5: Add SNS as a success destination and SQS as a failure destination for Lambda
lambda_client.put_function_event_invoke_config(
    FunctionName=lambda_function_name,
    DestinationConfig={
        "OnSuccess": {"Destination": sns_topic_arn},
        "OnFailure": {"Destination": sqs_queue_arn}
    }
)
print("✅ Lambda Destinations Configured:")
print(f"   - Success → SNS Topic: {sns_topic_arn}")
print(f"   - Failure → SQS Dead Letter Queue: {sqs_queue_arn}")

```
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/19.png?raw=true)
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/20.png?raw=true)
SNS
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/22.png?raw=true)
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/21.png?raw=true)
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/23.png?raw=true)

Created table in Dynamo DB
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/24.png?raw=true)
Inserted data into Dynamo DB
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/25.png?raw=true)
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/26.png?raw=true)
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/27.png?raw=true)
CloudWatch
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/28.png?raw=true)
DynamoDB: Data transferred to cloudwatch
![Lambda UI](https://github.com/Anusha1126/AWS/blob/main/Week2/Day2/images/29.png?raw=true)

## Conclusion
This project demonstrates:
- Creating and deploying an AWS Lambda function.
- Using Lambda Layers to handle dependencies.
- Storing logs in CloudWatch.
- Handling failure scenarios by saving data back to S3.
- Deploying Lambda using the AWS SDK (Boto3).
- Uploading data to S3 using Boto3.
AWS Lambda reduces infrastructure management and is highly scalable.
