import pandas as pd
import datetime

def clean_and_process_csv(file_path):
    # Load CSV, skipping metadata row
    df = pd.read_csv(file_path, skiprows=2)

    # Keep only relevant columns
    df = df.iloc[:, 2:]  # last four columns
    df.columns = ['date', 'posting_date', 'amount', 'description']

    # Convert date formats to YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    df['posting_date'] = pd.to_datetime(df['posting_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')

    # Ensure amount is numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # Tag transaction type
    df['transaction_type'] = df['amount'].apply(lambda x: 'Income' if x < 0 else 'Expense')

    # Convert all amounts to positive values
    df['amount'] = df['amount'].abs()

    # Exclude specific payment text from Income
    df = df[~((df['description'].str.contains("PAYMENT RECEIVED - THANK YOU", case=False, na=False)) 
               & (df['transaction_type'] == "Income"))]

    # Add month_year column for MySQL grouping
    df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')

    return df
