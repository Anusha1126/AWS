import boto3
import time

# AWS Configuration
AWS_REGION = "us-east-1"
DB_INSTANCE_IDENTIFIER = "rds-mysql-source"
DB_NAME = "mydatabase"
DB_USER = "admin"
DB_PASSWORD = "mypassword"
DB_INSTANCE_CLASS = "db.t3.micro"
DB_ENGINE = "mysql"
ALLOCATED_STORAGE = 20  # 20GB Storage
SECURITY_GROUP_ID = "sg-01be7c620263ea11f"

# Create RDS client
rds = boto3.client("rds", region_name=AWS_REGION)

# Create the RDS instance
try:
    response = rds.create_db_instance(
        DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER,
        DBName=DB_NAME,
        Engine=DB_ENGINE,
        MasterUsername=DB_USER,
        MasterUserPassword=DB_PASSWORD,
        DBInstanceClass=DB_INSTANCE_CLASS,
        AllocatedStorage=ALLOCATED_STORAGE,
        PubliclyAccessible=True,  # Set to False for internal use only
        VpcSecurityGroupIds=[SECURITY_GROUP_ID],  # Using the provided Security Group ID
        MultiAZ=False,  # Set explicitly for a single AZ instance
    )
    print(f"RDS instance creation initiated: {response['DBInstance']['DBInstanceIdentifier']}")

    # Wait for the RDS instance to be available
    print("Waiting for the RDS instance to become available...")
    waiter = rds.get_waiter("db_instance_available")
    waiter.wait(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
    print(f"RDS instance '{DB_INSTANCE_IDENTIFIER}' is now active.")

    # Get the endpoint of the DB instance
    db_instance = rds.describe_db_instances(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
    endpoint = db_instance["DBInstances"][0]["Endpoint"]["Address"]
    print(f"The database instance is accessible at: {endpoint}")

except Exception as e:
    print(f"Failed to create RDS instance. Error: {e}")