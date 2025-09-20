import requests
import pandas as pd
import logging
import re
import json
import time

# 🔹 Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Define Ollama API Endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:8b"

def query_ollama(prompt):
    """Send a request to Ollama's local API and return the response."""
    logging.info("📡 Sending batch request to Ollama AI...")
    payload = {"model": MODEL, "prompt": prompt, "stream": False}

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        ai_response = response.json().get("response", "").strip()
        
        logging.info("✅ Ollama AI Response Received.")
        return ai_response
    except requests.RequestException as e:
        logging.error(f"❌ Ollama API request failed: {e}")
        return None  # Return None if API call fails

def batch_categorize_transactions(df):
    """Use AI to categorize all transactions using a lookup dictionary."""
    
    logging.info("🔄 Starting AI-based batch transaction categorization...")
    
    # 🔹 Format transactions for AI processing
    transactions_list = [{"description": desc} for desc in df["description"]]
    
    categorization_prompt = f"""
    You are an expert financial assistant. Categorize each transaction based on its description.

    ### Transactions:
    {json.dumps(transactions_list, indent=2)}

    ### Instructions:
    - Assign a **single category** to each transaction from the list below:
      - Groceries
      - Dining
      - Entertainment
      - Insurance
      - Shopping
      - Transport
      - Healthcare
      - Utilities
      - Rent
      - Other (if unclassifiable)
    - **Output must be a JSON object where each description maps to its category.**
    - **Do NOT modify, merge, or remove duplicate descriptions.**
    - **Do NOT include additional explanations, comments, or formatting.**
    - **Ensure the number of items in the response matches the number of transactions provided.**

    ### Example Correct Output:
    ```json
    {{
      "Walmart Groceries": "Groceries",
      "Uber Ride": "Transport",
      "Netflix Subscription": "Entertainment"
    }}
    ```
    """

    ai_response = query_ollama(categorization_prompt)

    if ai_response:
        # 🔹 Remove <think>...</think> section before processing
        ai_response = re.sub(r"<think>.*?</think>", "", ai_response, flags=re.DOTALL).strip()

        # 🔹 Log AI response correctly
        logging.info(f"Raw AI Response: {ai_response}")

        # 🔹 Extract only the JSON object from AI response
        json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)

        if json_match:
            max_retries = 3
            retry_count = 0
            ai_category_map = None

            while retry_count < max_retries:
                try:
                    ai_category_map = json.loads(json_match.group(0))  # Convert JSON response to a dictionary
                    logging.info(f"Extracted AI Category Map: {ai_category_map}")

                    # 🔹 Apply AI categories to dataframe using a lookup
                    df["Category"] = df["description"].map(lambda desc: ai_category_map.get(desc, "Other"))
                    logging.info("✅ All transactions categorized successfully.")
                    break  # ✅ Successful parsing, exit loop

                except json.JSONDecodeError:
                    retry_count += 1
                    logging.warning(f"⚠️ Attempt {retry_count}/{max_retries}: AI response is not valid JSON. Retrying...")
                    time.sleep(1)  # Pause for a second before retrying

            # If parsing failed after 3 attempts, default to "Other"
            if ai_category_map is None:
                logging.error("❌ AI response is still not valid JSON after 3 retries. Defaulting all to 'Other'.")
                df["Category"] = "Other"

        else:
            logging.error("❌ AI response did not contain a valid JSON object. Defaulting all to 'Other'.")
            df["Category"] = "Other"

    else:
        logging.error("❌ AI failed to return categories. Defaulting all to 'Other'.")
        df["Category"] = "Other"

    return df  # Return categorized dataframe


import json

def generate_insights(df):
    """Use AI to generate financial insights based on full transaction data, including the 'Category' column but without relying on it."""
    
    logging.info("💡 Generating financial insights based on full transaction data...")

    # 🔹 Convert full dataframe to JSON for AI processing (keeping "Category" column)
    transactions_json = df.to_json(orient="records")

    insights_prompt = f"""
    You are an expert financial analyst. Analyze the **full transaction data** below to identify financial trends, spending patterns, and anomalies.

    ### Full Transactions Data:
    {transactions_json}

    ### Instructions:
    - Identify **which transactions have the highest spending**.
    - Detect **any unusual or high-value transactions that stand out**.
    - Spot **patterns in spending behavior** across different merchants and transaction types.
    - Identify **repeated transactions** (such as subscriptions or recurring expenses).
    - Suggest **budget improvements based on transaction history**.
    - Provide insights on **potential cost-saving opportunities**.
    - The "Category" column is available for reference, but do not rely on it—derive insights from the full data.

    Provide your insights in a structured, concise format:
    """

    ai_insights = query_ollama(insights_prompt)

    if ai_insights:
        logging.info("✅ AI Insights Generated Successfully.")
        ai_insights = re.sub(r"<think>.*?</think>", "", ai_insights, flags=re.DOTALL).strip()
    else:
        logging.warning("⚠️ AI Insights Generation Failed.")

    return ai_insights  # Return AI-generated insights

