💰DeepSeek AI – Personal Financial Advisor & Expense Tracker

DeepSeek AI helps you track and analyze your personal finances by integrating AI-powered expense tracking, SQL generation, and financial insights. It’s a self-hosted AI-powered bookkeeper that securely manages your financial data locally, without cloud dependency.
---
✨ Features
•	📂 CSV-Based Expense Tracking – Upload your bank transactions CSV to analyze spending.
•	📊 AI Categorization – Automatically classifies transactions (Groceries, Rent, Travel, etc.).
•	🧠 AI-Powered Insights – Generates actionable financial advice based on your transactions.
•	🏦 Database Integration – Store transactions in PostgreSQL (or MySQL) for historical analysis.
•	🔍 AI-Generated SQL Queries – Ask natural language financial questions, and AI generates & executes SQL queries.
•	🔄 Auto-Correcting AI Queries – AI refines SQL queries automatically if they fail.
•	📈 Financial Visualization – Generates bar charts, spending trends, and breakdowns.
•	🔐 100% Local & Private – Runs on your machine, no cloud storage needed.
---
🛠️ Tech Stack
•	AI Model: DeepSeek R1 (running locally via Ollama)
•	UI: Streamlit
•	Database: PostgreSQL (or MySQL with minor adjustments)
•	Backend: Python
---
🔧 Setup Instructions
1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
2️⃣ Set Up Database
Ensure PostgreSQL is running locally and update .env with your credentials:
```plaintext
POSTGRES_HOST='localhost'
POSTGRES_PORT='5432'
POSTGRES_USER='your_db_user'
POSTGRES_PASSWORD='your_db_password'
POSTGRES_DB='your_db_name'
```
For MySQL, update the database connection settings in app/database.py accordingly.
3️⃣ Run Ollama Locally
```bash
ollama run deepseek-r1:8b
```
4️⃣ Launch the Streamlit App
```bash
streamlit run app/main.py
```
---
🏗️ How It Works
1.	Upload Transactions – Upload CSV files of your bank statements.
2.	AI Categorization & Charts – AI categorizes transactions and displays visual insights.
3.	Store in Database – Click 'Load Data to PostgreSQL' to store your data.
4.	Ask AI Financial Questions – Examples: 'What was my biggest expense last month?', 'How much did I spend on groceries this year?'
5.	AI Generates & Executes SQL – AI converts the question into SQL, executes it, and provides results.
6.	Self-Correcting Queries – Queries automatically refine and retry if they fail.
---
🎯 Example Queries
What was my biggest expense last month?
```sql
SELECT MAX(amount), description 
FROM upload_transactions 
WHERE transaction_type = 'Expense' AND month_year = '2024-01';
```
How much have I spent on food?
```sql
SELECT SUM(amount) 
FROM upload_transactions 
WHERE category = 'Food';
```
---
🔥 Future Improvements
•	More AI-driven financial insights
•	Interactive dashboard with filters
•	Support for multiple banks & currencies
•	Export customized financial reports
---
💡 Contribute & Feedback
DeepSeek AI is designed to securely manage your finances using AI. If you find it useful or have suggestions, contribute or open an issue on GitHub.

📩 Let’s improve this together!
---
💙 If you like this project, give it a ⭐ on GitHub and share your feedback!
