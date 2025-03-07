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
