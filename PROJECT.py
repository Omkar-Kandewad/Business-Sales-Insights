# Business Sales Insights using Oracle SQL, Pandas & Matplotlib

import pandas as pd
import matplotlib.pyplot as plt
import cx_Oracle

# -----------------------------
# Oracle Connection
# -----------------------------
conn = cx_Oracle.connect(
    user="C##HR",
    password="C##HR",
    dsn="localhost:1521/xe"
)

# -----------------------------
# SQL Query
# -----------------------------
query = """
SELECT 
    o.order_id,
    c.customer_name,
    c.city,
    o.order_date,
    o.product,
    o.quantity,
    o.price,
    (o.quantity * o.price) AS total_amount
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
"""

# -----------------------------
# Load data into DataFrame
# -----------------------------
df = pd.read_sql(query, conn)

# 🔥 IMPORTANT FIX (THIS LINE SOLVES YOUR ERROR)
df.columns = df.columns.str.lower()

print(df)

# -----------------------------
# Total Revenue
# -----------------------------
print("Total Revenue:", df['total_amount'].sum())

# -----------------------------
# Revenue by Product
# -----------------------------
product_revenue = df.groupby('product')['total_amount'].sum()
print(product_revenue)

product_revenue.plot(kind='bar')
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.show()

# -----------------------------
# Top Customers
# -----------------------------
customer_revenue = df.groupby('customer_name')['total_amount'].sum().sort_values(ascending=False)
print(customer_revenue)

customer_revenue.plot(kind='bar')
plt.title("Top Customers by Revenue")
plt.xlabel("Customer")
plt.ylabel("Total Revenue")
plt.show()

# -----------------------------
# Monthly Sales Trend
# -----------------------------
df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.to_period('M')

monthly_sales = df.groupby('month')['total_amount'].sum()
print(monthly_sales)

monthly_sales.plot(marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

conn.close()



