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
