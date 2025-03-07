import boto3
import time

AWS_REGION = "us-east-1"
CLUSTER_ID = "my-redshift-cluster"

redshift = boto3.client("redshift", region_name=AWS_REGION)

while True:
    cluster_info = redshift.describe_clusters(ClusterIdentifier=CLUSTER_ID)["Clusters"][0]
    cluster_status = cluster_info["ClusterStatus"]
    print(f"Cluster Status: {cluster_status}")

    if cluster_status == "available":
        endpoint = cluster_info["Endpoint"]["Address"]
        print(f"✅ Redshift Cluster Endpoint: {endpoint}")
        break
    time.sleep(30)  # Check status every 30 seconds
