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
    bucket_name = "anusha-gallery-2"
    region = "us-east-1"
    object_name = "images/image.png"  # Folder 'images/' and file 'image.png'
    file_path = "C:\Downloads\Cloud.jpg"  # Update with the actual path to your file

    # Create bucket
    create_bucket(bucket_name, region)

    # Upload file
    upload_object(bucket_name, object_name, file_path)
