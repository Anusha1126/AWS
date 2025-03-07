# AWS Migration 

## AWS Database Migration Service (DMS)

### Overview
This document provides an overview of the AWS migration process, including essential tools and steps involved in migrating data from a source to a destination database using AWS services. AWS Database Migration Service (DMS) is a managed service that enables seamless database migration to AWS with minimal downtime. This demo covers key components, setup steps, migration types, challenges, and best practices.

## AWS Migration Tools
AWS offers a range of tools to facilitate efficient and secure data migration. The primary tools used in this process include:


![AWS Glue Crawler](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day2/images/2.png?raw=true)

![AWS DMS](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day2/images/3.png?raw=true)

AWS DMS helps migrate databases to AWS quickly and securely while minimizing downtime. It supports homogeneous and heterogeneous database migrations.

### Why Migration is Important
![Importance of Migration](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day2/images/4.png?raw=true)

AWS DMS helps migrate databases to AWS quickly and securely while minimizing downtime. It supports homogeneous and heterogeneous database migrations.

### Why Migration is Important


Migrating to AWS offers several benefits, including improved scalability, cost-efficiency, security, and high availability. It enables organizations to modernize their infrastructure with minimal effort.

## Migration Process
The following steps outline the migration process using AWS tools.

## Prerequisites
Before starting the demo, ensure you have:
- An AWS account with required permissions for DMS.
- Source and target databases (e.g., MySQL, PostgreSQL, or Oracle).
- AWS Schema Conversion Tool (SCT) if migrating between different database engines.

## Key Components
1. **Replication Instance** - The compute instance that manages the migration process.
2. **Source Endpoint** - The existing database that will be migrated.
3. **Target Endpoint** - The destination AWS database (e.g., RDS, S3, Redshift).
4. **Migration Task** - Defines how the migration will proceed (Full Load, CDC, or both).

## Migration Types
| Migration Type | Description |
|-------------------------|-------------|
| **Homogeneous Migration** | Same database engines (e.g., MySQL → MySQL, PostgreSQL → PostgreSQL). |
| **Heterogeneous Migration** | Different database engines (e.g., Oracle → PostgreSQL). |
| **Continuous Data Replication (CDC)** | Ongoing replication for near real-time updates. |

## Common Challenges & Solutions
| Challenge | Solution |
|------------|----------|
| **Slow Migration** | Use parallel load and optimize instance size. |
| **Schema Compatibility Issues** | Use AWS SCT for schema conversion. |
| **Data Loss During Migration** | Enable validation and logging features. |
| **High CDC Lag** | Tune replication instance and increase storage IOPS. |
| **Connectivity Issues** | Use AWS VPN or Direct Connect for stable network. |

## Best Practices
✅ Choose the **right instance size** based on data volume.  
✅ Test migration with **a subset of data** before full migration.  
✅ Optimize schema **before migration** to avoid transformation failures.  
✅ Enable **data validation** to compare source and target databases.  
✅ Use **AWS SCT** for heterogeneous migrations.  
✅ Monitor migration **using CloudWatch and performance logs**.  

---

## Migration Steps

### Step 1: Create a Replication Instance
1. Navigate to the **AWS DMS Console**.
2. Click **Create replication instance**.
3. Choose an instance type (e.g., `dms.r5.large`).
4. Define allocated storage and VPC settings.
5. Click **Create** and wait for the instance to be available.

![Replication Instance](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/1.png?raw=true)

A replication instance is required to facilitate the migration process. It manages the transfer of data from the source to the target database.

### Step 2: Source and Destination Database Creation

![Database Creation](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/5.png?raw=true)

Before migrating data, both source and destination databases must be configured properly. AWS supports various databases, including Amazon RDS, Aurora, and third-party databases like MySQL and PostgreSQL.

### Step 3: Configure Source and Target Endpoints
1. In the **AWS DMS Console**, go to **Endpoints** and click **Create endpoint**.
2. Select **Source Endpoint** and enter the database credentials (hostname, port, username, password).
3. Test the connection before saving.
4. Repeat the process for the **Target Endpoint**.

![Creating Endpoints](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/6.png?raw=true)

Endpoints define the connection settings for both source and target databases. Properly configured endpoints ensure seamless data flow between the two environments.

### Step 4: Create a Migration Task
1. Navigate to **Database Migration Tasks** and click **Create task**.
2. Choose the **Replication Instance** created earlier.
3. Select the **Source and Target Endpoints**.
4. Choose the migration type:
   - **Full Load**: Migrates existing data only.
   - **Change Data Capture (CDC)**: Captures ongoing changes.

---

## Created RDS Instances

```python
import boto3
import time

# AWS Configuration
AWS_REGION = "us-east-1"
DB_INSTANCE_IDENTIFIER = "rds-mysql-source"
DB_NAME = "mydatabase"
DB_USER = "admin"
DB_PASSWORD = "mypassword"
DB_INSTANCE_CLASS = "db.t3.micro"
DB_ENGINE = "mysql"
ALLOCATED_STORAGE = 20  # 20GB Storage
SECURITY_GROUP_ID = "sg-01be7c620263ea11f"

# Create RDS client
rds = boto3.client("rds", region_name=AWS_REGION)

# Create the RDS instance
try:
    response = rds.create_db_instance(
        DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER,
        DBName=DB_NAME,
        Engine=DB_ENGINE,
        MasterUsername=DB_USER,
        MasterUserPassword=DB_PASSWORD,
        DBInstanceClass=DB_INSTANCE_CLASS,
        AllocatedStorage=ALLOCATED_STORAGE,
        PubliclyAccessible=True,  # Set to False for internal use only
        VpcSecurityGroupIds=[SECURITY_GROUP_ID],  # Using the provided Security Group ID
        MultiAZ=False,  # Set explicitly for a single AZ instance
    )
    print(f"RDS instance creation initiated: {response['DBInstance']['DBInstanceIdentifier']}")

    # Wait for the RDS instance to be available
    print("Waiting for the RDS instance to become available...")
    waiter = rds.get_waiter("db_instance_available")
    waiter.wait(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
    print(f"RDS instance '{DB_INSTANCE_IDENTIFIER}' is now active.")

    # Get the endpoint of the DB instance
    db_instance = rds.describe_db_instances(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
    endpoint = db_instance["DBInstances"][0]["Endpoint"]["Address"]
    print(f"The database instance is accessible at: {endpoint}")

except Exception as e:
    print(f"Failed to create RDS instance. Error: {e}")

```    


## Data Insertion to Table

```python
import mysql.connector

# Database Configuration
rds_endpoint = "rds-mysql-source.c2xmycgk2zok.us-east-1.rds.amazonaws.com"  # Replace with actual RDS endpoint
db_name = "mydatabase"
db_user = "admin"
db_password = "mypassword"  # Replace with actual password

# Connect to MySQL RDS
try:
    conn = mysql.connector.connect(
        host=rds_endpoint, user=db_user, password=db_password, database=db_name
    )
    cursor = conn.cursor()
    print("Database connection established.")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

# Create Table
create_table_query = """
    CREATE TABLE IF NOT EXISTS ecommerce_sales (
        order_id INT PRIMARY KEY,
        customer_name VARCHAR(100),
        product_name VARCHAR(255),
        quantity INT,
        unit_price DECIMAL(10,2),
        total_price DECIMAL(10,2),
        order_date DATE,
        payment_method VARCHAR(50)
    )
"""
cursor.execute(create_table_query)
print("Table 'ecommerce_sales' created or already exists.")

# Insert Realistic Sales Data
insert_query = """
    INSERT INTO ecommerce_sales (order_id, customer_name, product_name, quantity, unit_price, total_price, order_date, payment_method) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    quantity = VALUES(quantity),
    unit_price = VALUES(unit_price),
    total_price = VALUES(total_price),
    order_date = VALUES(order_date),
    payment_method = VALUES(payment_method)
"""

real_sales_data = [
    (101, "John Doe", "Apple iPhone 14", 1, 799.99, 799.99, '2024-02-01', "Credit Card"),
    (102, "Jane Smith", "Samsung Galaxy S23", 1, 699.99, 699.99, '2024-02-02', "PayPal"),
    (103, "Alice Johnson", "Sony WH-1000XM5 Headphones", 2, 299.99, 599.98, '2024-02-03', "Debit Card"),
    (104, "Michael Brown", "MacBook Air M2", 1, 1199.99, 1199.99, '2024-02-04', "Credit Card"),
    (105, "Emma Wilson", "Dell XPS 13 Laptop", 1, 999.99, 999.99, '2024-02-05', "Amazon Pay"),
    (106, "Chris Davis", "Logitech MX Master 3 Mouse", 3, 99.99, 299.97, '2024-02-06', "Google Pay"),
    (107, "Sarah Miller", "Bose SoundLink Bluetooth Speaker", 1, 199.99, 199.99, '2024-02-07', "PayPal"),
    (108, "David Johnson", "GoPro HERO10 Black", 2, 399.99, 799.98, '2024-02-08', "Credit Card"),
    (109, "Sophia White", "Nike Air Zoom Pegasus 39", 2, 129.99, 259.98, '2024-02-09', "Apple Pay"),
    (110, "Daniel Martinez", "Kindle Paperwhite", 1, 139.99, 139.99, '2024-02-10', "Amazon Pay"),
]

cursor.executemany(insert_query, real_sales_data)
conn.commit()
print("Realistic e-commerce sales data inserted successfully.")


# Query Data
cursor.execute("SELECT * FROM ecommerce_sales;")
results = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]

# Print results in table format manually
print("\nE-commerce Sales Table Data:")
print(" | ".join(column_names))
print("-" * 80)
for row in results:
    print(" | ".join(str(value) for value in row))

# Close connection
cursor.close()
conn.close()

print("Database operations completed successfully.")


```

![Creating Endpoints](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/7.png?raw=true)

## Instance Creation

``` python
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

```    

![Creating Endpoints](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/9.png?raw=true)

## End points creation
## Source end point

``` python
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
```     

## Target endpoint

``` python
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

``` 

![Creating Endpoints](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/10.png?raw=true)

## Migration task

``` python
import boto3
import json
import time

# Initialize AWS DMS client
dms_client = boto3.client('dms')

# Define DMS Task Configuration
replication_task_id = "mysql-postgre-migration"
source_endpoint_arn = "arn:aws:dms:us-east-1:970547378939:endpoint:RUI3AT4FYVB4VGCYQARFWVSOQE"
target_endpoint_arn = "arn:aws:dms:us-east-1:970547378939:endpoint:WCQKVFOVPBASLDG5ZNFIQF352I"
replication_instance_arn = "arn:aws:dms:us-east-1:970547378939:rep:EWPF27MXSFBCLP7CCBWMGFEL5U"

# Define Table Mappings (Proper JSON Format)
table_mappings_dict = {
    "rules": [
        {
            "rule-type": "selection",
            "rule-id": "1",
            "rule-name": "IncludeAllTables",
            "rule-action": "include",
            "object-locator": {
                "schema-name": "mydatabase",
                "table-name": "%"
            }
        }
    ]
}

# Convert to JSON String
table_mappings = json.dumps(table_mappings_dict)

try:
    # Create a DMS Replication Task
    response = dms_client.create_replication_task(
        ReplicationTaskIdentifier=replication_task_id,
        SourceEndpointArn=source_endpoint_arn,
        TargetEndpointArn=target_endpoint_arn,
        MigrationType="full-load",  # Moves all existing data
        TableMappings=table_mappings,
        ReplicationInstanceArn=replication_instance_arn
    )

    # Get Task ARN
    task_arn = response["ReplicationTask"]["ReplicationTaskArn"]
    print(f"DMS Replication Task '{replication_task_id}' has been created successfully.")
    print(f"Task ARN: {task_arn}")

    # Wait for the task to reach 'ready' state before starting
    while True:
        task_status = dms_client.describe_replication_tasks(
            Filters=[{"Name": "replication-task-arn", "Values": [task_arn]}]
        )["ReplicationTasks"][0]["Status"]

        print(f"Waiting for task to be ready. Current status: {task_status}")

        if task_status in ["ready"]:
            break  # Task is ready to start

        elif task_status in ["creating"]:
            time.sleep(10)  # Wait and check again

        else:
            raise Exception(f"Task cannot be started. Current Status: {task_status}")

    # Start the Replication Task
    dms_client.start_replication_task(
        ReplicationTaskArn=task_arn,
        StartReplicationTaskType="start-replication"
    )

    print(f"Replication Task '{replication_task_id}' has started successfully.")

except Exception as e:
    print(f"Error: {str(e)}")

``` 
![Creating Endpoints](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/8.png?raw=true)    

![Creating Endpoints](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/12.png?raw=true)    


CLI:

## Create RDS Instance

## Source RDS
```bash
aws rds create-db-instance ^
    --db-instance-identifier source-db-instance ^
    --db-instance-class db.t3.micro ^
    --engine mysql ^
    --allocated-storage 20 ^
    --master-username admin ^
    --master-user-password Admin@1234 ^
    --backup-retention-period 7 ^
    --publicly-accessible ^
    --vpc-security-group-ids sg-xxxxxxxx ^
    --region us-east-1
```
![Creating Endpoints](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/14.png?raw=true)    

## Target RDS
```
aws rds create-db-instance ^
    --db-instance-identifier target-db-instance ^
    --db-instance-class db.t3.micro ^
    --engine mysql ^
    --allocated-storage 20 ^
    --master-username admin ^
    --master-user-password Admin@1234 ^
    --backup-retention-period 7 ^
    --publicly-accessible ^
    --vpc-security-group-ids sg-xxxxxxxx ^
    --region us-east-1
```
## Create DMS Instance
```bash
aws dms create-replication-instance ^
    --replication-instance-identifier dms-instance ^
    --replication-instance-class dms.t3.medium ^
    --allocated-storage 100 ^
    --engine-version 3.5.3 ^
    --publicly-accessible ^
    --region us-east-1
```
## Create Endpoints

## Source
```bash
aws dms create-endpoint ^
    --endpoint-identifier source-endpoint ^
    --endpoint-type source ^
    --engine-name mysql ^
    --username admin ^
    --password 993132Ray ^
    --server-name source-db-instance.c72km8ss6vll.us-east-1.rds.amazonaws.com ^
    --port 3306 ^
    --database-name sourcedb
```    

## Target    
```bash
aws dms create-endpoint ^
    --endpoint-identifier target-endpoint ^
    --endpoint-type target ^
    --engine-name mysql ^
    --username admin ^
    --password 993132Ray ^
    --server-name target-db-instance.c72km8ss6vll.us-east-1.rds.amazonaws.com ^
    --port 3306 ^
    --database-name targetdb
```    

## Created table before replication task
![Creating Endpoints](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week2/Day3/images/13.png?raw=true)    

## Create replication task
```bash
aws dms createreplicationtask ^ --replication-task-identifier dms-task ^ --replication-instance-arn arn:aws:dms:us-east-1:879381286027:rep:KZDXOCBFDNEJJOBRWF3N7E7EZE ^ --source-endpoint-arn arn:aws:dms:us-east-1:879381286027:endpoint:3LOBQNN6PZARJPABXMNIKACSSI ^ --target-endpoint-arn arn:aws:dms:us-east-1:879381286027:endpoint:6HNOYMZFLFB33HPMJYHA2I2OWY ^ --migration-type full-load ^ --table-mappings "C:\Users\repal\OneDrive\Desktop\DataEngineeringPractice\DET_GEN_AI_2025_B4_WEEK_01-1\Week2\Day3\src\table_mappings.json"
```

Use the **AWS DMS Console** to monitor migration status.
- Check **CloudWatch logs** for performance and error handling.
- Validate data integrity by comparing row counts in source and target databases.

## Additional Considerations
- **Testing & Validation**: Before fully migrating, it is crucial to test data integrity and validate the migrated datasets.
- **Monitoring & Optimization**: Use AWS CloudWatch and AWS DMS monitoring tools to track migration progress and optimize performance.
- **Security & Compliance**: Implement best practices for securing sensitive data and ensuring compliance with industry standards.

## Conclusion
AWS provides robust and scalable tools to facilitate seamless database migration. By following the outlined steps, organizations can efficiently migrate data while ensuring minimal downtime and high data integrity. By following best practices, testing before full migration, and monitoring performance, you can ensure a successful and smooth transition to AWS.



