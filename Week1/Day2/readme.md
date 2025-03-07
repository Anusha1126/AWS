# AWS IAM, Redshift, RDS, and S3 - Overview & Usage Guide

## **Overview**
This document provides a comprehensive guide on implementing and integrating **AWS IAM, Amazon Redshift, Amazon RDS, and Amazon S3** in an AWS cloud environment. Each service plays a crucial role in cloud-based data security, storage, processing, and analytics, supporting a variety of business and technical use cases.

## **Prerequisites**
Before working with these AWS services, ensure the following prerequisites are met:
- **AWS Account**: An active AWS account with necessary permissions.
- **IAM Roles & Permissions**: IAM roles configured with appropriate access for Redshift, RDS, and S3.
- **VPC & Subnets**: A properly configured Virtual Private Cloud (VPC) with security groups.
- **SQL & Database Knowledge**: Familiarity with PostgreSQL (for Redshift), MySQL/PostgreSQL (for RDS), and object storage concepts (for S3).
- **AWS CLI & Boto3 Installed**: For automation via scripting.

## **Amazon S3 - Simple Storage Service**

### **What is Amazon S3?**
Amazon S3 is an object storage service that enables storing and retrieving any amount of data from anywhere. It is designed for scalability, durability, and security.

### **Key Concepts**
- **Bucket**: A unique container to store objects.
- **Object**: Data stored in a bucket (e.g., CSV files, images, videos, text files, etc.).

### **Advantages of Amazon S3**
- **Scalability**: Supports unlimited storage for growing workloads.
- **High Durability**: 99.999999999% (11 nines) durability.
- **Security**: Encryption, access control, and IAM integration.
- **Cost-Effective**: Pay-as-you-go pricing with multiple storage classes.
- **Accessibility**: Access via AWS Console, API, CLI, or SDK.

### **Use Cases**
- **Data Backup and Archiving**: Store long-term backups and automate database backups.
- **Big Data and Analytics**: Serve as a data lake for ML analytics tools like AWS Glue, Athena, and Redshift.
- **Static Website Hosting**: Serve HTML, CSS, and JavaScript directly from an S3 bucket.
- **Media Storage and Streaming**: Store and stream images, videos, and audio files.
- **Disaster Recovery**: Multi-region replication and versioning for data protection.

### **S3 Configuration using AWS CLI**
#### **1. Configure AWS CLI**
```sh
aws configure
```
Provide:
- **Access Key**
- **Secret Key**
- **Region**
- **Output Format**

#### **2. Verify Configuration**
```sh
aws configure list
```

#### **3. Create an S3 Bucket**
```sh
aws s3 mb s3://my-new-bucket
```
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture1.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture2.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture3.png?raw=true) 
### **S3 Configuration using Python (Boto3)**
#### **Creating an S3 Bucket**

```python
import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region="us-east-1"):
    s3_client = boto3.client("s3", region_name=region)
    try:
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
```

#### **Uploading a File to S3**
```python
def upload_object(bucket_name, object_name, file_path):
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded as '{object_name}' in bucket '{bucket_name}'.")
    except ClientError as e:
        print(f"Error: {e}")
```

---

![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture4.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture5.png?raw=true) 

## **AWS IAM - Identity and Access Management**

## **Introduction**
AWS Identity and Access Management (IAM) is a security service that helps users control access to AWS resources. It enables the creation of users, groups, and roles with customized permissions to ensure secure and managed interactions with AWS services.

## **Core Components**
1. **Users** – Individual accounts representing people or applications.
2. **Groups** – Collections of users sharing common permissions.
3. **Roles** – Temporary access permissions assigned to users, applications, or services.
4. **Policies** – JSON-based documents defining access permissions.
5. **Multi-Factor Authentication (MFA)** – Adds an extra security layer.
6. **Access Keys & Secret Keys** – Used for programmatic access to AWS resources.
7. **Cross-Region Replication** – Allows IAM policy replication across multiple AWS regions.

## **Types of IAM Policies**
1. **Managed Policies** – AWS-created reusable permission sets.
2. **Inline Policies** – Custom policies attached directly to IAM entities.
3. **Permissions Boundaries** – Restrict maximum permissions for IAM roles or users.
4. **Service Control Policies (SCPs)** – Policies applied at the AWS Organizations level.
5. **Resource-Based Policies** – Policies attached directly to AWS resources like S3 buckets.

## **How It Can Be Used**
- **Granular Access Control** – Assign least-privilege permissions to users and services.
- **Service Authentication** – Secure access to AWS services like Redshift, RDS, and S3.
- **Federated Access** – Integrate with external identity providers.
- **Auditing & Compliance** – Track access using AWS CloudTrail.

### **Advantages of IAM**
- **Access Control**: Restrict access to AWS resources.
- **Secure API Access**: Manage API keys and tokens securely.
- **Multi-Factor Authentication (MFA)**: Adds an extra security layer.
- **Role-Based Access Control (RBAC)**: Assign permissions based on user roles.
- **Audit and Compliance**: Track user activities using AWS CloudTrail.

### **Common Use Cases**
- **User and Role Management**: Create and manage IAM users, groups, and roles to control access.
- **Secure API Authentication**: Use IAM roles to grant temporary access to AWS services via API requests.
- **Least Privilege Access**: Implement the principle of least privilege to ensure users have the minimum required permissions.
- **Multi-Account Access Management**: Use IAM Identity Center (SSO) for managing access across multiple AWS accounts.
- **Federated Access**: Integrate IAM with external identity providers (e.g., Okta, Active Directory) for single sign-on (SSO).
- **Monitoring and Compliance**: Use IAM policies and CloudTrail logs to audit access and meet compliance requirements.
- **Service-to-Service Communication**: Assign IAM roles to EC2 instances, Lambda functions, or containers to grant controlled access to AWS services.

---
# IAM Configuration using AWS CLI

## 1. Configure AWS CLI
Run the following command to configure AWS CLI with your credentials:

```sh
aws configure
```

To verify the configured settings, use:

```sh
aws configure list
```

![AWS Configure](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day3/images/1.png?raw=true)

---

## 2. Create an IAM User
Create an IAM user named `data_admin` using the following command:

```sh
aws iam create-user --user-name data_admin
```

![Create IAM User](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day3/images/2.png?raw=true)

---

## 3. Create and Attach an Inline Policy
Create a JSON file (`s3_read_only_policy.json`) to define an inline policy with read-only access to S3:

```sh
cat <<EOT > s3_read_only_policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": "*"
        }
    ]
}
EOT
```

Attach the inline policy to the IAM user:

```sh
aws iam put-user-policy --user-name data_admin --policy-name S3ReadOnlyPolicy --policy-document file://s3_read_only_policy.json
```

Verify the policy:

```sh
aws iam list-user-policies --user-name data_admin
```

![List User Policies](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day3/images/3.png?raw=true)
![Policy Verification](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day3/images/4.png?raw=true)

---

## 4. Attach a Standard AWS Managed Policy
Attach the `AmazonS3ReadOnlyAccess` managed policy to the IAM user:

```sh
aws iam attach-user-policy --user-name data_admin --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

![Attach Managed Policy](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day3/images/5.png?raw=true)
![Policy Confirmation](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day3/images/6.png?raw=true)

---

## 5. IAM Configuration Using Python (Boto3)
The following Python script automates the IAM user and policy setup using `boto3`:

```python
import boto3
import json

# AWS Configuration
AWS_REGION = "us-east-1"
USER_NAME = "data_admin_boto3"
INLINE_POLICY_NAME = "S3WriteOnlyPolicy"
MANAGED_POLICY_ARN = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"

# Initialize AWS clients
iam_client = boto3.client("iam", region_name=AWS_REGION)

# Inline policy document
inline_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": "*"
        }
    ]
}

# Create IAM user
def create_iam_user(user_name):
    try:
        response = iam_client.create_user(UserName=user_name)
        print(f"User '{user_name}' created successfully.")
        return response
    except iam_client.exceptions.EntityAlreadyExistsException:
        print(f"User '{user_name}' already exists.")
        return None

# Attach inline policy to IAM user
def attach_inline_policy(user_name, policy_name, policy_document):
    try:
        iam_client.put_user_policy(
            UserName=user_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        print(f"Inline policy '{policy_name}' attached to user '{user_name}' successfully.")
    except Exception as e:
        print(f"Error attaching inline policy: {e}")

# Attach managed policy to IAM user
def attach_managed_policy(user_name, policy_arn):
    try:
        iam_client.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
        print(f"Managed policy '{policy_arn}' attached to user '{user_name}' successfully.")
    except Exception as e:
        print(f"Error attaching managed policy: {e}")

# Main function
def main():
    create_iam_user(USER_NAME)
    attach_inline_policy(USER_NAME, INLINE_POLICY_NAME, inline_policy_document)
    attach_managed_policy(USER_NAME, MANAGED_POLICY_ARN)

if __name__ == "__main__":
    main()
```

![Boto3 Execution](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day3/images/7.png?raw=true)
![Final Output](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day3/images/8.png?raw=true)

## **Amazon RDS - Relational Database Service**

### **What is Amazon RDS?**
Amazon RDS is a fully managed relational database service that simplifies database operations, maintenance, and scaling.

### **Advantages of RDS**
- **Managed Database**: AWS handles backups, scaling, security, and maintenance.
- **High Availability**: Supports Multi-AZ deployments.
- **Automatic Backups**: Enables daily backups and snapshots.
- **Scalability**: Easily scale storage and compute resources.
- **Security**: Supports IAM roles, encryption, and VPC isolation.

  ### **Common Use Cases**

- **Web Applications**: Use RDS as the backend database for high-performance, scalable applications.
- **Data Warehousing**: Store structured data for reporting and analytics with tools like Tableau, Power BI, and AWS Redshift.
- **ETL Pipelines**: Serve as an intermediate storage layer for extracting, transforming, and loading (ETL) data.
- **Multi-Tenant Applications**: Support multiple users with isolated databases for SaaS platforms.
- **Machine Learning Workloads**: Store processed data before feeding it into AWS SageMaker or other ML models.
- **Disaster Recovery**: Enable automated failover with Multi-AZ deployments and snapshots.
- **Hybrid Cloud Integration**: Extend on-premises databases into the cloud for scalability and reliability.


### **RDS Configuration using AWS CLI**
#### **1. Create an RDS Instance**
```sh
aws rds create-db-instance \
    --db-instance-identifier mydbinstance \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --allocated-storage 20 \
    --master-username admin \
    --master-user-password SecurePass123 \
    --backup-retention-period 7 \
    --no-multi-az \
    --publicly-accessible
```

### **Connecting to RDS using Python**
```python
import mysql.connector

db_host = "your-rds-endpoint.amazonaws.com"
db_user = "admin"
db_password = "yourpassword"
db_name = "yourdatabase"

conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()
cursor.execute("SELECT VERSION();")
version = cursor.fetchone()
print(f"Connected to MySQL version: {version}")
cursor.close()
conn.close()
```

---
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture9.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture10.png?raw=true) 

**RDS Data Insertion**

```python
import boto3
import mysql.connector
import time

# AWS RDS configuration
rds = boto3.client("rds")

db_instance_id = "mydbinstance"
db_instance_class = "db.t3.micro"
engine = "mysql"
master_username = "admin"
master_password = "SecurePass123"
allocated_storage = 20

# Function to check if the RDS instance exists
def check_rds_instance_exists(instance_id):
    try:
        response = rds.describe_db_instances(DBInstanceIdentifier=instance_id)
        return True
    except rds.exceptions.DBInstanceNotFoundFault:
        return False

# 1️⃣ Create an RDS MySQL instance (if it does not exist)
if not check_rds_instance_exists(db_instance_id):
    try:
        response = rds.create_db_instance(
            DBInstanceIdentifier=db_instance_id,
            AllocatedStorage=allocated_storage,
            DBInstanceClass=db_instance_class,
            Engine=engine,
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            PubliclyAccessible=True,
            BackupRetentionPeriod=7,
            MultiAZ=False,
        )
        print(f"RDS instance {db_instance_id} is being created...")

        # Wait for the instance to become available
        while True:
            response = rds.describe_db_instances(DBInstanceIdentifier=db_instance_id)
            status = response["DBInstances"][0]["DBInstanceStatus"]
            print(f"Current RDS Status: {status}")
            if status == "available":
                break
            time.sleep(30)  # Wait before checking again
    except Exception as e:
        print(f"Error creating RDS instance: {str(e)}")
else:
    print(f"RDS instance '{db_instance_id}' already exists.")

# 2️⃣ Retrieve the RDS Endpoint
try:
    response = rds.describe_db_instances(DBInstanceIdentifier=db_instance_id)
    db_endpoint = response["DBInstances"][0]["Endpoint"]["Address"]
    print(f"RDS Endpoint: {db_endpoint}")
except Exception as e:
    print(f"Error fetching RDS instance endpoint: {str(e)}")
    exit()

# 3️⃣ Connect to the MySQL Database
for attempt in range(5):
    try:
        conn = mysql.connector.connect(
            host=db_endpoint,
            user=master_username,
            password=master_password
        )
        cursor = conn.cursor()
        print("Connected to the RDS MySQL database successfully!")
        break
    except mysql.connector.Error as err:
        print(f"Error connecting to RDS database: {err}")
        time.sleep(10)
else:
    print("Failed to connect to RDS database after multiple attempts.")
    exit()

# 4️⃣ Create the Database if it does not exist
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS testdb;")
    print("Database 'testdb' created successfully!")
except Exception as e:
    print(f"Error creating database: {str(e)}")

# 5️⃣ Connect to the 'testdb' Database
try:
    conn.database = 'testdb'
    print("Switched to 'testdb' database successfully!")
except mysql.connector.Error as err:
    print(f"Error switching to 'testdb' database: {err}")
    exit()

# 6️⃣ Create a Table in the Database
try:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        department VARCHAR(50),
        salary DECIMAL(10,2)
    );
    """
    cursor.execute(create_table_query)
    print("Table 'employees' created successfully!")
except Exception as e:
    print(f"Error creating table: {str(e)}")

# 7️⃣ Insert Data into the Table
try:
    insert_query = "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)"
    employees = [
        ("Alice Johnson", "IT", 75000.00),
        ("Bob Smith", "Finance", 80000.00),
        ("Charlie Brown", "HR", 70000.00)
    ]

    cursor.executemany(insert_query, employees)
    conn.commit()
    print(f"{cursor.rowcount} rows inserted into 'employees' table successfully!")
except Exception as e:
    print(f"Error inserting data: {str(e)}")

# 8️⃣ Retrieve and Display the Data
try:
    cursor.execute("SELECT * FROM employees;")
    rows = cursor.fetchall()
    print("\nData in 'employees' table:")
    for row in rows:
        print(row)
except Exception as e:
    print(f"Error fetching data: {str(e)}")

# Close the Connection
cursor.close()
conn.close()
print("Database connection closed.")
```

---

# **Amazon Redshift**

## **Introduction**

Amazon **Redshift** is a fully managed, cloud-based **data warehouse** service provided by AWS. It is designed for **high-performance analytics** on structured and semi-structured data. Redshift enables organizations to analyze **petabyte-scale** data using **SQL-based queries** while leveraging its **columnar storage** and **massively parallel processing (MPP)** architecture.


## **Core Components**
1. **Clusters** – The fundamental Redshift resource that hosts the data and runs queries. A **Redshift Cluster** is a collection of resources used to store and analyze large datasets. It consists of the following main components:
2. **Nodes** – Comprises Compute Nodes and a Leader Node.
    - **Leader Node**: The central management component that **parses and optimizes queries**, distributes workloads to             compute nodes, and collects & returns results to the user.
    - **Compute Nodes**: These nodes store data, execute queries, and perform parallel processing. They execute tasks               assigned by the leader node and return processed data.
3. **Columnar Storage** – Stores data in columns rather than rows to optimize query performance.
4. **Workload Management (WLM)** – Allocates cluster resources to different query queues.
5. **Redshift Spectrum** – Enables querying of structured and semi-structured data directly from Amazon S3.
6. **Data Distribution Styles** – **Even, Key, and All** for optimized query execution.
7. **Compression & Encoding** – Uses automatic compression to improve storage efficiency.
8. **Cross-Region Replication** – Enables replication of Redshift snapshots to another AWS region.

### **Why Use Redshift?**
1. **Scalability** – Redshift can handle **terabytes to petabytes** of data, scaling seamlessly as demand grows.
2. **Performance Optimization** – Uses **columnar storage** and **compression** to optimize queries and reduce I/O operations.
3. **Cost-Effective** – Offers **pay-as-you-go** pricing with reserved instance options for cost savings.
4. **Easy Integration** – Works with **AWS ecosystem services** like S3, Glue, QuickSight, and Data Lake solutions.
5. **Massively Parallel Processing (MPP)** – Distributes queries across multiple nodes for **faster query execution**.
6. **Security & Compliance** – Provides **VPC isolation, encryption (AES-256), and IAM-based access control** for data security.
7. **Concurrency Scaling** – Allows multiple users to run complex queries **without performance degradation**.
8. **Automatic Backups & Snapshots** – Ensures **high availability** and disaster recovery support.

### **Cluster Types**
- **Single Node Cluster**: The leader node also functions as a compute node. Suitable for small-scale workloads.
- **Multi-Node Cluster**: Consists of **one leader node** and **multiple compute nodes**. Used for **large-scale data processing** requiring high performance and scalability.

## **Use Cases of Amazon Redshift**

1. **Enterprise Data Warehousing**  
   - Consolidates **data from multiple sources** (ERP, CRM, logs, IoT) into a centralized warehouse.
   - Supports **business intelligence (BI)** and reporting needs for large enterprises.

2. **Big Data Analytics**  
   - Processes and analyzes **structured, semi-structured, and unstructured** data.
   - Used for **real-time analytics, ad-hoc queries, and predictive analytics**.

3. **ETL & Data Lake Integration**  
   - Works seamlessly with **AWS Glue, S3, and Lake Formation** for ETL pipelines.
   - Stores **historical and real-time** datasets for analytics.

4. **Business Intelligence & Reporting**  
   - Integrated with **BI tools** such as **Amazon QuickSight, Tableau, Power BI, and Looker**.
   - Helps generate **dashboards and data-driven insights**.

5. **Financial Analytics & Fraud Detection**  
   - Processes **large-scale financial transactions** for insights and compliance reporting.
   - Detects **fraudulent transactions using ML and SQL-based analysis**.

6. **Marketing & Customer Analytics**  
   - Analyzes **customer behavior, churn prediction, and campaign effectiveness**.
   - Personalizes **customer recommendations** using Redshift ML.

7. **Healthcare & Genomic Data Analysis**  
   - Stores and analyzes **electronic health records (EHRs)**.
   - Supports **genomic sequencing and clinical trial analytics**.

8. **IoT Data Processing & Log Analytics**  
   - Stores and processes **sensor and device data** from IoT applications.
   - Analyzes **server logs, application logs, and security events**.

9. **E-commerce & Retail Analytics**  
   - Analyzes **customer purchase trends, inventory management, and supply chain optimization**.
   - Provides **real-time pricing, demand forecasting, and stock recommendations**.

10. **Gaming & Clickstream Analysis**  
   - Tracks **in-game user activity, session analysis, and revenue insights**.
   - Analyzes **clickstream data to improve user engagement**.

## **Python Code for Cluster Creation**

The following Python script demonstrates how to create an AWS Redshift cluster using **boto3**:

```python
import boto3

# AWS Configuration
AWS_REGION = "us-east-1"  # Modify as needed
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
```

![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/Cluster_Creation.png)


## **Checking Cluster Status**

Use the following Python script to check the cluster status and retrieve its endpoint once available:

```python
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
```
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/retrieve_cluster.png)
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/Query_output.png)

## **Creating the table**

```python
import psycopg2

# Replace with your Redshift cluster details
host = "my-redshift-cluster.csgshqmtgnij.us-east-1.redshift.amazonaws.com"
port = "5439"
dbname = "dev"
user = "admin"
password = "YourSecurePassword123"

try:
    print("🚀 Trying to connect to AWS Redshift...")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("✅ Connected to AWS Redshift successfully!")

    cursor = conn.cursor()

    # Create a table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INT,
        name VARCHAR(100),
        department VARCHAR(50),
        salary DECIMAL(10, 2)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("✅ Table 'employees' created successfully!")

    # Insert data into the table
    insert_data_query = """
    INSERT INTO employees (id, name, department, salary) VALUES
    (1, 'Alice Johnson', 'IT', 75000.00),
    (2, 'Bob Smith', 'Finance', 80000.00),
    (3, 'Charlie Brown', 'HR', 70000.00);
    """
    cursor.execute(insert_data_query)
    conn.commit()
    print("✅ Data inserted into 'employees' table successfully!")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection Error: {e}")
    
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/create_table.png)

## **Connecting to Redshift Cluster**

Use **psycopg2** to connect to the Redshift cluster and execute queries:

```python
import psycopg2

# Replace with your Redshift cluster details
host = "my-redshift-cluster.csgshqmtgnij.us-east-1.redshift.amazonaws.com"
port = "5439"
dbname = "dev"
user = "admin"
password = "YourSecurePassword123"

try:
    print("🚀 Trying to connect to AWS Redshift...")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("✅ Connected to AWS Redshift successfully!")

    cursor = conn.cursor()
    cursor.execute("SELECT current_user, current_database();")
    print("Query Result:", cursor.fetchall())

    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Connection Error:", e)
```
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/create_table.png)

![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/result1.png)
import psycopg2


**View the data in cluster**
```python
# Replace with your Redshift cluster details
host = "my-redshift-cluster.csgshqmtgnij.us-east-1.redshift.amazonaws.com"
port = "5439"
dbname = "dev"
user = "admin"
password = "YourSecurePassword123"

try:
    print("🚀 Trying to connect to AWS Redshift...")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("✅ Connected to AWS Redshift successfully!")

    cursor = conn.cursor()

    # List all tables in the public schema
    list_tables_query = """
    SELECT tablename
    FROM pg_catalog.pg_tables
    WHERE schemaname = 'public';
    """
    cursor.execute(list_tables_query)
    tables = cursor.fetchall()
    print("\nTables in 'public' schema:")
    for table in tables:
        print(table)

    # View the structure of the employees table
    describe_table_query = """
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'employees';
    """
    cursor.execute(describe_table_query)
    columns = cursor.fetchall()
    print("\nStructure of 'employees' table:")
    for column in columns:
        print(column)

    # View the data in the employees table
    select_query = "SELECT * FROM employees;"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    print("\nData in 'employees' table:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection Error: {e}")
```
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/result_python.png)

## **Creating and Deleting Cluster using AWS CLI (Git Bash)**

### **Create Cluster**

```bash
aws redshift create-cluster \
    --cluster-identifier my-redshift-cluster-2 \
    --node-type dc2.large \
    --master-username adminuser \
    --master-user-password MySecurePass123 \
    --cluster-type single-node \
    --db-name mydatabase \
    --port 5439 \
    --publicly-accessible \
    --iam-roles arn:aws:iam::970547378939:role/RedshiftRole
```

![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/cluster_creation_thru_bash.png)
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day2/Images/Query_output.png)

### **Delete Cluster**

```bash
aws redshift delete-cluster \
    --cluster-identifier my-redshift-cluster-2 \
    --skip-final-cluster-snapshot
```

## **Troubleshooting**
- Ensure inbound rules for **port 5439** allow external access by selecting **Custom TCP** in security group settings.

---

## **Conclusion**
AWS provides powerful cloud services for storage, security, and database management. Key takeaways:
- **S3**: Scalable object storage for backups, websites, and big data.
- **IAM**: Securely manage access to AWS resources.
- **RDS**: Fully managed relational databases for applications and analytics.
- **Redshift**: A fully managed data warehouse solution optimized for analytical queries and big data processing. It enables fast querying and scalable storage, making it ideal for business intelligence and large-scale data analysis.

These services together form a strong foundation for modern cloud computing, data engineering, and application development.