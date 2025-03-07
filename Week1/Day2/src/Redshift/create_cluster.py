import boto3

# AWS Configuration
AWS_REGION = "us-east-1"  # Change if needed
CLUSTER_ID = "my-redshift-cluster"
DB_NAME = "dev"
MASTER_USERNAME = "admin"
MASTER_PASSWORD = "YourSecurePassword123"
NODE_TYPE = "dc2.large"  # Free-tier node type
NUMBER_OF_NODES = 1  # Single-node (free tier eligible)

# Create Redshift client
redshift = boto3.client("redshift", region_name=AWS_REGION)

# Create a Redshift Cluster
try:
    response = redshift.create_cluster(
        ClusterIdentifier=CLUSTER_ID,
        NodeType=NODE_TYPE,
        NumberOfNodes=NUMBER_OF_NODES,
        DBName=DB_NAME,
        MasterUsername=MASTER_USERNAME,
        MasterUserPassword=MASTER_PASSWORD,
        PubliclyAccessible=True,  # Allow external access
        ClusterType="single-node",  # Free-tier option
    )

    print(f"Creating Redshift Cluster: {CLUSTER_ID}")
    print("Cluster creation initiated. This may take a few minutes.")

except Exception as e:
    print("Error:", e)
