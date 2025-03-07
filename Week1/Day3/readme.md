# Amazon QuickSight and Glue Data Catalog

## Overview
This repository contains resources and documentation for an **Amazon QuickSight** and **Glue Data Catalog** demo, covering key components, backend architecture, common challenges, and best practices.

---
## Quicksight
Amazon QuickSight is a cloud-powered business intelligence (BI) service that allows users to create interactive dashboards, analyze data, and gain insights from various AWS data sources.
## Components

### Datasets
- Connects to various sources (**S3, Redshift, RDS, Athena, DynamoDB**).
- Supports **filtering, joining, and aggregating** data before analysis.

### Analysis
- Interactive interface to create reports and visualizations.
- Apply **filters, calculated fields,** and **forecasting models**.

### Visualizations
- Supports multiple chart types (**bar, pie, line, heatmaps, maps**).
- **AutoGraph** recommends the best visualization based on data type.

### Dashboards
- Create interactive and **real-time dashboards**.
- Share reports with stakeholders using **role-based access control**.

### Themes
- Customize dashboards using built-in or **custom themes**.

---

## Backend Framework

### Data Integration
- Native integration with AWS services: **S3, Redshift, RDS, DynamoDB, Athena**.
- Connects to **third-party databases** via JDBC/ODBC.

### SPICE Engine
- **In-memory data storage** for faster performance.
- Optimized for large datasets and complex queries.

### Security & Permissions
- Uses **AWS IAM** for role-based access control.
- Supports **row-level security (RLS)** to restrict data access.

### Embedding & API Integration
- Embed QuickSight dashboards into web apps.
- Use **QuickSight APIs** for automation and data refresh.



## Getting Started

## Import Dataset into QuickSight and Create Visualizations

Created the following dashboards for the dataset `employee_laid_off`:

### **1. Pie Chart**
- Relationship between **location** and **percentage_laid_off**


![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/11.png?raw=true) )

### **2. Bar Chart**
- Relationship between **funds_raised** and **industry**
  
![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/12.png?raw=true) )

### **3. Heat Map**
- Relationship between **count_of_records** and **funds_raised_millions**
  
![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/13.png?raw=true) )

### **4. Vertical Stacked Bar Chart**
- Relationship between **Job level** and **Monthly Compensation**
  
![Stacked Bar Chart](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/14.png?raw=true) )


## Accessing Users using AWS CLI

### **List QuickSight Users**
```sh
aws quicksight list-users --aws-account-id 970547378939 --namespace default --region us-east-1
```

![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/15.png?raw=true) )


### **Using Python (Boto3 SDK) to List QuickSight Users and Dashboards**

```python
import boto3

client = boto3.client('quicksight', region_name='us-east-1')

account_id = "970547378939"  # Replace with your actual AWS Account ID

response = client.list_dashboards(AwsAccountId=account_id)

```

for dashboard in response['DashboardSummaryList']:
    print(f"Dashboard Name: {dashboard['Name']}, Dashboard ID: {dashboard['DashboardId']}")

![Python SDK](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/16.png?raw=true) )

---

## Adding Permissions to QuickSight to Retrieve Data from S3

### **Manage QuickSight and Add Permissions**

![Manage QuickSight](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/17.png?raw=true) )

### **Connecting to the Data Source (S3)**

![S3 Connection](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/18.png?raw=true) )

### **Connection Establishment**

![Connection Establishment](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/19.png?raw=true) )

### **Data Visualization of Employees**

![Employee Visualization](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/20.png?raw=true) )

---

## Manifest File JSON for S3 Data Import

```json
{
  "fileLocations": [
    {
      "URIs": ["s3://my-employees/employees.csv"]
    }
  ]
}
```

### **Upload the File to S3 Bucket**

Ensure the file `employees.csv` is uploaded to the S3 bucket before proceeding with data import.

---

## Troubleshooting: Add Policy Permissions to QuickSight

### **IAM Policy for S3 Access**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "quicksight.amazonaws.com"},
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-employees/*"
    }
  ]
}
```

Ensure that the IAM role associated with QuickSight has the necessary permissions to access S3 data.


## Common Challenges & Solutions

| **Challenge**                     | **Solution** |
|-----------------------------------|-------------|
| 🔗 Data Connectivity Issues       | Ensure proper connectors are configured, use **AWS Glue** for ETL. |
| 🐢 Performance with Large Datasets | Optimize queries, leverage **SPICE**, aggregate data at the source. |
| 📌 Data Transformation Complexity  | Use QuickSight transformations or preprocess data with **AWS Glue**. |
| 🔑 User Access Management          | Implement **IAM roles** and **row-level security**. |
| 🎨 Customization Limitations       | Use **QuickSight Custom Visuals SDK** for advanced visualizations. |

---

## Best Practices

- **Optimize Data Sources**: Pre-aggregate data before loading into QuickSight.
- **Leverage SPICE**: Store frequently accessed data in SPICE for performance gains.
- **Automate Reporting**: Schedule **dashboard refreshes** and email reports.
- **Secure Access**: Use **IAM roles & row-level security** for controlled access.
- **Embed Dashboards**: Use **QuickSight APIs** for seamless integration.

---


# AWS Glue Data Catalog

## Overview
AWS Glue Data Catalog is a **logical metadata repository** within AWS that stores metadata about datasets across various sources like Amazon S3, RDS, Redshift, and other JDBC-compliant databases. It helps **organize, manage, and query** datasets efficiently. **Note:** It is not a physical database but a metadata store.

## 1. **Introduction to AWS Glue Data Catalog**
### What is AWS Glue Data Catalog?
- A **centralized metadata repository** that allows you to store and manage metadata for your data assets across various sources.
- Acts as a **persistent catalog** for AWS services like **Athena, Redshift Spectrum, and EMR**.

### Key Benefits
- **Serverless** and automatically scales.
- **Supports schema evolution** for dynamic data structures.
- **Integrates with AWS services** like S3, RDS, and Redshift.
- **Provides data lineage and governance capabilities**.

## 2. **Key Components of AWS Glue Data Catalog**
### a. **Databases**
- Logical grouping of tables.
- Helps organize metadata for different datasets.

### b. **Tables**
- Represents metadata for actual data stored in S3, RDS, or other sources.
- Stores schema, partition information, and storage location.

### c. **Crawlers**
- Automatically scans data sources and populates tables.
- Supports incremental updates.
- Handles schema evolution automatically.

### d. **Partitions**
- Helps optimize query performance.
- Used in Athena and Redshift Spectrum for better query execution.

### e. **Glue Catalog API & Integration**
- Accessible via **Boto3 (Python)** and **AWS SDK** for automation.
- Can be queried directly using Athena.

## 3. **Backend Framework and How It Works**
### **Architecture Flow**
#### **Data Ingestion**
- Data can be stored in **S3, DynamoDB, RDS**, or other sources.

#### **Glue Crawlers**
- Automatically extract metadata and populate the Data Catalog.

#### **Schema Registry**
- Tracks changes in schema over time.

#### **Athena/Redshift Spectrum Queries**
- Enables direct querying of data in S3.

#### **Integration with Data Lake**
- AWS **Lake Formation** can be used for **access control and governance**.

## 4. **Features**
### a. **Data Discovery**
- Supports data stored in **Amazon S3, Redshift, RDS, DynamoDB**, and **JDBC-compliant databases**.
- Enables **automatic schema detection** and metadata generation.

### b. **ETL (Extract, Transform, Load)**
- Integrates with **AWS Glue ETL jobs** to process and transform data.
- Helps automate **data pipeline workflows**.

### c. **Data Catalog**
- A **persistent metadata store** that can connect to **over 70 different data sources**.
- Provides **centralized management** of metadata.
- Enables **schema evolution and versioning**.

### d. **Key Components**
#### - **Databases & Tables**
  - A Glue **Database** is a **logical container** for organizing Tables.
  - A Glue **Table** stores **metadata** about actual data, including schema and storage location.

#### - **Connections**
  - A **configuration object** that enables AWS Glue to **connect to external data stores**.
  - Stores necessary connection details such as **database endpoint, username, and password**.
  - Supports connections to **RDS, Redshift, and other JDBC-compliant databases**.

#### - **Crawlers**
  - Programs that **scan data sources**, infer **schemas**, and create/update metadata tables in the Glue Data Catalog.
  - Can be **scheduled or triggered** to keep metadata updated.

## 5. **How Crawlers Work**
1. **Crawler establishes a connection** with the data source (e.g., S3, RDS, Redshift).
2. **Scans the dataset** to infer schema and structure.
3. **Creates or updates a table** in the Glue Data Catalog with the extracted metadata.

```plaintext
Crawler ----> Establishes connection with S3 ----> Table is created in Glue Data Catalog
```



## Use Cases
- **Centralized Metadata Management**: Provides a single metadata repository for multiple AWS services.
- **Schema Evolution Handling**: Supports automatic schema updates to reflect data changes.
- **Querying with Athena & Redshift Spectrum**: Enables direct querying of data in S3 using SQL.
- **ETL Automation**: Facilitates seamless data transformations using AWS Glue jobs.

### 1. Creating the S3 Bucket and Uploading Files
Initially, a bucket and file were created in the following location:
![Product Visualization](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/21.png?raw=true) )

### 2. Creating the IAM Role and Attaching Policies
A role was created and the necessary policies were attached:
![Roles](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/22.png?raw=true) )

### 3. Creating the Crawler
A crawler was set up to catalog the data:
![Crawler](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/23.png?raw=true) )

### 4. Executing the Crawler
After the successful execution of the crawler, a table was created:
![Crawler](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/24.png?raw=true) )

### 5. Setting Up Athena
If using Athena for the first time, setup is required:
![Athena Setup](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/25.png?raw=true) )

### 6. Query Execution in Athena
Results after executing a query in Athena:
![Athena Result](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/26.png?raw=true) )

### 7. Creating an ETL Job and Destination Folder
An ETL job was created, and a destination folder was set up:
![ETL](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/27.png?raw=true) )

### 8. Viewing Processed Data
To view the results again, a new table can be created in the Glue catalog and queried using Athena.

status of the crawler using CLI
$ aws glue get-crawler --name products --query "Crawler.State" --region us-east-1
![status](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/28.png?raw=true) )

To create the database using CLI
```bash
$ aws glue create-database --database-input '{"Name":"my_employees_data_catalog_db","Description":"My Glue Data Catalog Database"}'
```
![dbcreation](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/29.png?raw=true) )

Command to create the crawler
```bash
aws glue create-crawler --name my_employee_s3_crawler \
    --role arn:aws:iam::970547378939:role/gluerole \
    --database-name my_data_catalog_db \
    --targets '{"S3Targets": [{"Path": "s3://my-employees/employees.csv"}]}'
```

![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/30.png?raw=true) )

Create the table using CLI
```bash
$ aws glue create-table --database-name my_employees_data_catalog_db --table-input '{
    "Name": "my_employee_s3_table",
    "TableType": "EXTERNAL_TABLE",
    "StorageDescriptor": {
        "Columns": [
            {"Name": "id", "Type": "int"},
            {"Name": "name", "Type": "string"},                                             {"Name": "age", "Type": "int"}                                              ],                                                                              "Location": "s3://my-employees/",                                               "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",                      "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",                                                                                   "SerdeInfo": {                                                                      "SerializationLibrary": "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
            "Parameters": {"field.delim": ","}
        }
    }
}'
```
![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/31.png?raw=true) )

Code to create database, table and crawler

```python

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

```

![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/31.png?raw=true) )
![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/32.png?raw=true) )
![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/33.png?raw=true) )
![My Image](https://github.com/Anusha1126/AWS/blob/main/Week1/Day3/images/34.png?raw=true) )



Troubleshooting:
IAM role and path mistake

## Conclusion
AWS Glue Data Catalog simplifies metadata management and enables efficient data discovery, governance, and integration with AWS analytics and ETL services. It plays a crucial role in modern **serverless data lakes** and **big data processing workflows**.

References
https://www.youtube.com/watch?v=weWeaM5-EHc&t=1147s
