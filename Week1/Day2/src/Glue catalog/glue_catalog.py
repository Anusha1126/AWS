import boto3
import os
import time
import botocore.exceptions

# AWS Configuration
AWS_REGION = "us-east-2"
BUCKET_NAME = "my-csv-bucket"
LOCAL_CSV_FILE = r"C:\Users\repal\OneDrive\Desktop\DataEngineeringPractice\DET_GEN_AI_2025_B4_WEEK_01-1\layoffs.csv"
S3_OBJECT_NAME = "employees.csv"
GLUE_DATABASE_NAME = "employees_db"
GLUE_CRAWLER_NAME = "employees_crawler"
IAM_ROLE_NAME = "AWSGlueServiceRole"

# Initialize AWS clients
s3_client = boto3.client("s3", region_name=AWS_REGION)
glue_client = boto3.client("glue", region_name=AWS_REGION)


def create_s3_bucket(bucket_name, region):
    """Creates an S3 bucket if it doesn't exist."""
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists. Skipping creation.")
        else:
            print(f"Error creating bucket: {e}")


def upload_file_to_s3(bucket_name, local_file, s3_object_name):
    """Uploads a file to an S3 bucket."""
    try:
        s3_client.upload_file(local_file, bucket_name, s3_object_name)
        print(f"File '{local_file}' uploaded to S3 bucket '{bucket_name}' as '{s3_object_name}'.")
    except botocore.exceptions.ClientError as e:
        print(f"Error uploading file: {e}")


def get_or_create_glue_database(database_name):
    """Creates a Glue database if it doesn't exist."""
    try:
        glue_client.get_database(Name=database_name)
        print(f"Glue database '{database_name}' already exists.")
    except glue_client.exceptions.EntityNotFoundException:
        glue_client.create_database(DatabaseInput={"Name": database_name})
        print(f"Glue database '{database_name}' created successfully.")


def get_or_create_glue_crawler(crawler_name, database_name, s3_path, role_name):
    """Creates or updates an AWS Glue Crawler."""
    try:
        crawler = glue_client.get_crawler(Name=crawler_name)
        existing_s3_target = crawler["Crawler"]["Targets"]["S3Targets"][0]["Path"]

        if existing_s3_target != s3_path:
            print(f"Updating crawler '{crawler_name}' to use S3 path: {s3_path}")
            glue_client.update_crawler(
                Name=crawler_name,
                Role=role_name,
                DatabaseName=database_name,
                Targets={"S3Targets": [{"Path": s3_path}]},
            )
        else:
            print(f"Glue Crawler '{crawler_name}' already exists and is correctly configured.")
    except glue_client.exceptions.EntityNotFoundException:
        print(f"Creating Glue Crawler '{crawler_name}' with S3 path: {s3_path}")
        glue_client.create_crawler(
            Name=crawler_name,
            Role=role_name,
            DatabaseName=database_name,
            Targets={"S3Targets": [{"Path": s3_path}]},
            TablePrefix="",
        )


def start_glue_crawler(crawler_name):
    """Starts the Glue Crawler and waits for completion."""
    print(f"Starting Glue Crawler '{crawler_name}'...")
    glue_client.start_crawler(Name=crawler_name)

    # Wait for completion
    while True:
        response = glue_client.get_crawler(Name=crawler_name)
        status = response["Crawler"]["State"]
        if status == "READY":
            print(f"Glue Crawler '{crawler_name}' completed successfully.")
            break
        print(f"Crawler is running... Waiting 10 seconds.")
        time.sleep(10)


def check_glue_table(database_name):
    """Checks if the table was created in Glue after crawling."""
    tables = glue_client.get_tables(DatabaseName=database_name)["TableList"]
    table_names = [table["Name"] for table in tables]

    if table_names:
        print(f"Found tables in Glue database '{database_name}': {table_names}")
    else:
        print(f"No tables found in Glue database '{database_name}'. Check S3 path and file format.")


if __name__ == "__main__":
    # Step 1: Create S3 bucket
    create_s3_bucket(BUCKET_NAME, AWS_REGION)

    # Step 2: Upload CSV file to S3
    if os.path.exists(LOCAL_CSV_FILE):
        upload_file_to_s3(BUCKET_NAME, LOCAL_CSV_FILE, S3_OBJECT_NAME)
    else:
        print(f"Error: File '{LOCAL_CSV_FILE}' not found!")
        exit(1)

    # Step 3: Create Glue Database
    get_or_create_glue_database(GLUE_DATABASE_NAME)

    # Step 4: Create or Update Glue Crawler with correct S3 Path
    S3_PATH = f"s3://{BUCKET_NAME}/"
    get_or_create_glue_crawler(GLUE_CRAWLER_NAME, GLUE_DATABASE_NAME, S3_PATH, IAM_ROLE_NAME)

    # Step 5: Run Glue Crawler
    start_glue_crawler(GLUE_CRAWLER_NAME)

    # Step 6: Verify Table Exists
    check_glue_table(GLUE_DATABASE_NAME)