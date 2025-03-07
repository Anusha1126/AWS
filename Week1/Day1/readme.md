# AWS Services-S3, IAM, RDS

## Overview
This guide provides a step-by-step approach to configuring AWS services, including **Amazon S3**, **IAM**, and **Amazon RDS**. It covers essential commands, Python scripts, and best practices to set up and manage cloud resources efficiently.

---

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

### **What is IAM?**
AWS IAM is a security service that controls access to AWS resources, enabling secure management of users, roles, and permissions.

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

### **IAM Configuration using AWS CLI**
#### **1. List IAM Users**
```sh
aws iam list-users
```

#### **2. Create an IAM User**
```sh
aws iam create-user --user-name data_admin
```
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture6.png?raw=true) 
### **IAM Configuration using Python (Boto3)**
#### **Creating an IAM User**
```python
import boto3

iam = boto3.client("iam")
user_name = "data_developer"
try:
    response = iam.create_user(UserName=user_name)
    print(f"User {user_name} created successfully!")
except Exception as e:
    print(f"Error: {str(e)}")
```

#### **Attaching a Policy to IAM User**
```python
policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
try:
    iam.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    print(f"Policy {policy_arn} attached to {user_name} successfully!")
except Exception as e:
    print(f"Error: {str(e)}")
```

---
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture7.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture8.png?raw=true) 


## **Amazon RDS - Relational Database Service**

### **What is Amazon RDS?**
Amazon RDS is a fully managed relational database service that simplifies database operations, maintenance, and scaling.

### **Advantages of RDS**
- **Managed Database**: AWS handles backups, scaling, security, and maintenance.
- **High Availability**: Supports Multi-AZ deployments.
- **Automatic Backups**: Enables daily backups and snapshots.
- **Scalability**: Easily scale storage and compute resources.
- **Security**: Supports IAM roles, encryption, and VPC isolation.

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

### **Common Use Cases**

- **Web Applications**: Use RDS as the backend database for high-performance, scalable applications.
- **Data Warehousing**: Store structured data for reporting and analytics with tools like Tableau, Power BI, and AWS Redshift.
- **ETL Pipelines**: Serve as an intermediate storage layer for extracting, transforming, and loading (ETL) data.
- **Multi-Tenant Applications**: Support multiple users with isolated databases for SaaS platforms.
- **Machine Learning Workloads**: Store processed data before feeding it into AWS SageMaker or other ML models.
- **Disaster Recovery**: Enable automated failover with Multi-AZ deployments and snapshots.
- **Hybrid Cloud Integration**: Extend on-premises databases into the cloud for scalability and reliability.

![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture9.png?raw=true) 
![My Image](https://github.com/ray-tech-usa/DET_GEN_AI_2025_B4_WEEK_01/blob/feature-anusha/Week1/Day1/images/Picture10.png?raw=true) 

## **Conclusion**
AWS provides powerful cloud services for storage, security, and database management. Key takeaways:
- **S3**: Scalable object storage for backups, websites, and big data.
- **IAM**: Securely manage access to AWS resources.
- **RDS**: Fully managed relational databases for applications and analytics.

These services together form a strong foundation for modern cloud computing, data engineering, and application development.

