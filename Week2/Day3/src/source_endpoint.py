import boto3

# Initialize the AWS DMS client
dms_client = boto3.client('dms')

# Define configuration variables for the source endpoint (RDS MySQL)
source_endpoint_id = "dms-mysql-source"
source_endpoint_type = "source"
source_engine_name = "mysql"
rds_username = "admin"  # Replace with your RDS username
rds_password = "mypassword"  # Replace with your RDS password
rds_server_name = "rds-mysql-source.c2xmycgk2zok.us-east-1.rds.amazonaws.com"  # Replace with your actual RDS endpoint
rds_port = 3306  # Default MySQL port
rds_database_name = "mydatabase"  # Replace with your actual database name

try:
    # Create the DMS source endpoint
    response = dms_client.create_endpoint(
        EndpointIdentifier=source_endpoint_id,
        EndpointType=source_endpoint_type,
        EngineName=source_engine_name,
        Username=rds_username,
        Password=rds_password,
        ServerName=rds_server_name,
        Port=rds_port,
        DatabaseName=rds_database_name
    )

    print(f"Source endpoint '{source_endpoint_id}' has been successfully created!")
    print(f"MySQL RDS Endpoint: {rds_server_name}:{rds_port}")
    print(f"Database Name: {rds_database_name}")
    print("Check the AWS DMS console to verify endpoint details.")

except Exception as e:
    print(f" Error creating MySQL source endpoint: {str(e)}")