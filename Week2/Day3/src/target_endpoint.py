import boto3

# AWS Configurations
aws_region = "us-east-1"

# DMS & PostgreSQL Details
dms_client = boto3.client("dms", region_name=aws_region)
postgres_endpoint_identifier = "dms-postgre-target-endpoint"
postgres_cluster_endpoint = "database-postgre.c2xmycgk2zok.us-east-1.rds.amazonaws.com"
postgres_db_name = "mydatabase"
postgres_username = "admin"
postgres_password = "mypassword"  # Secure this properly

# Create PostgreSQL Target Endpoint
def create_postgres_target_endpoint():
    try:
        response = dms_client.create_endpoint(
            EndpointIdentifier=postgres_endpoint_identifier,
            EndpointType="target",
            EngineName="postgres",
            Username=postgres_username,
            Password=postgres_password,
            ServerName=postgres_cluster_endpoint,
            Port=5432,
            DatabaseName=postgres_db_name,
            SslMode="require"  # Ensure secure connection
        )
        print("PostgreSQL Target Endpoint:", response["Endpoint"]["EndpointArn"])
    
    except Exception as e:
        print("Error creating PostgreSQL target endpoint:", str(e))

# Execute the function
create_postgres_target_endpoint()