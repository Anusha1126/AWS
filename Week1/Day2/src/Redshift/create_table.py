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