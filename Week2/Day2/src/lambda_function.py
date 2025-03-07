import boto3
import json
import csv
import io
from decimal import Decimal  # Import Decimal to handle numeric values

# AWS resources
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

# DynamoDB Table
TABLE_NAME = "Employees"
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        print("Received Event:", json.dumps(event, indent=2))
        for record in event.get('Records', []):
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            print(f"Processing file: {key} from bucket: {bucket}")

            # Extract: Read file from S3
            try:
                file_obj = s3_client.get_object(Bucket=bucket, Key=key)
                file_content = file_obj['Body'].read().decode('utf-8')
            except Exception as e:
                print(f"Error reading file {key} from bucket {bucket}: {e}")
                continue

            # Transform: Process CSV/JSON data
            if key.endswith('.csv'):
                try:
                    transformed_data = process_csv(file_content)
                except Exception as e:
                    print(f"Error processing CSV file {key}: {e}")
                    continue
            elif key.endswith('.json'):
                try:
                    transformed_data = process_json(file_content)
                except Exception as e:
                    print(f"Error processing JSON file {key}: {e}")
                    continue
            else:
                print(f"Unsupported file format: {key}")
                continue

            # Load: Insert transformed data into DynamoDB
            for item in transformed_data:
                try:
                    table.put_item(Item=item)
                except Exception as e:
                    print(f"Error inserting item into DynamoDB: {e}")
            print(f"✅ Data from {key} inserted into DynamoDB.")
        return {"statusCode": 200, "body": "ETL process complete"}
    except Exception as overall_exception:
        print(f"Unhandled exception in lambda_handler: {overall_exception}")
        raise

def process_csv(file_content):
    """
    Processes CSV content and converts SALARY and COMMISSION_PCT using Decimal.
    """
    records = []
    csv_reader = csv.DictReader(io.StringIO(file_content))
    
    for row in csv_reader:
        # Convert SALARY using Decimal
        salary_str = row["SALARY"].strip()
        if salary_str in ["", "-"]:
            salary = Decimal("0")
        else:
            try:
                salary = Decimal(salary_str)
            except Exception as e:
                print(f"Error converting SALARY value '{salary_str}': {e}")
                salary = Decimal("0")

        # Convert COMMISSION_PCT using Decimal
        commission_str = row["COMMISSION_PCT"].strip()
        if commission_str in ["", "-"]:
            commission_pct = Decimal("0")
        else:
            try:
                commission_pct = Decimal(commission_str)
            except Exception as e:
                print(f"Error converting COMMISSION_PCT value '{commission_str}': {e}")
                commission_pct = Decimal("0")
                
        transformed_record = {
            "EMPLOYEE_ID": row["EMPLOYEE_ID"],
            "FIRST_NAME": row["FIRST_NAME"],
            "LAST_NAME": row["LAST_NAME"],
            "EMAIL": row["EMAIL"],
            "PHONE_NUMBER": row["PHONE_NUMBER"],
            "HIRE_DATE": row["HIRE_DATE"],
            "JOB_ID": row["JOB_ID"],
            "SALARY": salary,
            "COMMISSION_PCT": commission_pct,
            "MANAGER_ID": row["MANAGER_ID"],
            "DEPARTMENT_ID": row["DEPARTMENT_ID"]
        }
        records.append(transformed_record)
        print("Row read from CSV:", row)
    
    return records

def process_json(file_content):
    """
    Processes JSON content and converts numeric fields using Decimal.
    """
    data = json.loads(file_content)
    records = []
    
    for item in data:
        try:
            salary = Decimal(str(item.get("SALARY", "0")))
        except Exception as e:
            print(f"Error converting SALARY: {e}")
            salary = Decimal("0")
            
        try:
            commission_pct = Decimal(str(item.get("COMMISSION_PCT", "0")))
        except Exception as e:
            print(f"Error converting COMMISSION_PCT: {e}")
            commission_pct = Decimal("0")
        
        transformed_record = {
            "EMPLOYEE_ID": item.get("EMPLOYEE_ID", "Unknown"),
            "FIRST_NAME": item.get("FIRST_NAME", ""),
            "LAST_NAME": item.get("LAST_NAME", ""),
            "EMAIL": item.get("EMAIL", ""),
            "PHONE_NUMBER": item.get("PHONE_NUMBER", ""),
            "HIRE_DATE": item.get("HIRE_DATE", ""),
            "JOB_ID": item.get("JOB_ID", ""),
            "SALARY": salary,
            "COMMISSION_PCT": commission_pct,
            "MANAGER_ID": item.get("MANAGER_ID", ""),
            "DEPARTMENT_ID": item.get("DEPARTMENT_ID", "")
        }
        records.append(transformed_record)
    
    return records
