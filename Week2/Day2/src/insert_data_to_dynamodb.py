import boto3
import botocore

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

# Table name
TABLE_NAME = "Employees"

# Function to check if table exists
def table_exists(table_name):
    try:
        dynamodb.Table(table_name).load()
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        else:
            raise  # Raise other unexpected errors

# Check if table exists before creating
if not table_exists(TABLE_NAME):
    # Create the table
    response = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "EMPLOYEE_ID", "KeyType": "HASH"}  # Partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "EMPLOYEE_ID", "AttributeType": "S"}  # String type
        ],
        ProvisionedThroughput={  # Remove this if using On-Demand Mode
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )

    # Wait until the table exists
    response.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
    print(f"✅ Table '{TABLE_NAME}' created successfully. Check AWS Console → DynamoDB.")
else:
    print(f"⚠️ Table '{TABLE_NAME}' already exists. No need to create it.")
