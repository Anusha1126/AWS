import boto3

# Initialize the DMS client
dms_client = boto3.client('dms')

# Define configuration variables
replication_instance_id = "mysql-postgre-rep-instance"
replication_instance_class = "dms.t3.medium"
allocated_storage_gb = 50
security_group_ids = ["sg-01be7c620263ea11f"]  # Replace with your security group ID
PubliclyAccessible= True
engine_version = "3.5.3"
MultiAZ= False

try:
    # Create a DMS replication instance
    response = dms_client.create_replication_instance(
        ReplicationInstanceIdentifier=replication_instance_id,
        ReplicationInstanceClass=replication_instance_class,
        AllocatedStorage=allocated_storage_gb,
        VpcSecurityGroupIds=security_group_ids,
        PubliclyAccessible=PubliclyAccessible,
        MultiAZ=MultiAZ,
        EngineVersion=engine_version
    )

    print(f"Replication instance '{replication_instance_id}' is being created.")

except Exception as e:
    print(f"Error creating DMS replication instance: {str(e)}")