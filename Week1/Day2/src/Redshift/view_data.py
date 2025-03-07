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