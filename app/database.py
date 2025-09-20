import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Database credentials from .env
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DB")

# Establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Create transactions table if it doesn't exist
def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS bank_transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        date DATE NOT NULL,
        posting_date DATE NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        transaction_type ENUM('Income', 'Expense') NOT NULL,
        description TEXT NOT NULL,
        month_year VARCHAR(7) NOT NULL
    );
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

# Insert transactions into the database
def insert_transactions(df):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO bank_transactions 
    (name, date, posting_date, amount, transaction_type, description, month_year)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    # Convert DataFrame to list of tuples
    records = df[['Name', 'date', 'posting_date', 'amount', 'transaction_type', 'description', 'month_year']].values.tolist()

    cursor.executemany(insert_query, records)
    conn.commit()

    cursor.close()
    conn.close()

# Fetch transactions for a specific user
def get_transactions(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, date, posting_date, amount, transaction_type, description, month_year FROM bank_transactions WHERE name = %s ORDER BY date DESC"
    cursor.execute(query, (name,))
    records = cursor.fetchall()

    # Define column names
    columns = ['id', 'name', 'date', 'posting_date', 'amount', 'transaction_type', 'description', 'month_year']
    df = pd.DataFrame(records, columns=columns)

    cursor.close()
    conn.close()
    
    return df
