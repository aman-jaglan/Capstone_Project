import requests
import pandas as pd
import os
import time
from datetime import datetime
from sklearn.model_selection import train_test_split

# --------------------------------
# Settings and API Key Setup
# --------------------------------
NEWS_API_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key.
stocks = [
    'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
    'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
    'TSLA', 'F', 'COIN', 'MRNA'
]

# --------------------------------
# Define Date Range for Fetching Data
# --------------------------------
# Your plan permits articles as far back as 2025-03-07.
# To avoid issues on the boundary, we start on 2025-03-08.
# We fetch articles until the current date.
start_date = datetime(2025, 3, 11)
end_date = datetime.now()  # Current date

def fetch_news(stock, from_date, to_date, api_key):
    """
    Fetch news articles for a given stock symbol between from_date and to_date.
    Uses the "everything" endpoint with an enhanced financial query.
    """
    url = "https://newsapi.org/v2/everything"
    # Enhance query by combining the stock ticker with financial-related keywords.
    query = f'{stock} AND (stock OR shares OR "financial news" OR market)'
    params = {
        "q": query,
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 100,     # Maximum articles per request
        "apiKey": api_key,
    }
    
    try:
        response = requests.get(url, params=params)
    except Exception as e:
        print(f"Error fetching news for {stock}: {e}")
        return []
    
    if response.status_code != 200:
        try:
            error_message = response.json().get("message", "No error message provided.")
        except Exception:
            error_message = "No error message provided."
        print(f"Error response for {stock}: {response.status_code} - {error_message}")
        return []
    
    try:
        data = response.json()
    except Exception as e:
        print(f"Error decoding JSON for {stock}: {e}")
        return []
    
    if data.get("status") != "ok":
        print(f"API returned error for {stock}: {data.get('message')}")
        return []
    
    articles = data.get("articles", [])
    if not articles:
        print(f"No articles found for {stock} between {from_date.strftime('%Y-%m-%d')} and {to_date.strftime('%Y-%m-%d')}.")
    
    records = []
    for article in articles:
        records.append({
            "stock": stock,
            "publishedAt": article.get("publishedAt"),
            "title": article.get("title"),
            "description": article.get("description"),
            "content": article.get("content"),
            "source": article.get("source", {}).get("name")
        })
    return records

print(f"Fetching news data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...\n")

# --------------------------------
# Load Existing Master File (if available)
# --------------------------------
master_filename = "stock_news_master.csv"
if os.path.exists(master_filename):
    existing_df = pd.read_csv(master_filename)
    # Convert publishedAt to a timezone-aware datetime (UTC)
    existing_df['publishedAt'] = pd.to_datetime(existing_df['publishedAt'], errors='coerce', utc=True)
    print(f"Loaded existing master file with {len(existing_df)} records.")
else:
    existing_df = pd.DataFrame()

# --------------------------------
# Determine Stocks Needing to be Fetched
# --------------------------------
fetched_stocks = set(existing_df['stock'].unique()) if not existing_df.empty else set()
stocks_to_fetch = [s for s in stocks if s not in fetched_stocks]
print(f"Stocks already fetched: {fetched_stocks}")
print(f"Stocks to fetch news for: {stocks_to_fetch}")

# --------------------------------
# Fetch News for Stocks That Haven't Been Fetched Yet
# --------------------------------
for stock in stocks_to_fetch:
    print(f"Fetching news for {stock}...")
    articles = fetch_news(stock, start_date, end_date, NEWS_API_KEY)
    print(f"  Found {len(articles)} articles for {stock}.")
    if articles:
        new_df = pd.DataFrame(articles)
        # Convert publishedAt to UTC (tz-aware)
        new_df['publishedAt'] = pd.to_datetime(new_df['publishedAt'], errors='coerce', utc=True)
        existing_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        print(f"No new articles for {stock}.")
    time.sleep(1)  # Small delay to help with rate limiting

total_articles = len(existing_df)
print(f"\nTotal articles fetched (including previous data): {total_articles}.")

# --------------------------------
# Save Updated Master News File
# --------------------------------
existing_df.to_csv(master_filename, index=False)
print(f"\nMaster news data saved to {master_filename} with {total_articles} records.")

# --------------------------------
# Split the Data into Train/Validation and Test Sets
# --------------------------------
# Use articles published on or after 2025-04-01 as the test set (for backtesting).
# The remainder (before 2025-04-01) goes to training + validation.
split_date = pd.to_datetime("2025-04-01").tz_localize("UTC")
test_df = existing_df[existing_df['publishedAt'] >= split_date]
train_val_df = existing_df[existing_df['publishedAt'] < split_date]

print(f"\nTotal records for training+validation: {len(train_val_df)}")
print(f"Total records for test (backtesting): {len(test_df)}")

# Further split training+validation into train and validation (e.g., 90% train, 10% validation)
if len(train_val_df) > 0:
    train_df, val_df = train_test_split(train_val_df, test_size=0.1, random_state=42)
else:
    train_df = train_val_df.copy()
    val_df = pd.DataFrame()

train_filename = "stock_news_train.csv"
val_filename = "stock_news_val.csv"
test_filename = "stock_news_test.csv"

train_df.to_csv(train_filename, index=False)
val_df.to_csv(val_filename, index=False)
test_df.to_csv(test_filename, index=False)

print(f"\nSplit sizes:")
print(f"  Training set: {len(train_df)} records saved to {train_filename}")
print(f"  Validation set: {len(val_df)} records saved to {val_filename}")
print(f"  Test set: {len(test_df)} records saved to {test_filename}")

print("\nSample fetched news articles:")
print(existing_df.head())
