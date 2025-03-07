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