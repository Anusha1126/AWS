import boto3

# AWS Configuration
region = "us-east-1" 
database_name = "my_employees_data_catalog_db_python"
table_name = "people_data2"
s3_path = "s3://my-employees/employees.csv"
iam_role_arn = "arn:aws:iam::970547378939:role/gluerole"  

# Initialize boto3 clients
glue_client = boto3.client("glue", region_name=region)

# ✅ Step 1: Create Glue Database
def create_database():
    try:
        glue_client.create_database(DatabaseInput={"Name": database_name})
        print(f"✅ Database '{database_name}' created successfully!")
    except glue_client.exceptions.AlreadyExistsException:
        print(f"ℹ️ Database '{database_name}' already exists.")

# ✅ Step 2: Create Glue Table
def create_table():
    try:
        glue_client.create_table(
            DatabaseName=database_name,
            TableInput={
                "Name": table_name,
                "StorageDescriptor": {
                    "Columns": [
                                {"Name": "EMPLOYEE_ID", "Type": "int"},
                                {"Name": "FIRST_NAME", "Type": "string"},
                                {"Name": "LAST_NAME", "Type": "string"},
                                {"Name": "EMAIL", "Type": "string"},
                                {"Name": "PHONE_NUMBER", "Type": "string"},
                                {"Name": "HIRE_DATE", "Type": "string"},
                                {"Name": "JOB_ID", "Type": "string"},
                                {"Name": "SALARY", "Type": "double"},
                                {"Name": "COMMISSION_PCT", "Type": "string"},
                                {"Name": "MANAGER_ID", "Type": "int"},
                                {"Name": "DEPARTMENT_ID", "Type": "int"}
                            ],
                    "Location": s3_path,
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
                        "Parameters": {"field.delim": ","}
                    }
                }
            }
        )
        print(f"✅ Table '{table_name}' created successfully!")
    except glue_client.exceptions.AlreadyExistsException:
        print(f"ℹ️ Table '{table_name}' already exists.")

# ✅ Step 3: Create & Run Glue Crawler
def create_crawler():
    try:
        glue_client.create_crawler(
            Name="employees_crawler",
            Role=iam_role_arn,
            DatabaseName=database_name,
            Targets={"S3Targets": [{"Path": s3_path}]},
            TablePrefix="people_"
        )
        print("✅ Glue Crawler created successfully!")
    except glue_client.exceptions.AlreadyExistsException:
        print("ℹ️ Glue Crawler  already exists.")

# ✅ Step 4: Start Glue Crawler
def run_crawler():
    glue_client.start_crawler(Name="employees_crawler")
    print("🚀 Glue Crawler started...")

# Run all steps
create_database()
create_table()
create_crawler()
run_crawler()
