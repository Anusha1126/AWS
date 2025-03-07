import boto3
import time

# AWS Configuration
AWS_REGION = "us-east-1"  # Change to your AWS region
S3_OUTPUT = "s3://glue-bucket-products/query-results/"  # Change to your S3 bucket for Athena query results
S3_CSV_PATH = "s3://my-employees/employee/"  # Path to your CSV file in S3 (directory)

# Initialize Athena Client
athena_client = boto3.client("athena", region_name=AWS_REGION)

def run_athena_query(query, database="default"):
    """Execute an Athena query and return the execution ID."""
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": database},
        ResultConfiguration={"OutputLocation": S3_OUTPUT},
    )
    return response["QueryExecutionId"]

def wait_for_query(query_execution_id):
    """Wait until the query execution completes."""
    while True:
        response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response["QueryExecution"]["Status"]["State"]
        print(f"Query status: {status}")  # Debug print

        if status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            if status != "SUCCEEDED":
                print(f"Query failed with status: {status}")
                print("Error message:", response["QueryExecution"]["Status"]["StateChangeReason"])
            return status
        time.sleep(2)

def get_query_results(query_execution_id):
    """Fetch and display the results of the query."""
    response = athena_client.get_query_results(QueryExecutionId=query_execution_id)
    rows = response["ResultSet"]["Rows"]
    for row in rows:
        print([col.get("VarCharValue", "") for col in row["Data"]])

# 1️⃣ **Create Database**
create_db_query = "CREATE DATABASE IF NOT EXISTS employeee;"
query_id = run_athena_query(create_db_query)
if wait_for_query(query_id) == "SUCCEEDED":
    print("✅ Database 'employeee' created successfully!")

# 2️⃣ **Create Table**
create_table_query = f"""
CREATE EXTERNAL TABLE IF NOT EXISTS employeee.Employees (
    EMPLOYEE_ID INT,
    FIRST_NAME STRING,
    LAST_NAME STRING,
    EMAIL STRING,
    PHONE_NUMBER STRING,
    HIRE_DATE STRING,
    JOB_ID STRING,
    SALARY DOUBLE,
    COMMISSION_PCT STRING,
    MANAGER_ID INT,
    DEPARTMENT_ID INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ',',
    'field.delim' = ','
)
LOCATION '{S3_CSV_PATH}'
TBLPROPERTIES ('has_encrypted_data'='false');
"""

query_id = run_athena_query(create_table_query, database="employeee")
if wait_for_query(query_id) == "SUCCEEDED":
    print("✅ Table 'Employees' created successfully!")

# 3️⃣ **Query Data**
query_data_sql = "SELECT * FROM employeee.Employees LIMIT 10;"
query_id = run_athena_query(query_data_sql, database="employeee")

query_status = wait_for_query(query_id)
if query_status == "SUCCEEDED":
    print("✅ Data queried successfully! Check results in:", S3_OUTPUT)
    get_query_results(query_id)
else:
    print(f"❌ Query failed with status: {query_status}")