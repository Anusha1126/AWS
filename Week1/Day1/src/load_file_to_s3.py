import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region="us-east-1"):
    """Create an S3 bucket."""
    s3_client = boto3.client("s3", region_name=region)
    try:
        # Create bucket
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        print(f"Error: {e}")

def upload_object(bucket_name, object_name, file_path):
    """Upload a file to an S3 bucket."""
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded as '{object_name}' in bucket '{bucket_name}'.")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Define bucket name, region, file path, and object name
    bucket_name = "lambda-s3"  # Ensure the bucket name is valid
    region = "us-east-1"
    file_path = r"C:\Users\repal\OneDrive\Desktop\DataEngineeringPractice\DET_GEN_AI_2025_B4_WEEK_01-1\random_text.txt"  # Use raw string to avoid escape characters
    object_name = "random_text.txt"  # The name you want to give the file in the S3 bucket

    # Create the bucket (if it doesn't already exist)
    create_bucket(bucket_name, region)

    # Upload the .txt file to the S3 bucket
    upload_object(bucket_name, object_name, file_path)