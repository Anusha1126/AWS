import boto3

# AWS Clients
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

# Your S3 Bucket and Lambda Function ARN
BUCKET_NAME = "s3-bucket-lambda"
LAMBDA_FUNCTION_NAME = "S3ToDynamoDBLambda"
LAMBDA_FUNCTION_ARN = f"arn:aws:lambda:us-east-1:970547378939:function:{LAMBDA_FUNCTION_NAME}"

# Grant S3 permission to invoke Lambda
try:
    lambda_client.add_permission(
        FunctionName=LAMBDA_FUNCTION_NAME,
        StatementId="S3InvokeLambda",
        Action="lambda:InvokeFunction",
        Principal="s3.amazonaws.com",
        SourceArn=f"arn:aws:s3:::{BUCKET_NAME}"
    )
    print(f"✅ Permission granted for S3 bucket {BUCKET_NAME} to invoke Lambda function {LAMBDA_FUNCTION_NAME}")
except lambda_client.exceptions.ResourceConflictException:
    print(f"⚠️ Permission already exists for S3 bucket {BUCKET_NAME} to invoke Lambda function {LAMBDA_FUNCTION_NAME}")

# Add S3 Event Notification to trigger Lambda
response = s3_client.put_bucket_notification_configuration(
    Bucket=BUCKET_NAME,
    NotificationConfiguration={
        'LambdaFunctionConfigurations': [
            {
                'LambdaFunctionArn': LAMBDA_FUNCTION_ARN,
                'Events': ['s3:ObjectCreated:*']
            }
        ]
    }
)

print("✅ S3 trigger set up successfully for bucket:", BUCKET_NAME)