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