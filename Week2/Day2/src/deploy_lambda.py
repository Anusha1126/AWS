import boto3
import zipfile
import os

# AWS clients
lambda_client = boto3.client('lambda', region_name="us-east-1")

# Lambda function details
LAMBDA_FUNCTION_NAME = "S3ToDynamoDBLambda"
LAMBDA_ROLE_ARN = "arn:aws:iam::970547378939:role/service-role/HelloWorldPythonLambda-role-e61pistk"

# Path to the Lambda function file
lambda_function_file = "Week2/Day2/src/lambda_function.py"  # Update this path if the file is located elsewhere

# Check if the Lambda function file exists
if not os.path.isfile(lambda_function_file):
    raise FileNotFoundError(f"The file {lambda_function_file} does not exist.")

# Package Lambda function
lambda_zip = "function.zip"
with zipfile.ZipFile(lambda_zip, "w") as zf:
    zf.write(lambda_function_file, arcname="lambda_function.py")

# Check if the Lambda function exists
try:
    lambda_client.get_function(FunctionName=LAMBDA_FUNCTION_NAME)
    function_exists = True
except lambda_client.exceptions.ResourceNotFoundException:
    function_exists = False

# Create or update the Lambda function
if function_exists:
    # Update Lambda function code
    with open(lambda_zip, "rb") as f:
        lambda_client.update_function_code(
            FunctionName=LAMBDA_FUNCTION_NAME,
            ZipFile=f.read()
        )
    print(f"✅ Lambda Function {LAMBDA_FUNCTION_NAME} updated successfully.")
else:
    # Create Lambda function
    with open(lambda_zip, "rb") as f:
        lambda_client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime="python3.9",
            Role=LAMBDA_ROLE_ARN,
            Handler="lambda_function.lambda_handler",
            Code={"ZipFile": f.read()},
            Timeout=30,
            MemorySize=128
        )
    print(f"✅ Lambda Function {LAMBDA_FUNCTION_NAME} created successfully.")