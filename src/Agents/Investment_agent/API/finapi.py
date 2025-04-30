
# import os
# import requests
# from flask import Flask, jsonify, request
# import logging
# from flask_cors import CORS  # Import CORS to enable cross-origin requests

# # Disable tokenizers parallelism warning
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

# # Initialize the Flask app
# app = Flask(__name__)

# # Enable CORS for all routes
# CORS(app)

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Replace with your own Alpha Vantage API key
# ALPHA_VANTAGE_API_KEY = 'YOUR_API_KEY'


# # =======================
# # Component 1: DataFetcherComponent
# # =======================
# class DataFetcherComponent:
#     def __init__(self):
#         self.url = "https://www.alphavantage.co/query"
#         logging.info("DataFetcherComponent initialized")

#     def fetch_real_time_stock_data(self, symbol):
#         """
#         Fetches real-time stock data for any stock symbol from Alpha Vantage API.

#         Args:
#             symbol (str): The stock symbol (e.g., AAPL, TSLA).

#         Returns:
#             dict: Stock data in JSON format.
#         """
#         logging.debug(f"Fetching real-time stock data for symbol: {symbol}")
#         params = {
#             'function': 'GLOBAL_QUOTE',  # 'GLOBAL_QUOTE' gets the latest data for a stock
#             'symbol': symbol,            # Stock symbol entered by the user (e.g., AAPL, TSLA)
#             'apikey': ALPHA_VANTAGE_API_KEY            
#         }

#         try:
#             response = requests.get(self.url, params=params)
#             response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
#             logging.info(f"Successfully fetched stock data for {symbol}")
#             return response.json()  # Return the data in JSON format
#         except requests.exceptions.HTTPError as err:
#             logging.error(f"HTTP error occurred: {err}")
#         except Exception as err:
#             logging.error(f"An error occurred: {err}")
#         return None


# # =======================
# # Component 2: QueryHandlerComponent
# # =======================
# class QueryHandlerComponent:
#     def __init__(self, data_fetcher):
#         logging.info("QueryHandlerComponent initialized")
#         self.data_fetcher = data_fetcher

#     def handle_query(self, user_query):
#         """Handles the user query and returns the most relevant stock data."""
#         if not user_query:
#             return {"error": "No query parameter provided."}, 400  # Ensure two values are returned

#         stock_symbol = user_query.strip().upper()  # Makes the input uppercase
#         logging.debug(f"Handling query for stock symbol: {stock_symbol}")

#         # Fetch the stock data
#         stock_data = self.data_fetcher.fetch_real_time_stock_data(stock_symbol)
#         logging.debug(f"Fetched stock data: {stock_data}")

#         if stock_data:
#             # Extract the stock data directly from the API response
#             global_quote = stock_data.get('Global Quote', {})
#             if global_quote:
#                 response = {
#                     "symbol": global_quote.get('01. symbol', 'N/A'),
#                     "open": global_quote.get('02. open', 'N/A'),
#                     "high": global_quote.get('03. high', 'N/A'),
#                     "low": global_quote.get('04. low', 'N/A'),
#                     "price": global_quote.get('05. price', 'N/A'),
#                     "volume": global_quote.get('06. volume', 'N/A'),
#                     "latest_trading_day": global_quote.get('07. latest trading day', 'N/A'),
#                     "previous_close": global_quote.get('08. previous close', 'N/A'),
#                     "change": global_quote.get('09. change', 'N/A'),
#                     "change_percent": global_quote.get('10. change percent', 'N/A')
#                 }
#                 return jsonify(response), 200  # Return stock data as JSON
#             else:
#                 logging.error("No 'Global Quote' data found in the response.")
#                 return {"error": "Unable to fetch valid stock data."}, 500
#         else:
#             logging.error("Unable to fetch stock data.")
#             return {"error": "Unable to fetch stock data."}, 500  # Return error response


# # =======================
# # Component 3: FinancialQAApp (Main app)
# # =======================
# class FinancialQAApp:
#     def __init__(self):
#         logging.info("FinancialQAApp initialized")
#         # Initialize all components
#         self.data_fetcher = DataFetcherComponent()
#         self.query_handler = QueryHandlerComponent(self.data_fetcher)

#     def run(self):
#         """
#         Runs the Flask app and sets up the route for query handling.
#         """
#         logging.debug("Setting up query route...")

#         # Route for handling queries about stock prices/trends
#         @app.route('/api/financial-qa', methods=['GET'])
#         def query():
#             user_query = request.args.get('query')  # Retrieve the query from the request
#             logging.debug(f"Received query: {user_query}")  # Log the query

#             if user_query:
#                 logging.debug("Processing query...")
#                 response, status_code = self.query_handler.handle_query(user_query)  # This will unpack correctly now
#                 logging.debug(f"Response: {response}")
#                 return response, status_code
#             else:
#                 logging.warning("No query parameter provided.")
#                 return jsonify({"error": "No query parameter provided."}), 400

#         # Root route for the app, returning a simple welcome message
#         @app.route('/')
#         def home():
#             return "Welcome to the Financial QA API!"  # Custom message for the root


# # =======================
# # Main Execution
# # =======================
# if __name__ == '__main__':
#     logging.info("Starting Financial QA App")
#     app_instance = FinancialQAApp()
#     app_instance.run()
#     app.run(debug=True)










# import os
# import requests
# from flask import Flask, jsonify, request
# import logging
# from flask_cors import CORS  # Import CORS to enable cross-origin requests

# # Disable tokenizers parallelism warning
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

# # Initialize the Flask app
# app = Flask(__name__)

# # Enable CORS for all routes
# CORS(app)

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Replace with your own Alpha Vantage API key
# ALPHA_VANTAGE_API_KEY = 'YOUR_API_KEY'


# # =======================
# # Component 1: DataFetcherComponent
# # =======================
# class DataFetcherComponent:
#     def __init__(self):
#         self.url = "https://www.alphavantage.co/query"
#         logging.info("DataFetcherComponent initialized")

#     def fetch_real_time_stock_data(self, symbol):
#         """
#         Fetches real-time stock data for any stock symbol from Alpha Vantage API.

#         Args:
#             symbol (str): The stock symbol (e.g., AAPL, TSLA).

#         Returns:
#             dict: Stock data in JSON format.
#         """
#         logging.debug(f"Fetching real-time stock data for symbol: {symbol}")
#         params = {
#             'function': 'GLOBAL_QUOTE',  # 'GLOBAL_QUOTE' gets the latest data for a stock
#             'symbol': symbol,            # Stock symbol entered by the user (e.g., AAPL, TSLA)
#             'apikey': ALPHA_VANTAGE_API_KEY            
#         }

#         try:
#             response = requests.get(self.url, params=params)
#             response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
#             logging.info(f"Successfully fetched stock data for {symbol}")
#             return response.json()  # Return the data in JSON format
#         except requests.exceptions.HTTPError as err:
#             logging.error(f"HTTP error occurred: {err}")
#         except Exception as err:
#             logging.error(f"An error occurred: {err}")
#         return None


# # =======================
# # Component 2: QueryHandlerComponent
# # =======================
# class QueryHandlerComponent:
#     def __init__(self, data_fetcher):
#         logging.info("QueryHandlerComponent initialized")
#         self.data_fetcher = data_fetcher

#     def handle_query(self, user_query):
#         """Handles the user query and returns the most relevant stock data."""
#         if not user_query:
#             return {"error": "No query parameter provided."}, 400  # Ensure two values are returned

#         stock_symbol = user_query.strip().upper()  # Makes the input uppercase
#         logging.debug(f"Handling query for stock symbol: {stock_symbol}")

#         # Fetch the stock data
#         stock_data = self.data_fetcher.fetch_real_time_stock_data(stock_symbol)
#         logging.debug(f"Fetched stock data: {stock_data}")

#         if stock_data:
#             # Extract the stock data directly from the API response
#             global_quote = stock_data.get('Global Quote', {})
#             if global_quote:
#                 response = {
#                     "symbol": global_quote.get('01. symbol', 'N/A'),
#                     "open": global_quote.get('02. open', 'N/A'),
#                     "high": global_quote.get('03. high', 'N/A'),
#                     "low": global_quote.get('04. low', 'N/A'),
#                     "price": global_quote.get('05. price', 'N/A'),
#                     "volume": global_quote.get('06. volume', 'N/A'),
#                     "latest_trading_day": global_quote.get('07. latest trading day', 'N/A'),
#                     "previous_close": global_quote.get('08. previous close', 'N/A'),
#                     "change": global_quote.get('09. change', 'N/A'),
#                     "change_percent": global_quote.get('10. change percent', 'N/A')
#                 }
#                 return jsonify(response), 200  # Return stock data as JSON
#             else:
#                 logging.error("No 'Global Quote' data found in the response.")
#                 return {"error": "Unable to fetch valid stock data."}, 500
#         else:
#             logging.error("Unable to fetch stock data.")
#             return {"error": "Unable to fetch stock data."}, 500  # Return error response


# # =======================
# # Component 3: FinancialQAApp (Main app)
# # =======================
# class FinancialQAApp:
#     def __init__(self):
#         logging.info("FinancialQAApp initialized")
#         # Initialize all components
#         self.data_fetcher = DataFetcherComponent()
#         self.query_handler = QueryHandlerComponent(self.data_fetcher)

#     def run(self):
#         """
#         Runs the Flask app and sets up the route for query handling.
#         """
#         logging.debug("Setting up query route...")

#         # Route for handling queries about stock prices/trends
#         @app.route('/api/financial-qa', methods=['GET'])
#         def query():
#             user_query = request.args.get('query')  # Retrieve the query from the request
#             logging.debug(f"Received query: {user_query}")  # Log the query

#             if user_query:
#                 logging.debug("Processing query...")
#                 response, status_code = self.query_handler.handle_query(user_query)  # This will unpack correctly now
#                 logging.debug(f"Response: {response}")
#                 return response, status_code
#             else:
#                 logging.warning("No query parameter provided.")
#                 return jsonify({"error": "No query parameter provided."}), 400

#         # Root route for the app, returning a simple welcome message
#         @app.route('/')
#         def home():
#             return "Welcome to the Financial QA API!"  # Custom message for the root


# # =======================
# # Main Execution
# # =======================
# if __name__ == '__main__':
#     logging.info("Starting Financial QA App")
#     app_instance = FinancialQAApp()
#     app_instance.run()
#     app.run(debug=True)

# from flask import Flask, jsonify, request
# from flask_cors import CORS  # Import CORS to allow cross-origin requests
# import logging
# import os
# import requests

# os.environ["TOKENIZERS_PARALLELISM"] = "false"

# # Initialize the Flask app
# app = Flask(__name__)

# # Enable CORS for all routes
# CORS(app, resources={"/api/*": {"origins": "*"}})  # Allow all domains for now

# logging.basicConfig(level=logging.DEBUG)

# ALPHA_VANTAGE_API_KEY = 'O30LC68NVP5U8YSQ'


# class DataFetcherComponent:
#     def __init__(self):
#         self.url = "https://www.alphavantage.co/query"
#         logging.info("DataFetcherComponent initialized")

#     def fetch_real_time_stock_data(self, symbol):
#         params = {
#             'function': 'GLOBAL_QUOTE',
#             'symbol': symbol,
#             'apikey': ALPHA_VANTAGE_API_KEY
#         }

#         try:
#             response = requests.get(self.url, params=params)
#             response.raise_for_status()
#             logging.info(f"Successfully fetched stock data for {symbol}")
#             return response.json()
#         except requests.exceptions.HTTPError as err:
#             logging.error(f"HTTP error occurred: {err}")
#         except Exception as err:
#             logging.error(f"An error occurred: {err}")
#         return None


# class QueryHandlerComponent:
#     def __init__(self, data_fetcher):
#         self.data_fetcher = data_fetcher

#     def handle_query(self, user_query):
#         if not user_query:
#             return {"error": "No query parameter provided."}, 400

#         stock_symbol = user_query.strip().upper()
#         stock_data = self.data_fetcher.fetch_real_time_stock_data(stock_symbol)

#         if stock_data:
#             global_quote = stock_data.get('Global Quote', {})
#             if global_quote:
#                 response = {
#                     "symbol": global_quote.get('01. symbol', 'N/A'),
#                     "open": global_quote.get('02. open', 'N/A'),
#                     "high": global_quote.get('03. high', 'N/A'),
#                     "low": global_quote.get('04. low', 'N/A'),
#                     "price": global_quote.get('05. price', 'N/A'),
#                     "volume": global_quote.get('06. volume', 'N/A'),
#                     "latest_trading_day": global_quote.get('07. latest trading day', 'N/A'),
#                     "previous_close": global_quote.get('08. previous close', 'N/A'),
#                     "change": global_quote.get('09. change', 'N/A'),
#                     "change_percent": global_quote.get('10. change percent', 'N/A')
#                 }
#                 return jsonify(response), 200
#             else:
#                 return {"error": "Unable to fetch valid stock data."}, 500
#         else:
#             return {"error": "Unable to fetch stock data."}, 500


# class FinancialQAApp:
#     def __init__(self):
#         self.data_fetcher = DataFetcherComponent()
#         self.query_handler = QueryHandlerComponent(self.data_fetcher)

#     def run(self):
#         @app.route('/api/financial-qa', methods=['GET'])
#         def query():
#             user_query = request.args.get('query')
#             if user_query:
#                 response, status_code = self.query_handler.handle_query(user_query)
#                 return response, status_code
#             else:
#                 return jsonify({"error": "No query parameter provided."}), 400

#         @app.route('/')
#         def home():
#             return "Welcome to the Financial QA API!"


# if __name__ == '__main__':
#     app_instance = FinancialQAApp()
#     app_instance.run()
#     app.run(debug=True)












#YASH

# import yfinance as yf
# import numpy as np
# import pandas as pd
# import torch
# import re
# import os
# from transformers import (
#     AutoTokenizer,
#     AutoModelForSequenceClassification,
#     Trainer,
#     TrainingArguments
# )
# from sklearn.metrics import accuracy_score
# from datetime import datetime, timedelta
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import logging
# from typing import Dict, List, Union

# # Configuration
# os.environ["TOKENIZERS_PARALLELISM"] = "false"
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# CORS(app)

# class StockDataProcessor:
#     def __init__(self, tickers: List[str]):
#         self.tickers = tickers
#         self.historical_data: Dict[str, pd.DataFrame] = {}

#     def fetch_data(self, years: int = 5) -> pd.DataFrame:
#         end_date = datetime.now()
#         start_date = end_date - timedelta(days=365*years)
        
#         for ticker in self.tickers:
#             try:
#                 data = yf.Ticker(ticker)
#                 df = data.history(start=start_date, end=end_date, auto_adjust=True)
                
#                 if df.empty:
#                     continue
                    
#                 df = self._calculate_features(df)
#                 df['ticker'] = ticker
#                 self.historical_data[ticker] = df
                
#             except Exception as e:
#                 continue
        
#         if not self.historical_data:
#             raise ValueError("No valid stock data was fetched")
            
#         return pd.concat(self.historical_data.values())

#     def _calculate_features(self, df: pd.DataFrame) -> pd.DataFrame:
#         df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
#         df['returns'] = df['Close'].pct_change()
#         df['sma_10'] = df['Close'].rolling(10).mean()
#         df['ema_50'] = df['Close'].ewm(span=50, adjust=False).mean()
#         df['rsi'] = self._calculate_rsi(df['Close'].values)
#         df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
#         return df.dropna()

#     @staticmethod
#     def _calculate_rsi(prices: np.ndarray, window: int = 14) -> np.ndarray:
#         deltas = np.diff(prices)
#         seed = deltas[:window+1]
#         up = seed[seed >= 0].sum()/window
#         down = -seed[seed < 0].sum()/window
#         rs = up/down
#         rsi = np.zeros_like(prices)
#         rsi[:window] = 100. - 100./(1.+rs)
        
#         for i in range(window, len(prices)):
#             delta = deltas[i-1]
#             upval = delta if delta > 0 else 0.
#             downval = -delta if delta < 0 else 0.
#             up = (up*(window-1) + upval)/window
#             down = (down*(window-1) + downval)/window
#             rs = up/down
#             rsi[i] = 100. - 100./(1.+rs)
            
#         return rsi

# class FinancialPredictor:
#     def __init__(self, tickers: List[str], model_dir: str = "./saved_model"):
#         self.tickers = tickers
#         self.model_dir = model_dir
#         self.data_processor = StockDataProcessor(tickers)
#         self.tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
#         self.model = AutoModelForSequenceClassification.from_pretrained(
#             "yiyanghkust/finbert-tone",
#             num_labels=2,
#             ignore_mismatched_sizes=True
#         )
#         self.is_trained = False

#     def train(self) -> bool:
#         try:
#             df = self.data_processor.fetch_data()
#             texts, labels = self._create_text_prompts(df)
            
#             encodings = self.tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors="pt")
            
#             training_args = TrainingArguments(
#                 output_dir="./results",
#                 num_train_epochs=3,
#                 per_device_train_batch_size=8,
#                 evaluation_strategy="epoch",
#                 learning_rate=2e-5
#             )
            
#             trainer = Trainer(
#                 model=self.model,
#                 args=training_args,
#                 train_dataset=torch.utils.data.TensorDataset(
#                     torch.tensor(encodings['input_ids']),
#                     torch.tensor(labels)
#                 ),
#                 compute_metrics=lambda eval_pred: {
#                     'accuracy': accuracy_score(*eval_pred)
#                 }
#             )
            
#             trainer.train()
#             self.is_trained = True
#             return True
            
#         except Exception as e:
#             logger.error(f"Training failed: {str(e)}")
#             return False

#     def predict(self, ticker: str) -> Dict[str, Union[str, float]]:
#         if ticker not in self.data_processor.historical_data:
#             self.data_processor.fetch_data()
            
#         df = self.data_processor.historical_data[ticker]
#         latest = df.iloc[-1:].copy()
        
#         text = self._create_text_prompts(latest)[0][0]
#         inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        
#         with torch.no_grad():
#             outputs = self.model(**inputs)
        
#         probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
#         confidence = probs[0][1].item()
        
#         return {
#             'ticker': ticker,
#             'prediction': 'up' if confidence > 0.5 else 'down',
#             'confidence': confidence,
#             'last_close': float(latest['Close'].iloc[0]),
#             'rsi': float(latest['rsi'].iloc[0]),
#             'sma_10': float(latest['sma_10'].iloc[0]),
#             'ema_50': float(latest['ema_50'].iloc[0])
#         }

#     def _create_text_prompts(self, df: pd.DataFrame) -> tuple:
#         texts = []
#         labels = []
#         for _, row in df.iterrows():
#             text = (
#                 f"Stock {row['ticker']} at {row.name.date()}: "
#                 f"Price ${row['Close']:.2f}, "
#                 f"RSI {row['rsi']:.1f}, "
#                 f"SMA10 ${row['sma_10']:.2f}, "
#                 f"EMA50 ${row['ema_50']:.2f}"
#             )
#             texts.append(text)
#             labels.append(int(row['target']))
#         return texts, labels

# predictor = FinancialPredictor(["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "JPM", "NVDA", "WMT"])

# @app.route('/api/analyze', methods=['GET'])
# def analyze():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker or ticker not in predictor.tickers:
#         return jsonify({'error': 'Invalid ticker'}), 400
    
#     try:
#         prediction = predictor.predict(ticker)
#         stock = yf.Ticker(ticker).info
#         return jsonify({
#             'ticker': ticker,
#             'prediction': prediction['prediction'],
#             'confidence': prediction['confidence'],
#             'price': prediction['last_close'],
#             'rsi': prediction['rsi'],
#             'sma_10': prediction['sma_10'],
#             'ema_50': prediction['ema_50'],
#             'pe_ratio': stock.get('trailingPE'),
#             'market_cap': stock.get('marketCap'),
#             'dividend_yield': stock.get('dividendYield')
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/stocks', methods=['GET'])
# def stocks():
#     return jsonify({'tickers': predictor.tickers})

# if __name__ == '__main__':
#     if not predictor.is_trained:
#         predictor.train()
#     app.run(host='0.0.0.0', port=5001, debug=False)


# #NEMI

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime
# import logging

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Configuration
# SUPPORTED_TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "JPM", "NVDA", "WMT"]
# RISK_LEVELS = {
#     'low': ['JPM', 'WMT'],       # Stable blue-chip stocks
#     'medium': ['AAPL', 'MSFT'],  # Balanced growth
#     'high': ['TSLA', 'NVDA']     # High-growth tech
# }

# # In-memory storage
# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys())
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker or ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': 'Invalid ticker'}), 400
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period="1mo")
#         info = stock.info
        
#         # Calculate metrics
#         current_price = hist['Close'].iloc[-1]
#         sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
#         trend = "up" if current_price > sma_10 else "down"
#         confidence = min(0.95, max(0.05, 0.7 if trend == "up" else 0.3))
        
#         response = {
#             'ticker': ticker,
#             'price': round(current_price, 2),
#             'prediction': trend,
#             'confidence': confidence,
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0)
#         }
        
#         # Add investment context
#         if user_profile['available_amount'] > 0:
#             response['shares_possible'] = int(user_profile['available_amount'] / current_price)
        
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/recommend', methods=['GET'])
# def recommend_stocks():
#     try:
#         amount = float(request.args.get('amount', user_profile['available_amount']))
#         risk = request.args.get('risk', user_profile['risk_preference'])
        
#         if risk not in RISK_LEVELS:
#             return jsonify({'error': 'Invalid risk level'}), 400
            
#         recommendations = []
#         for ticker in RISK_LEVELS[risk]:
#             try:
#                 analysis = yf.Ticker(ticker).history(period="1mo")
#                 current_price = analysis['Close'].iloc[-1]
#                 sma_10 = analysis['Close'].rolling(10).mean().iloc[-1]
                
#                 if current_price > sma_10:  # Simple uptrend detection
#                     confidence = min(0.95, max(0.05, 0.7 + (current_price - sma_10)/sma_10))
#                     shares = int(amount / current_price)
#                     recommendations.append({
#                         'ticker': ticker,
#                         'price': round(current_price, 2),
#                         'confidence': confidence,
#                         'potential_shares': shares
#                     })
#             except:
#                 continue
        
#         # Sort by confidence and take top 3
#         recommendations.sort(key=lambda x: x['confidence'], reverse=True)
#         top_picks = recommendations[:3]
        
#         if not top_picks:
#             return jsonify({'status': 'no_recommendations'})
            
#         # Generate allocation plan
#         total_confidence = sum(x['confidence'] for x in top_picks)
#         allocation = []
#         for stock in top_picks:
#             weight = stock['confidence'] / total_confidence
#             allocated = round(amount * weight, 2)
#             shares = int(allocated / stock['price'])
#             allocation.append({
#                 'ticker': stock['ticker'],
#                 'amount': allocated,
#                 'shares': shares,
#                 'percentage': round(weight * 100, 1)
#             })
        
#         return jsonify({
#             'status': 'success',
#             'recommendations': top_picks,
#             'allocation_plan': allocation
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/update_profile', methods=['POST'])
# def update_profile():
#     try:
#         data = request.get_json()
#         user_profile['available_amount'] = float(data.get('amount', 5000.0))
#         user_profile['risk_preference'] = data.get('risk', 'medium')
#         return jsonify({'status': 'profile_updated'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)
    


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# import torch
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from datetime import datetime, timedelta
# import logging
# import time

# app = Flask(__name__)
# CORS(app)

# # Configuration
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# SUPPORTED_TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "JPM", "NVDA", "WMT"]
# RISK_LEVELS = {
#     'low': ['JPM', 'WMT'],
#     'medium': ['AAPL', 'MSFT'],
#     'high': ['TSLA', 'NVDA']
# }

# # Initialize NLP model
# tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
# sentiment_model = AutoModelForSequenceClassification.from_pretrained(
#     "yiyanghkust/finbert-tone",
#     num_labels=3
# )

# # User profile with no default amount
# user_profile = {
#     'available_amount': None,
#     'risk_preference': 'medium'
# }

# def safe_fetch_stock_data(ticker, max_retries=3, delay=1):
#     """Robust stock data fetcher with retries"""
#     for attempt in range(max_retries):
#         try:
#             stock = yf.Ticker(ticker)
#             hist = stock.history(period="1mo", interval="1d")
            
#             if hist.empty:
#                 logger.warning(f"Empty data for {ticker}, attempt {attempt + 1}")
#                 time.sleep(delay)
#                 continue
                
#             return stock, hist
#         except Exception as e:
#             logger.error(f"Attempt {attempt + 1} failed for {ticker}: {str(e)}")
#             if attempt == max_retries - 1:
#                 raise
#             time.sleep(delay)
#     raise ValueError(f"Failed to fetch data for {ticker} after {max_retries} attempts")

# def calculate_rsi(prices, window=14):
#     """Calculate RSI with error handling"""
#     try:
#         deltas = np.diff(prices)
#         seed = deltas[:window+1]
#         up = seed[seed >= 0].sum()/window
#         down = -seed[seed < 0].sum()/window
#         rs = up/down
#         rsi = np.zeros_like(prices)
#         rsi[:window] = 100. - 100./(1.+rs)
        
#         for i in range(window, len(prices)):
#             delta = deltas[i-1]
#             upval = delta if delta > 0 else 0.
#             downval = -delta if delta < 0 else 0.
#             up = (up*(window-1) + upval)/window
#             down = (down*(window-1) + downval)/window
#             rs = up/down
#             rsi[i] = 100. - 100./(1.+rs)
            
#         return rsi[-1]
#     except Exception as e:
#         logger.error(f"RSI calculation failed: {str(e)}")
#         return 50  # Neutral value if calculation fails

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker or ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': 'Invalid ticker', 'valid_tickers': SUPPORTED_TICKERS}), 400
    
#     try:
#         # Robust data fetching
#         stock, hist = safe_fetch_stock_data(ticker)
#         info = stock.info
        
#         # Calculate technical indicators
#         current_price = hist['Close'].iloc[-1]
#         sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
#         rsi = calculate_rsi(hist['Close'].values)
#         trend = "up" if current_price > sma_10 else "down"
        
#         # Sentiment analysis with fallback
#         sentiment = {
#             'sentiment': 'neutral',
#             'confidence': 0.5,
#             'positive': 0.33,
#             'neutral': 0.34,
#             'negative': 0.33,
#             'num_articles': 0
#         }
        
#         try:
#             news = getattr(stock, 'news', [])[:3]  # Safe news access
#             if news:
#                 processed_articles = 0
#                 sentiments = []
                
#                 for article in news:
#                     if not article.get('title'):
#                         continue
                        
#                     try:
#                         inputs = tokenizer(article['title'], return_tensors="pt", truncation=True)
#                         with torch.no_grad():
#                             outputs = sentiment_model(**inputs)
#                         probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
#                         sentiments.append(probs[0].numpy())
#                         processed_articles += 1
#                     except Exception as e:
#                         logger.warning(f"Failed to process article: {str(e)}")
                
#                 if processed_articles > 0:
#                     avg_sentiment = np.mean(sentiments, axis=0)
#                     sentiment_labels = ['negative', 'neutral', 'positive']
#                     dominant = sentiment_labels[np.argmax(avg_sentiment)]
#                     sentiment = {
#                         'sentiment': dominant,
#                         'confidence': float(np.max(avg_sentiment)),
#                         'positive': float(avg_sentiment[2]),
#                         'neutral': float(avg_sentiment[1]),
#                         'negative': float(avg_sentiment[0]),
#                         'num_articles': processed_articles
#                     }
#         except Exception as e:
#             logger.error(f"Sentiment analysis failed: {str(e)}")
        
#         # Prepare response
#         response = {
#             'ticker': ticker,
#             'price': round(float(current_price), 2),
#             'prediction': trend,
#             'confidence': min(0.95, max(0.05, 0.7 if trend == "up" else 0.3)),
#             'sma_10': round(float(sma_10), 2) if not np.isnan(sma_10) else None,
#             'rsi': round(float(rsi), 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'sector': info.get('sector', 'N/A'),
#             'market_cap': info.get('marketCap'),
#             **sentiment
#         }
        
#         if user_profile['available_amount']:
#             response['shares_possible'] = int(user_profile['available_amount'] / current_price)
        
#         return jsonify(response)
        
#     except Exception as e:
#         logger.error(f"Analysis failed for {ticker}: {str(e)}")
#         return jsonify({
#             'error': 'Failed to analyze stock',
#             'details': str(e),
#             'ticker': ticker
#         }), 500

# # ... (rest of your endpoints remain the same)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# import pandas as pd
# import torch
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from datetime import datetime, timedelta
# import logging
# import time
# from sklearn.metrics import (
#     accuracy_score, precision_score, recall_score, 
#     f1_score, confusion_matrix, mean_absolute_error
# )

# app = Flask(__name__)
# CORS(app)

# # Configuration
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# SUPPORTED_TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "JPM", "NVDA", "WMT"]
# RISK_LEVELS = {
#     'low': ['JPM', 'WMT'],
#     'medium': ['AAPL', 'MSFT'],
#     'high': ['TSLA', 'NVDA']
# }

# # Initialize NLP model
# tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
# sentiment_model = AutoModelForSequenceClassification.from_pretrained(
#     "yiyanghkust/finbert-tone",
#     num_labels=3
# )

# # User profile
# user_profile = {
#     'available_amount': None,
#     'risk_preference': 'medium'
# }

# # Model performance tracking
# model_performance = {}

# class StockAnalyzer:
#     def __init__(self, ticker):
#         self.ticker = ticker
#         self.stock = yf.Ticker(ticker)
        
#     def fetch_data(self, max_retries=3):
#         for attempt in range(max_retries):
#             try:
#                 hist = self.stock.history(period="1mo", interval="1d")
#                 if not hist.empty:
#                     return hist
#             except Exception as e:
#                 logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
#                 time.sleep(1)
#         raise ValueError(f"Failed to fetch data for {self.ticker}")

#     def calculate_technical(self, hist):
#         hist['returns'] = hist['Close'].pct_change()
#         hist['sma_10'] = hist['Close'].rolling(10).mean()
#         hist['rsi'] = self._calculate_rsi(hist['Close'].values)
#         return hist.iloc[-1]

#     def _calculate_rsi(self, prices, window=14):
#         deltas = np.diff(prices)
#         seed = deltas[:window+1]
#         up = seed[seed >= 0].sum()/window
#         down = -seed[seed < 0].sum()/window
#         rs = up/down
#         rsi = np.zeros_like(prices)
#         rsi[:window] = 100. - 100./(1.+rs)
        
#         for i in range(window, len(prices)):
#             delta = deltas[i-1]
#             upval = delta if delta > 0 else 0.
#             downval = -delta if delta < 0 else 0.
#             up = (up*(window-1) + upval)/window
#             down = (down*(window-1) + downval)/window
#             rs = up/down
#             rsi[i] = 100. - 100./(1.+rs)
            
#         return rsi[-1]

#     def analyze_sentiment(self):
#         try:
#             news = getattr(self.stock, 'news', [])[:3]
#             if not news:
#                 return {
#                     'sentiment': 'neutral',
#                     'confidence': 0.5,
#                     'num_articles': 0
#                 }
                
#             sentiments = []
#             for article in news:
#                 if not article.get('title'):
#                     continue
#                 try:
#                     inputs = tokenizer(article['title'], return_tensors="pt", truncation=True)
#                     with torch.no_grad():
#                         outputs = sentiment_model(**inputs)
#                     probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
#                     sentiments.append(probs[0].numpy())
#                 except Exception as e:
#                     logger.warning(f"Failed to process article: {str(e)}")
            
#             if not sentiments:
#                 return {
#                     'sentiment': 'neutral',
#                     'confidence': 0.5,
#                     'num_articles': 0
#                 }
                
#             avg_sentiment = np.mean(sentiments, axis=0)
#             sentiment_labels = ['negative', 'neutral', 'positive']
#             dominant = sentiment_labels[np.argmax(avg_sentiment)]
#             return {
#                 'sentiment': dominant,
#                 'confidence': float(np.max(avg_sentiment)),
#                 'positive': float(avg_sentiment[2]),
#                 'neutral': float(avg_sentiment[1]),
#                 'negative': float(avg_sentiment[0]),
#                 'num_articles': len(sentiments)
#             }
#         except Exception as e:
#             logger.error(f"Sentiment analysis failed: {str(e)}")
#             return {
#                 'sentiment': 'neutral',
#                 'confidence': 0.5,
#                 'num_articles': 0
#             }

# class Backtester:
#     def __init__(self, ticker):
#         self.ticker = ticker
#         self.stock = yf.Ticker(ticker)
        
#     def run_backtest(self, years=1):
#         end_date = datetime.now()
#         start_date = end_date - timedelta(days=365*years)
#         hist = self.stock.history(start=start_date, end=end_date)
        
#         if hist.empty:
#             raise ValueError("No historical data available")
            
#         true_trends = []
#         pred_trends = []
#         prices = []
        
#         for i in range(10, len(hist)):
#             window = hist.iloc[i-10:i]
#             current = hist.iloc[i]
            
#             # Actual trend (next day)
#             true_trend = 1 if hist.iloc[i]['Close'] > hist.iloc[i-1]['Close'] else 0
#             true_trends.append(true_trend)
            
#             # Model prediction
#             sma_10 = window['Close'].rolling(10).mean().iloc[-1]
#             pred_trend = 1 if current['Close'] > sma_10 else 0
#             pred_trends.append(pred_trend)
            
#             prices.append(current['Close'])
        
#         # Calculate metrics
#         accuracy = accuracy_score(true_trends, pred_trends)
#         precision = precision_score(true_trends, pred_trends)
#         recall = recall_score(true_trends, pred_trends)
#         f1 = f1_score(true_trends, pred_trends)
        
#         returns = np.diff(prices) / prices[:-1]
#         directional_accuracy = np.mean((np.array(pred_trends[1:]) == np.sign(returns)).astype(int))
#         sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) != 0 else 0
        
#         return {
#             'classification_metrics': {
#                 'accuracy': accuracy,
#                 'precision': precision,
#                 'recall': recall,
#                 'f1': f1,
#                 'confusion_matrix': confusion_matrix(true_trends, pred_trends).tolist()
#             },
#             'financial_metrics': {
#                 'directional_accuracy': directional_accuracy,
#                 'sharpe_ratio': sharpe_ratio,
#                 'avg_return': np.mean(returns),
#                 'win_rate': np.mean(np.array(returns) > 0)
#             }
#         }

# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys())
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker or ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': 'Invalid ticker'}), 400
    
#     try:
#         analyzer = StockAnalyzer(ticker)
#         hist = analyzer.fetch_data()
#         latest = analyzer.calculate_technical(hist)
#         info = analyzer.stock.info
#         sentiment = analyzer.analyze_sentiment()
        
#         # Prediction
#         trend = "up" if latest['Close'] > latest['sma_10'] else "down"
#         confidence = min(0.95, max(0.05, 0.7 if trend == "up" else 0.3))
        
#         # Backtest results
#         backtester = Backtester(ticker)
#         performance = backtester.run_backtest(years=1)
        
#         response = {
#             'ticker': ticker,
#             'price': round(float(latest['Close']), 2),
#             'prediction': trend,
#             'confidence': confidence,
#             'sma_10': round(float(latest['sma_10']), 2),
#             'rsi': round(float(latest['rsi']), 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'sector': info.get('sector', 'N/A'),
#             'market_cap': info.get('marketCap'),
#             'sentiment': sentiment,
#             'performance_metrics': {
#                 'historical_accuracy': performance['classification_metrics']['accuracy'],
#                 'directional_accuracy': performance['financial_metrics']['directional_accuracy'],
#                 'sharpe_ratio': performance['financial_metrics']['sharpe_ratio'],
#                 'win_rate': performance['financial_metrics']['win_rate']
#             }
#         }
        
#         if user_profile['available_amount']:
#             response['shares_possible'] = int(user_profile['available_amount'] / latest['Close'])
        
#         return jsonify(response)
#     except Exception as e:
#         logger.error(f"Analysis failed: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/history', methods=['GET'])
# def get_history():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker or ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': 'Invalid ticker'}), 400
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period="1mo", interval="1d")
        
#         if hist.empty:
#             return jsonify({'error': 'No data available'}), 404
            
#         hist['sma_10'] = hist['Close'].rolling(10).mean()
#         data = []
        
#         for date, row in hist.iterrows():
#             data.append({
#                 'date': date.strftime('%Y-%m-%d'),
#                 'close': round(row['Close'], 2),
#                 'sma_10': round(row['sma_10'], 2) if not pd.isna(row['sma_10']) else None
#             })
        
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/performance/<ticker>', methods=['GET'])
# def get_performance(ticker):
#     try:
#         backtester = Backtester(ticker)
#         results = backtester.run_backtest(years=2)
#         return jsonify(results)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/profile', methods=['GET'])
# def get_profile():
#     return jsonify(user_profile)

# @app.route('/api/update_profile', methods=['POST'])
# def update_profile():
#     try:
#         data = request.get_json()
#         if 'amount' in data:
#             amount = float(data['amount'])
#             if amount <= 0:
#                 return jsonify({'error': 'Amount must be positive'}), 400
#             user_profile['available_amount'] = amount
            
#         if 'risk' in data:
#             if data['risk'] not in RISK_LEVELS:
#                 return jsonify({'error': 'Invalid risk level'}), 400
#             user_profile['risk_preference'] = data['risk']
            
#         return jsonify({'status': 'profile_updated'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)






# Initialize clients with API keys

# import json
# import time
# from bs4 import BeautifulSoup
# import re
# import requests
# from openai import OpenAI  # Correct import for v1.x
# from langchain_community.llms import OpenAI as LangchainOpenAI
# import yfinance as yf
# import warnings
# import os

# warnings.filterwarnings("ignore")
# OPENAI_API_KEY = "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"  # Replace with your actual key
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)

# # Initialize LangChain LLM
# llm = LangchainOpenAI(
#     temperature=0,
#     model_name="gpt-3.5-turbo-instruct",  # Changed to compatible model
#     openai_api_key=OPENAI_API_KEY
# )


# # Fetch stock data from Yahoo Finance
# def get_stock_price(ticker, history=5):
#     # time.sleep(4) #To avoid rate limit error
#     ticker = ticker  # No need to add ".NS" for U.S. stocks
#     stock = yf.Ticker(ticker)
#     df = stock.history(period="1y")
#     df = df[["Close", "Volume"]]
#     df.index = [str(x).split()[0] for x in list(df.index)]
#     df.index.rename("Date", inplace=True)
#     df = df[-history:]
#     return df.to_string()


# # Script to scrap top5 Google news for given company name
# def google_query(search_term):
#     if "news" not in search_term:
#         search_term = search_term + " stock news"
#     url = f"https://www.google.com/search?q={search_term}&cr=countryUS"
#     url = re.sub(r"\s", "+", url)
#     return url


# def get_recent_stock_news(company_name):
#     # time.sleep(4) #To avoid rate limit error
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

#     g_query = google_query(company_name)
#     res = requests.get(g_query, headers=headers).text
#     soup = BeautifulSoup(res, "html.parser")
#     news = []
#     for n in soup.find_all("div", "n0jPhd ynAwRc tNxQIb nDgy9d"):
#         news.append(n.text)
#     for n in soup.find_all("div", "IJl0Z"):
#         news.append(n.text)

#     if len(news) > 6:
#         news = news[:4]
#     else:
#         news = news
#     news_string = ""
#     for i, n in enumerate(news):
#         news_string += f"{i}. {n}\n"
#     top5_news = "Recent News:\n\n" + news_string

#     return top5_news


# # Fetch financial statements from Yahoo Finance
# def get_financial_statements(ticker):
#     # time.sleep(4) #To avoid rate limit error
#     ticker = ticker  # No need to add ".NS" for U.S. stocks
#     company = yf.Ticker(ticker)
#     balance_sheet = company.balance_sheet
#     if balance_sheet.shape[1] >= 3:
#         balance_sheet = balance_sheet.iloc[:, :3]    # Remove 4th year's data
#     balance_sheet = balance_sheet.dropna(how="any")
#     balance_sheet = balance_sheet.to_string()
#     return balance_sheet


# # Openai function calling
# function = [
#     {
#         "name": "get_company_Stock_ticker",
#         "description": "This will get the US stock ticker of the company",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "ticker_symbol": {
#                     "type": "string",
#                     "description": "This is the stock symbol of the company.",
#                 },

#                 "company_name": {
#                     "type": "string",
#                     "description": "This is the name of the company given in query",
#                 }
#             },
#             "required": ["company_name", "ticker_symbol"],
#         },
#     }
# ]


# def get_stock_ticker(query):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0,
#         messages=[{
#             "role": "user",
#             "content": f"Given the user request, what is the company name and the company stock ticker ?: {query}?"
#         }],
#         functions=function,
#         function_call={"name": "get_company_Stock_ticker"},
#     )
#     message = response["choices"][0]["message"]
#     arguments = json.loads(message["function_call"]["arguments"])
#     company_name = arguments["company_name"]
#     company_ticker = arguments["ticker_symbol"]
#     return company_name, company_ticker


# def analyze_stock(query):
#     # agent.run(query) Outputs Company name, Ticker
#     Company_name, ticker = get_stock_ticker(query)
#     print({"Query": query, "Company_name": Company_name, "Ticker": ticker})
#     stock_data = get_stock_price(ticker, history=10)
#     stock_financials = get_financial_statements(ticker)
#     stock_news = get_recent_stock_news(Company_name)

#     available_information = f"Stock Price: {stock_data}\n\nStock Financials: {stock_financials}\n\nStock News: {stock_news}"

#     # Run the analysis using the available data
#     analysis = llm(f"Give detailed stock analysis, Use the available data and provide an investment recommendation. \
#                  The user is fully aware of the investment risk, don’t include any kind of warning like 'It is recommended to conduct further research and analysis or consult with a financial advisor before making an investment decision' in the answer. \
#                  User question: {query} \
#                  You have the following information available about {Company_name}. Write (5-8) pointwise investment analysis to answer user query, At the end conclude with proper explanation. Try to give positives and negatives: \
#                   {available_information} ")

#     return analysis
# def main():
#     query = input("Enter a stock to analyze (e.g., 'Apple' or 'AAPL'): ")
#     analysis = analyze_stock(query)
#     print("\nStock Analysis:")
#     print(analysis)

# if __name__ == "__main__":
#     main()
















#NEMI
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime
# import logging

# app = Flask(__name__)
# CORS(app)

# # Configuration
# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker or ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': 'Invalid ticker'}), 400
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period="1mo")
#         info = stock.info
        
#         current_price = hist['Close'].iloc[-1]
#         open_price = hist['Open'].iloc[-1]
#         high_price = hist['High'].iloc[-1]
#         low_price = hist['Low'].iloc[-1]
#         previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
#         volume = hist['Volume'].iloc[-1]
        
#         sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
#         trend = "up" if current_price > sma_10 else "down"
        
#         price_change = (current_price - previous_close) / previous_close
#         volatility = (high_price - low_price) / open_price
        
#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change * 10))
#         confidence -= min(0.1, volatility * 0.5)
#         confidence = min(0.95, max(0.05, confidence))
        
#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'prediction': trend,
#             'confidence': round(confidence, 2),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'sector': SECTOR_MAP.get(ticker, 'other'),
#             'market_cap': info.get('marketCap'),
#             'beta': info.get('beta', 1.0)
#         }
        
#         if user_profile['available_amount'] > 0:
#             response['shares_possible'] = int(user_profile['available_amount'] / current_price)
        
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/recommend', methods=['GET'])
# def recommend_stocks():
#     try:
#         amount = float(request.args.get('amount', user_profile['available_amount']))
#         risk = request.args.get('risk', user_profile['risk_preference'])
        
#         if risk not in RISK_LEVELS:
#             return jsonify({'error': 'Invalid risk level'}), 400
            
#         recommendations = []
#         for ticker in RISK_LEVELS[risk]:
#             try:
#                 stock = yf.Ticker(ticker)
#                 hist = stock.history(period="1mo")
                
#                 current_price = hist['Close'].iloc[-1]
#                 shares = max(1, int((amount * 0.33) / current_price))
#                 previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
#                 sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
#                 price_change = (current_price - previous_close) / previous_close
#                 price_change_3d = (current_price - hist['Close'].iloc[-4]) / hist['Close'].iloc[-4] if len(hist) >= 4 else 0
                
#                 is_uptrend = current_price > sma_10
#                 is_recovering = price_change_3d > 0
                
#                 confidence = 0.5
#                 confidence += 0.3 if is_uptrend else (-0.1 if not is_recovering else 0.1)
#                 confidence += min(0.2, price_change_3d * 3)
#                 confidence = max(0.2, min(0.9, confidence))
                
#                 recommendations.append({
#                     'ticker': ticker,
#                     'price': round(current_price, 2),
#                     'shares': shares,
#                     'confidence': round(confidence, 2),
#                     'trend': 'up' if is_uptrend else ('recovering' if is_recovering else 'down'),  # Convert bool to string
#                     'change_1d': round(price_change * 100, 2),
#                     'change_3d': round(price_change_3d * 100, 2),
#                     'sector': SECTOR_MAP.get(ticker, 'other'),
#                     'is_uptrend': str(is_uptrend)  # Convert bool to string if needed
#                 })
#             except Exception as e:
#                 print(f"Error processing {ticker}: {str(e)}")
#                 continue
        
#         recommendations.sort(key=lambda x: x['confidence'], reverse=True)
#         top_picks = recommendations[:3]
        
#         if not top_picks:
#             return jsonify({
#                 'status': 'success',
#                 'recommendations': recommendations[:3],
#                 'allocation_plan': allocation
#             })
            
#         total_confidence = sum(x['confidence'] for x in top_picks)
#         allocation = []
#         for stock in top_picks:
#             weight = stock['confidence'] / total_confidence
#             allocated = round(amount * weight, 2)
#             shares = max(1, int(allocated / stock['price']))
#             allocation.append({
#                 'ticker': stock['ticker'],
#                 'amount': allocated,
#                 'shares': shares,
#                 'percentage': round(weight * 100, 1)
#             })
        
#         return jsonify({
#             'status': 'success',
#             'recommendations': top_picks,
#             'allocation_plan': allocation
#         })
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'message': 'Failed to generate recommendations'
#         }), 500

# @app.route('/api/update_profile', methods=['POST'])
# def update_profile():
#     try:
#         data = request.get_json()
#         user_profile['available_amount'] = float(data.get('amount', 5000.0))
#         user_profile['risk_preference'] = data.get('risk', 'medium')
#         return jsonify({'status': 'profile_updated'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)




# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# # Replace with your actual NewsAPI key.
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# # Mapping of common company names for natural language queries.
# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvda': 'NVDA',
#     'amd': 'AMD',
#     'jnj': 'JNJ',
#     'pfe': 'PFE',
#     'jpm': 'JPM',
#     'gs': 'GS',
#     'ko': 'KO',
#     'pep': 'PEP',
#     'xom': 'XOM',
#     'nee': 'NEE',
#     'cvx': 'CVX',
#     'wmt': 'WMT',
#     'hd': 'HD',
#     'gme': 'GME',
#     'tsla': 'TSLA',
#     'f': 'F',
#     'coin': 'COIN',
#     'mrna': 'MRNA'
# }

# def extract_company_and_ticker(query):
#     """
#     If the query exactly matches a supported ticker (case-insensitive), return it.
#     Otherwise, search for any supported company name.
#     """
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # News Fetching Functions
# # ---------------------------
# def google_query(search_term):
#     """
#     Construct a Google news search URL (using tbm=nws).
#     """
#     if "news" not in search_term.lower():
#         search_term += " stock news"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws"
#     return re.sub(r"\s", "+", url)

# def google_scrape_news(company_name):
#     """
#     Fallback method: Scrape headlines from Google News search results.
#     Tries multiple selectors to capture headlines.
#     """
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         html = response.text
#     except Exception as e:
#         app.logger.error(f"Error fetching news from Google: {e}")
#         return [], "Recent News:\nNo news available."
    
#     soup = BeautifulSoup(html, "html.parser")
#     headlines = []
#     # Primary selector
#     for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
#         headline = tag.get_text().strip()
#         if headline and headline not in headlines:
#             headlines.append(headline)
#     # Fallback selectors
#     if not headlines:
#         for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if len(headlines) > 4:
#         headlines = headlines[:4]
#     news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# def get_news_from_newsapi(company_name):
#     """
#     Use NewsAPI to fetch recent news headlines.
#     """
#     if not NEWSAPI_KEY:
#         app.logger.error("NEWSAPI_KEY is not provided.")
#         return [], ""
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": company_name + " stock",
#         "sortBy": "publishedAt",
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 4
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
#         if headlines:
#             news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#             return headlines, news_string
#     except Exception as e:
#         app.logger.error(f"NewsAPI error: {e}")
#     return [], ""

# def get_recent_stock_news(company_name, ticker):
#     """
#     Attempt to fetch news using yfinance’s built‑in news first.
#     If none are returned, then try NewsAPI and fall back to Google scraping.
#     """
#     stock = yf.Ticker(ticker)
#     try:
#         news_items = stock.news
#     except Exception:
#         news_items = []
#     headlines = []
#     if news_items:
#         for item in news_items:
#             if "title" in item and item["title"]:
#                 headlines.append(item["title"])
#     if not headlines:
#         headlines, news_string = get_news_from_newsapi(company_name)
#         if not headlines:
#             headlines, news_string = google_scrape_news(company_name)
#     else:
#         news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# # ---------------------------
# # FinBERT-based Sentiment Analysis
# # ---------------------------
# from transformers import pipeline
# finbert = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

# def analyze_news_sentiment(news_list):
#     """
#     Use FinBERT to analyze each headline.
#     Returns a list of sentiment dictionaries.
#     """
#     sentiments = []
#     for headline in news_list:
#         try:
#             result = finbert(headline)[0]
#             sentiments.append(result)
#         except Exception:
#             sentiments.append({"label": "Neutral", "score": 0.0})
#     return sentiments

# def aggregate_sentiments(sentiments):
#     """
#     Aggregates individual sentiment scores to produce an overall sentiment.
#     """
#     if not sentiments:
#         return "Neutral"
#     positive = sum(s['score'] for s in sentiments if s['label'].lower() == 'positive')
#     negative = sum(s['score'] for s in sentiments if s['label'].lower() == 'negative')
#     neutral = sum(s['score'] for s in sentiments if s['label'].lower() == 'neutral')
#     total = positive + negative + neutral
#     pos_pct = positive / total if total > 0 else 0
#     neg_pct = negative / total if total > 0 else 0
#     if pos_pct > neg_pct:
#         return "Positive"
#     elif neg_pct > pos_pct:
#         return "Negative"
#     else:
#         return "Neutral"

# # ---------------------------
# # API Endpoints
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     # First try to get ticker from "ticker" parameter.
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         company, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; no supported company name found. Try one of: ' + ", ".join(SUPPORTED_TICKERS)}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}". Try: ' + ", ".join(SUPPORTED_TICKERS)}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period="1mo")
#         info = stock.info

#         current_price = hist['Close'].iloc[-1]
#         open_price = hist['Open'].iloc[-1]
#         high_price = hist['High'].iloc[-1]
#         low_price = hist['Low'].iloc[-1]
#         previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
#         volume = hist['Volume'].iloc[-1]

#         sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
#         trend = "up" if current_price > sma_10 else "down"
#         price_change = (current_price - previous_close) / previous_close
#         volatility = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change * 10))
#         confidence -= min(0.1, volatility * 0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name = info.get('shortName', ticker)
#         news_list, news_string = get_recent_stock_news(company_name, ticker)
#         sentiments = analyze_news_sentiment(news_list)
#         overall_sentiment = aggregate_sentiments(sentiments)

#         # Rule-based decision
#         if trend == "up" and overall_sentiment == "Positive":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "Negative":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         # ---- Added Detailed Technical Explanation ----
#         detailed_explanation = "\n\n📊 Detailed Technical Explanation:\n"
#         detailed_explanation += f"🔸 10-Day SMA: ${sma_10:.2f}. This is the average closing price over the last 10 days. "
#         if current_price < sma_10:
#             detailed_explanation += f"Since the current price (${current_price:.2f}) is below the SMA, it indicates a DOWN trend.\n"
#         else:
#             detailed_explanation += f"Since the current price (${current_price:.2f}) is above the SMA, it indicates an UP trend.\n"
#         pe_ratio = info.get('trailingPE', 'N/A')
#         detailed_explanation += f"🔸 PE Ratio: {pe_ratio}. The PE ratio typically ranges between 15 and 30 for mature companies. A value in this range suggests moderate valuation.\n"
#         dividend_yield = info.get('dividendYield', 0)
#         detailed_explanation += f"🔸 Dividend Yield: {(dividend_yield * 100):.2f}%. Normally, dividend yields are below 5%; an unusually high yield may indicate potential red flags.\n"
#         detailed_explanation += f"🔸 Price Change: {price_change*100:.2f}%. This is the percentage change from the previous close. "
#         if price_change < 0:
#             detailed_explanation += "A negative value indicates a recent price decline.\n"
#         else:
#             detailed_explanation += "A positive value indicates an increase in price.\n"
#         detailed_explanation += f"🔸 Volatility: {volatility*100:.2f}%. This measures how much the stock price fluctuates during the trading day; higher volatility means larger price swings.\n"
#         # ---- End of Detailed Explanation ----

#         analysis = (
#             f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} with a {trend.upper()} trend "
#             f"and a technical confidence score of {confidence:.2f}. The 10-Day SMA is ${sma_10:.2f}, with a price change of {price_change*100:.2f}% "
#             f"and volatility of {volatility*100:.2f}%. Recent news sentiment is {overall_sentiment}. With an investment amount of ${amount:.2f}, "
#             f"you could purchase up to {shares_possible} shares. Overall, the recommendation is to {decision}. Please consider your risk tolerance before making any decision."
#         )
#         analysis += detailed_explanation

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': pe_ratio,
#             'dividend_yield': dividend_yield,
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'analysis': analysis
#         }
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/recommend', methods=['GET'])
# def recommend_stocks():
#     try:
#         amount = float(request.args.get('amount', user_profile['available_amount']))
#         risk = request.args.get('risk', user_profile['risk_preference'])
#         if risk not in RISK_LEVELS:
#             return jsonify({'error': 'Invalid risk level'}), 400

#         candidates = []
#         for ticker in RISK_LEVELS[risk]:
#             try:
#                 stock = yf.Ticker(ticker)
#                 hist = stock.history(period="1mo")
#                 current_price = hist['Close'].iloc[-1]
#                 previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
#                 sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
#                 price_change = (current_price - previous_close) / previous_close
#                 price_change_3d = (current_price - hist['Close'].iloc[-4]) / hist['Close'].iloc[-4] if len(hist) >= 4 else 0
#                 is_uptrend = current_price > sma_10
#                 is_recovering = price_change_3d > 0

#                 confidence = 0.5
#                 if is_uptrend:
#                     confidence += 0.3
#                 elif not is_recovering:
#                     confidence -= 0.1
#                 else:
#                     confidence += 0.1
#                 confidence += min(0.2, price_change_3d * 3)
#                 confidence = max(0.2, min(0.9, confidence))
                
#                 candidates.append({
#                     'ticker': ticker,
#                     'price': round(current_price, 2),
#                     'confidence': confidence,
#                     'trend': 'up' if is_uptrend else ('recovering' if is_recovering else 'down'),
#                     'sector': SECTOR_MAP.get(ticker, 'other')
#                 })
#             except Exception as e:
#                 app.logger.error(f"Error processing {ticker}: {str(e)}")
#                 continue

#         candidates.sort(key=lambda x: x['confidence'], reverse=True)
#         top_picks = candidates[:3]
#         if not top_picks:
#             return jsonify({
#                 'status': 'success',
#                 'recommendations': [],
#                 'allocation_plan': []
#             })

#         total_confidence = sum(x['confidence'] for x in top_picks)
#         allocation = []
#         for stock in top_picks:
#             weight = stock['confidence'] / total_confidence
#             allocated = round(amount * weight, 2)
#             shares = max(1, int(allocated / stock['price']))
#             allocation.append({
#                 'ticker': stock['ticker'],
#                 'amount': allocated,
#                 'shares': shares,
#                 'percentage': round(weight * 100, 1)
#             })
#             stock['shares'] = shares

#         return jsonify({
#             'status': 'success',
#             'recommendations': top_picks,
#             'allocation_plan': allocation
#         })
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'message': 'Failed to generate recommendations'
#         }), 500

# @app.route('/api/update_profile', methods=['POST'])
# def update_profile():
#     try:
#         data = request.get_json()
#         user_profile['available_amount'] = float(data.get('amount', 5000.0))
#         user_profile['risk_preference'] = data.get('risk', 'medium')
#         return jsonify({'status': 'profile_updated'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)

# import os
# import requests
# from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import nltk
# import logging
# from dotenv import load_dotenv
# import yfinance as yf

# # Initialize
# load_dotenv()
# nltk.download('vader_lexicon')
# app = Flask(__name__)
# CORS(app)
# logging.basicConfig(level=logging.INFO)

# # Configuration
# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvidia': 'NVDA',
#     'amd': 'AMD',
#     'johnson & johnson': 'JNJ',
#     'jnj': 'JNJ',
#     'pfizer': 'PFE',
#     'pfe': 'PFE',
#     'jpmorgan': 'JPM',
#     'jpm': 'JPM',
#     'goldman sachs': 'GS',
#     'gs': 'GS',
#     'coca cola': 'KO',
#     'ko': 'KO',
#     'pepsi': 'PEP',
#     'pep': 'PEP',
#     'exxon': 'XOM',
#     'xom': 'XOM',
#     'next era energy': 'NEE',
#     'nee': 'NEE',
#     'chevron': 'CVX',
#     'cvx': 'CVX',
#     'walmart': 'WMT',
#     'wmt': 'WMT',
#     'home depot': 'HD',
#     'hd': 'HD',
#     'gamestop': 'GME',
#     'gme': 'GME',
#     'tesla': 'TSLA',
#     'tsla': 'TSLA',
#     'ford': 'F',
#     'f': 'F',
#     'coinbase': 'COIN',
#     'coin': 'COIN',
#     'moderna': 'MRNA',
#     'mrna': 'MRNA'
# }

# # Load models
# finbert = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")
# roberta = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()
# gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")

# # def fetch_news(ticker):
# #     """Fetch news using NewsAPI with proper error handling"""
# #     NEWS_API_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Your actual key
    
# #     if not NEWS_API_KEY:
# #         raise ValueError("NewsAPI key not configured")
    
# #     company_name = next((k for k, v in COMPANY_NAME_TO_TICKER.items() if v == ticker), ticker)
# #     url = f"https://newsapi.org/v2/everything?q={company_name}+stock&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    
# #     try:
# #         response = requests.get(url, timeout=10)
# #         data = response.json()
        
# #         if data['status'] != 'ok':
# #             raise ValueError(data.get('message', 'NewsAPI error'))
        
# #         return [
# #             (article['title'], article['source']['name'])
# #             for article in data['articles']
# #         ]
# #     except Exception as e:
# #         logging.error(f"News fetch failed: {str(e)}")
# #         raise ValueError(f"Could not fetch news: {str(e)}")

# def fetch_news(ticker):
#     """Fetch stock-related news with ticker symbol directly for better relevance."""
#     NEWS_API_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Your actual key
    
#     if not NEWS_API_KEY:
#         raise ValueError("NewsAPI key not configured")
    
#     # Directly use the stock ticker symbol in the query and broaden the search
#     query = f"{ticker} stock news"  # Simplified query
#     url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    
#     try:
#         response = requests.get(url, timeout=10)
#         data = response.json()

#         # Check if the response is successful
#         if data['status'] != 'ok':
#             raise ValueError(data.get('message', 'NewsAPI error'))

#         # If no articles, log it
#         if not data['articles']:
#             logging.warning(f"No articles found for ticker {ticker}.")
        
#         # Return the fetched articles (with more relevant stock-related titles)
#         return [
#             (article['title'], article['source']['name'], article['description'], article['url'])
#             for article in data['articles']
#             if 'stock' in article['title'].lower() or 'earnings' in article['title'].lower()
#         ]
    
#     except Exception as e:
#         logging.error(f"News fetch failed: {str(e)}")
#         raise ValueError(f"Could not fetch news: {str(e)}")

# # EVERYTHING BELOW THIS LINE REMAINS EXACTLY THE SAME >>>>>>>>>>>>>>>>>>>>>>>>>>
# def get_stock_data(ticker):
#     """Get current stock price using yfinance"""
#     stock = yf.Ticker(ticker)
#     data = stock.history(period='1d')
#     if data.empty:
#         return None
#     return {
#         'current_price': round(data['Close'].iloc[-1], 2),
#         'change': round(data['Close'].iloc[-1] - data['Open'].iloc[-1], 2),
#         'change_percent': round(((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100, 2)
#     }

# def analyze_sentiment(text):
#     """Fixed-weight ensemble sentiment analysis"""
#     # Get predictions
#     finbert_result = finbert(text)[0]
#     roberta_result = roberta(text)[0]
#     vader_score = vader.polarity_scores(text)['compound']
    
#     # Convert to common scale (-1 to 1)
#     finbert_score = 1 if finbert_result['label'] == 'Positive' else -1 if finbert_result['label'] == 'Negative' else 0
#     roberta_score = (roberta_result['score'] if roberta_result['label'] == 'POS' else 
#                     -roberta_result['score'] if roberta_result['label'] == 'NEG' else 0)
    
#     # Fixed weights (calibrated for stability)
#     weighted_score = (0.6 * finbert_score) + (0.3 * roberta_score) + (0.1 * vader_score)
    
#     # Classify with hysteresis to reduce fluctuation
#     if weighted_score > 0.35: return 'Positive', weighted_score
#     if weighted_score < -0.35: return 'Negative', weighted_score
#     return 'Neutral', weighted_score

# def generate_analysis(ticker, news_items, overall_sentiment):
#     """Generate GPT-2 powered analysis"""
#     prompt = f"Analyze {ticker} stock sentiment based on these news headlines:\n"
#     prompt += "\n".join([f"- {headline}" for headline, _ in news_items])
#     prompt += f"\n\nOverall sentiment is {overall_sentiment}. Provide concise investment advice:"
    
#     inputs = gpt2_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
#     outputs = gpt2_model.generate(
#         **inputs,
#         max_length=200,
#         num_return_sequences=1,
#         temperature=0.7,
#         do_sample=True
#     )
    
#     return gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)

# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     """List supported tickers"""
#     return jsonify({
#         "tickers": SUPPORTED_TICKERS,
#         "mappings": COMPANY_NAME_TO_TICKER
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     """Main analysis endpoint"""
#     ticker_or_name = request.args.get('stock', '').upper()
    
#     # Resolve input to ticker
#     ticker = None
#     if ticker_or_name in SUPPORTED_TICKERS:
#         ticker = ticker_or_name
#     elif ticker_or_name.lower() in COMPANY_NAME_TO_TICKER:
#         ticker = COMPANY_NAME_TO_TICKER[ticker_or_name.lower()]
    
#     if not ticker:
#         return jsonify({"error": "Unsupported stock"}), 400
    
#     try:
#         # Fetch all data
#         news_items = fetch_news(ticker)
#         stock_data = get_stock_data(ticker)
        
#         # Analyze sentiment
#         analyzed_news = []
#         sentiment_scores = []
        
#         for headline, source in news_items:
#             sentiment, score = analyze_sentiment(headline)
#             analyzed_news.append({
#                 "headline": headline,
#                 "source": source,
#                 "sentiment": sentiment,
#                 "score": round(score, 2)
#             })
#             sentiment_scores.append(score)
        
#         # Calculate overall
#         avg_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
#         overall_sentiment = "Positive" if avg_score > 0.35 else "Negative" if avg_score < -0.35 else "Neutral"
        
#         # Generate GPT-2 analysis
#         gpt_analysis = generate_analysis(ticker, news_items, overall_sentiment)
        
#         return jsonify({
#             "ticker": ticker,
#             "news": analyzed_news,
#             "stock_data": stock_data,
#             "overall_sentiment": overall_sentiment,
#             "average_score": round(avg_score, 2),
#             "analysis": gpt_analysis
#         })
        
#     except Exception as e:
#         logging.error(f"Analysis failed: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)

# import os
# import requests
# from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import nltk
# import logging
# from dotenv import load_dotenv
# import yfinance as yf

# # Initialize
# load_dotenv()
# nltk.download('vader_lexicon')
# app = Flask(__name__)
# CORS(app)
# logging.basicConfig(level=logging.INFO)

# # Configuration
# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvidia': 'NVDA',
#     'amd': 'AMD',
#     'johnson & johnson': 'JNJ',
#     'jnj': 'JNJ',
#     'pfizer': 'PFE',
#     'pfe': 'PFE',
#     'jpmorgan': 'JPM',
#     'jpm': 'JPM',
#     'goldman sachs': 'GS',
#     'gs': 'GS',
#     'coca cola': 'KO',
#     'ko': 'KO',
#     'pepsi': 'PEP',
#     'pep': 'PEP',
#     'exxon': 'XOM',
#     'xom': 'XOM',
#     'next era energy': 'NEE',
#     'nee': 'NEE',
#     'chevron': 'CVX',
#     'cvx': 'CVX',
#     'walmart': 'WMT',
#     'wmt': 'WMT',
#     'home depot': 'HD',
#     'hd': 'HD',
#     'gamestop': 'GME',
#     'gme': 'GME',
#     'tesla': 'TSLA',
#     'tsla': 'TSLA',
#     'ford': 'F',
#     'f': 'F',
#     'coinbase': 'COIN',
#     'coin': 'COIN',
#     'moderna': 'MRNA',
#     'mrna': 'MRNA'
# }

# # Load models
# finbert = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")
# roberta = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()
# gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")

# # Fetch stock-related news with ticker symbol directly for better relevance
# def fetch_news(ticker):
#     """Fetch stock-related news with ticker symbol directly for better relevance."""
#     NEWS_API_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Your actual key
    
#     if not NEWS_API_KEY:
#         raise ValueError("NewsAPI key not configured")
    
#     # Directly use the stock ticker symbol in the query and broaden the search
#     query = f"{ticker} stock news"  # Simplified query
#     url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    
#     try:
#         response = requests.get(url, timeout=10)
#         data = response.json()

#         # Check if the response is successful
#         if data['status'] != 'ok':
#             raise ValueError(data.get('message', 'NewsAPI error'))

#         # If no articles, log it
#         if not data['articles']:
#             logging.warning(f"No articles found for ticker {ticker}.")
        
#         # Return the fetched articles (with more relevant stock-related titles)
#         return [
#             (article['title'], article['source']['name'], article['description'], article['url'])
#             for article in data['articles']
#             if 'stock' in article['title'].lower() or 'earnings' in article['title'].lower()
#         ]
    
#     except Exception as e:
#         logging.error(f"News fetch failed: {str(e)}")
#         raise ValueError(f"Could not fetch news: {str(e)}")

# # Get stock data using yfinance
# def get_stock_data(ticker):
#     """Get current stock price using yfinance"""
#     stock = yf.Ticker(ticker)
#     data = stock.history(period='1d')
#     if data.empty:
#         return None
#     return {
#         'current_price': round(data['Close'].iloc[-1], 2),
#         'change': round(data['Close'].iloc[-1] - data['Open'].iloc[-1], 2),
#         'change_percent': round(((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100, 2)
#     }

# # Sentiment analysis using multiple models
# def analyze_sentiment(text):
#     """Fixed-weight ensemble sentiment analysis"""
#     # Get predictions
#     finbert_result = finbert(text)[0]
#     roberta_result = roberta(text)[0]
#     vader_score = vader.polarity_scores(text)['compound']
    
#     # Convert to common scale (-1 to 1)
#     finbert_score = 1 if finbert_result['label'] == 'Positive' else -1 if finbert_result['label'] == 'Negative' else 0
#     roberta_score = (roberta_result['score'] if roberta_result['label'] == 'POS' else 
#                     -roberta_result['score'] if roberta_result['label'] == 'NEG' else 0)
    
#     # Fixed weights (calibrated for stability)
#     weighted_score = (0.6 * finbert_score) + (0.3 * roberta_score) + (0.1 * vader_score)
    
#     # Classify with hysteresis to reduce fluctuation
#     if weighted_score > 0.35: return 'Positive', weighted_score
#     if weighted_score < -0.35: return 'Negative', weighted_score
#     return 'Neutral', weighted_score

# # GPT-2 model powered analysis generation
# def generate_analysis(ticker, news_items, overall_sentiment):
#     """Generate GPT-2 powered analysis"""
#     prompt = f"Analyze {ticker} stock sentiment based on these news headlines:\n"
#     prompt += "\n".join([f"- {headline}" for headline, _ in news_items])
#     prompt += f"\n\nOverall sentiment is {overall_sentiment}. Provide concise investment advice:"
    
#     inputs = gpt2_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
#     outputs = gpt2_model.generate(
#         **inputs,
#         max_length=200,
#         num_return_sequences=1,
#         temperature=0.7,
#         do_sample=True
#     )
    
#     return gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)

# # Endpoint to fetch supported tickers
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     """List supported tickers"""
#     return jsonify({
#         "tickers": SUPPORTED_TICKERS,
#         "mappings": COMPANY_NAME_TO_TICKER
#     })

# # Main analysis endpoint
# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     """Main analysis endpoint"""
#     ticker_or_name = request.args.get('stock', '').upper()
    
#     # Resolve input to ticker
#     ticker = None
#     if ticker_or_name in SUPPORTED_TICKERS:
#         ticker = ticker_or_name
#     elif ticker_or_name.lower() in COMPANY_NAME_TO_TICKER:
#         ticker = COMPANY_NAME_TO_TICKER[ticker_or_name.lower()]
    
#     if not ticker:
#         return jsonify({"error": "Unsupported stock"}), 400
    
#     try:
#         # Fetch all data
#         news_items = fetch_news(ticker)
#         stock_data = get_stock_data(ticker)
        
#         # Analyze sentiment
#         analyzed_news = []
#         sentiment_scores = []
        
#         for headline, source, description, url in news_items:
#             sentiment, score = analyze_sentiment(headline)  # Correct unpacking here
#             analyzed_news.append({
#                 "headline": headline,
#                 "source": source,
#                 "sentiment": sentiment,
#                 "score": round(score, 2),
#                 "description": description,
#                 "url": url  # Add URL to the response
#             })
#             sentiment_scores.append(score)
        
#         # Calculate overall
#         avg_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
#         overall_sentiment = "Positive" if avg_score > 0.35 else "Negative" if avg_score < -0.35 else "Neutral"
        
#         # Generate GPT-2 analysis
#         gpt_analysis = generate_analysis(ticker, news_items, overall_sentiment)
        
#         return jsonify({
#             "ticker": ticker,
#             "news": analyzed_news,
#             "stock_data": stock_data,
#             "overall_sentiment": overall_sentiment,
#             "average_score": round(avg_score, 2),
#             "analysis": gpt_analysis
#         })
        
#     except Exception as e:
#         logging.error(f"Analysis failed: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)










# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup
# import nltk
# nltk.download('vader_lexicon')

# # ─────────────────────────────────────────────────────────────────────────────
# # New imports for ensemble sentiment (from Code B)
# from transformers import pipeline as _hf_pipeline
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # ─────────────────────────────────────────────────────────────────────────────

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key.

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvda': 'NVDA',
#     'amd': 'AMD',
#     'jnj': 'JNJ',
#     'pfe': 'PFE',
#     'jpm': 'JPM',
#     'gs': 'GS',
#     'ko': 'KO',
#     'pep': 'PEP',
#     'xom': 'XOM',
#     'nee': 'NEE',
#     'cvx': 'CVX',
#     'wmt': 'WMT',
#     'hd': 'HD',
#     'gme': 'GME',
#     'tsla': 'TSLA',
#     'f': 'F',
#     'coin': 'COIN',
#     'mrna': 'MRNA'
# }

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # Financial Statement Functions
# # ---------------------------
# def get_financial_statements(ticker):
#     """Fetch the financial statements for a given US ticker symbol."""
#     try:
#         company = yf.Ticker(ticker)
        
#         balance_sheet = company.balance_sheet
#         income_statement = company.financials
#         cashflow_statement = company.cashflow
        
#         # Clean and format the data
#         if balance_sheet.shape[1] >= 3:
#             balance_sheet = balance_sheet.iloc[:, :3]  # Keep first 3 years
#         balance_sheet = balance_sheet.dropna(how="any")  # Drop rows with NaN values

#         # Convert the data to strings for easy display
#         balance_sheet_str = balance_sheet.to_string()
#         income_statement_str = income_statement.to_string()
#         cashflow_statement_str = cashflow_statement.to_string()

#         return {
#             "balance_sheet": balance_sheet_str,
#             "income_statement": income_statement_str,
#             "cashflow_statement": cashflow_statement_str
#         }
#     except Exception as e:
#         logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
#         return {
#             "balance_sheet": "Error fetching balance sheet.",
#             "income_statement": "Error fetching income statement.",
#             "cashflow_statement": "Error fetching cash flow statement."
#         }

# # ---------------------------
# # News Fetching Functions
# # ---------------------------
# def google_query(search_term):
#     if "news" not in search_term.lower():
#         search_term += " stock news"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws"
#     return re.sub(r"\s", "+", url)

# def google_scrape_news(company_name):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         html = response.text
#     except Exception as e:
#         app.logger.error(f"Error fetching news from Google: {e}")
#         return [], "Recent News:\nNo news available."
    
#     soup = BeautifulSoup(html, "html.parser")
#     headlines = []
#     for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
#         headline = tag.get_text().strip()
#         if headline and headline not in headlines:
#             headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if len(headlines) > 4:
#         headlines = headlines[:4]
#     news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# def get_news_from_newsapi(company_name):
#     if not NEWSAPI_KEY:
#         app.logger.error("NEWSAPI_KEY is not provided.")
#         return [], ""
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": company_name + " stock",
#         "sortBy": "publishedAt",
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 4
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
#         if headlines:
#             news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#             return headlines, news_string
#     except Exception as e:
#         app.logger.error(f"NewsAPI error: {e}")
#     return [], ""

# def get_recent_stock_news(company_name, ticker):
#     stock = yf.Ticker(ticker)
#     try:
#         news_items = stock.news
#     except Exception:
#         news_items = []
#     headlines = []
#     if news_items:
#         for item in news_items:
#             if "title" in item and item["title"]:
#                 headlines.append(item["title"])
#     if not headlines:
#         headlines, news_string = get_news_from_newsapi(company_name)
#         if not headlines:
#             headlines, news_string = google_scrape_news(company_name)
#     else:
#         news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# # ---------------------------
# # FinBERT-based Sentiment Analysis (original)
# # ---------------------------
# from transformers import pipeline
# finbert = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

# def analyze_news_sentiment(news_list):
#     sentiments = []
#     for headline in news_list:
#         try:
#             result = finbert(headline)[0]
#             sentiments.append(result)
#         except Exception:
#             sentiments.append({"label": "Neutral", "score": 0.0})
#     return sentiments

# def aggregate_sentiments(sentiments):
#     if not sentiments:
#         return "Neutral"
#     positive = sum(s['score'] for s in sentiments if s['label'].lower() == 'positive')
#     negative = sum(s['score'] for s in sentiments if s['label'].lower() == 'negative')
#     neutral = sum(s['score'] for s in sentiments if s['label'].lower() == 'neutral')
#     total = positive + negative + neutral
#     pos_pct = positive / total if total > 0 else 0
#     neg_pct = negative / total if total > 0 else 0
#     if pos_pct > neg_pct:
#         return "Positive"
#     elif neg_pct > pos_pct:
#         return "Negative"
#     else:
#         return "Neutral"

# # ─────────────────────────────────────────────────────────────────────────────
# # Ensemble sentiment function copied **verbatim** from Code B:
# # ─────────────────────────────────────────────────────────────────────────────
# roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()

# def analyze_sentiment(text):
#     """Fixed-weight ensemble sentiment analysis from Code B."""
#     finbert_result  = finbert(text)[0]
#     roberta_result  = roberta(text)[0]
#     vader_score     = vader.polarity_scores(text)['compound']

#     # map labels to -1/0/+1
#     finbert_score  =  1 if finbert_result['label'] == 'Positive' \
#                     else -1 if finbert_result['label'] == 'Negative' \
#                     else 0
#     roberta_score  =  roberta_result['score'] if roberta_result['label'] == 'POS' \
#                     else -roberta_result['score'] if roberta_result['label'] == 'NEG' \
#                     else 0

#     weighted_score = (0.6 * finbert_score) + (0.3 * roberta_score) + (0.1 * vader_score)

#     if weighted_score > 0.35:
#         label = 'Positive'
#     elif weighted_score < -0.35:
#         label = 'Negative'
#     else:
#         label = 'Neutral'

#     return label, weighted_score
# # ─────────────────────────────────────────────────────────────────────────────

# def extract_company_and_ticker(query):
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# # ---------------------------
# # API Endpoints
# # ---------------------------

# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         _, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; ...'}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}". ...'}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist  = stock.history(period="1mo")
#         info  = stock.info

#         current_price   = hist['Close'].iloc[-1]
#         open_price      = hist['Open'].iloc[-1]
#         high_price      = hist['High'].iloc[-1]
#         low_price       = hist['Low'].iloc[-1]
#         previous_close  = hist['Close'].iloc[-2] if len(hist)>1 else current_price
#         volume          = hist['Volume'].iloc[-1]

#         sma_10          = hist['Close'].rolling(10).mean().iloc[-1]
#         trend           = "up" if current_price > sma_10 else "down"
#         price_change    = (current_price - previous_close) / previous_close
#         volatility      = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change*10))
#         confidence -= min(0.1, volatility*0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name, _ = extract_company_and_ticker(ticker)
#         news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)

#         # original FinBERT-only sentiments
#         sentiments = analyze_news_sentiment(news_list)
#         overall_sentiment = aggregate_sentiments(sentiments)

#         # ─────────────── New: ensemble sentiment scores ───────────────
#         detailed_sentiments = []
#         for hl in news_list:
#             label, score = analyze_sentiment(hl)
#             detailed_sentiments.append({
#                 'headline': hl,
#                 'label': label,
#                 'score': round(score, 2)
#             })
#         # ────────────────────────────────────────────────────────────────

#         # Fetch financial statement sentiment
#         financial_sentiment_data = get_financial_statements(ticker)
#         financial_sentiment = "Neutral"  # Example placeholder for sentiment
#         financial_statements_content = financial_sentiment_data.get("balance_sheet", "No content available")

#         # Rule-based decision
#         if trend == "up" and overall_sentiment == "Positive":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "Negative":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         analysis = (
#             f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} ..."
#         )

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'detailed_sentiments': detailed_sentiments,
#             'financial_statements_sentiment': financial_sentiment,
#             'financial_statements_content': financial_statements_content,
#             'analysis': analysis
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/recommend', methods=['GET'])
# def recommend_stocks():
#     try:
#         amount = float(request.args.get('amount', user_profile['available_amount']))
#         risk = request.args.get('risk', user_profile['risk_preference'])
#         if risk not in RISK_LEVELS:
#             return jsonify({'error': 'Invalid risk level'}), 400

#         candidates = []
#         for ticker in RISK_LEVELS[risk]:
#             try:
#                 stock = yf.Ticker(ticker)
#                 hist = stock.history(period="1mo")
#                 current_price = hist['Close'].iloc[-1]
#                 previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
#                 sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
#                 price_change = (current_price - previous_close) / previous_close
#                 price_change_3d = (current_price - hist['Close'].iloc[-4]) / hist['Close'].iloc[-4] if len(hist) >= 4 else 0
#                 is_uptrend = current_price > sma_10
#                 is_recovering = price_change_3d > 0

#                 confidence = 0.5
#                 if is_uptrend:
#                     confidence += 0.3
#                 elif not is_recovering:
#                     confidence -= 0.1
#                 else:
#                     confidence += 0.1
#                 confidence += min(0.2, price_change_3d * 3)
#                 confidence = max(0.2, min(0.9, confidence))
                
#                 candidates.append({
#                     'ticker': ticker,
#                     'price': round(current_price, 2),
#                     'confidence': confidence,
#                     'trend': 'up' if is_uptrend else ('recovering' if is_recovering else 'down'),
#                     'sector': SECTOR_MAP.get(ticker, 'other')
#                 })
#             except Exception as e:
#                 app.logger.error(f"Error processing {ticker}: {str(e)}")
#                 continue

#         candidates.sort(key=lambda x: x['confidence'], reverse=True)
#         top_picks = candidates[:3]
#         if not top_picks:
#             return jsonify({
#                 'status': 'success',
#                 'recommendations': [],
#                 'allocation_plan': []
#             })

#         total_confidence = sum(x['confidence'] for x in top_picks)
#         allocation = []
#         for stock in top_picks:
#             weight = stock['confidence'] / total_confidence
#             allocated = round(amount * weight, 2)
#             shares = max(1, int(allocated / stock['price']))
#             allocation.append({
#                 'ticker': stock['ticker'],
#                 'amount': allocated,
#                 'shares': shares,
#                 'percentage': round(weight * 100, 1)
#             })
#             stock['shares'] = shares

#         return jsonify({
#             'status': 'success',
#             'recommendations': top_picks,
#             'allocation_plan': allocation
#         })
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'message': 'Failed to generate recommendations'
#         }), 500

# @app.route('/api/update_profile', methods=['POST'])
# def update_profile():
#     try:
#         data = request.get_json()
#         user_profile['available_amount'] = float(data.get('amount', 5000.0))
#         user_profile['risk_preference'] = data.get('risk', 'medium')
#         return jsonify({'status': 'profile_updated'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)







# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup
# import nltk
# nltk.download('vader_lexicon')

# # ─────────────────────────────────────────────────────────────────────────────
# # Correct import for the transformer pipeline
# from transformers import pipeline as _hf_pipeline
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # ─────────────────────────────────────────────────────────────────────────────

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key.

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvda': 'NVDA',
#     'amd': 'AMD',
#     'jnj': 'JNJ',
#     'pfe': 'PFE',
#     'jpm': 'JPM',
#     'gs': 'GS',
#     'ko': 'KO',
#     'pep': 'PEP',
#     'xom': 'XOM',
#     'nee': 'NEE',
#     'cvx': 'CVX',
#     'wmt': 'WMT',
#     'hd': 'HD',
#     'gme': 'GME',
#     'tsla': 'TSLA',
#     'f': 'F',
#     'coin': 'COIN',
#     'mrna': 'MRNA'
# }

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # Sentiment Analysis (FinBERT, RoBERTa, VADER)
# # ---------------------------
# finbert = _hf_pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")  # Corrected pipeline import
# roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()

# def analyze_sentiment(text):
#     """Fixed-weight ensemble sentiment analysis using FinBERT, RoBERTa, and VADER."""
    
#     # Sentiment from FinBERT
#     finbert_result = finbert(text)[0]
#     finbert_label = finbert_result['label']
#     finbert_score = finbert_result['score']
    
#     # Sentiment from RoBERTa
#     roberta_result = roberta(text)[0]
#     roberta_label = roberta_result['label']
#     roberta_score = roberta_result['score']
    
#     # Sentiment from VADER
#     vader_score = vader.polarity_scores(text)['compound']
    
#     # Map FinBERT result to score: Positive (1), Neutral (0), Negative (-1)
#     finbert_score = 1 if finbert_label == 'Positive' else -1 if finbert_label == 'Negative' else 0
    
#     # Map RoBERTa result to score: Positive (1), Neutral (0), Negative (-1)
#     roberta_score = roberta_score if roberta_label == 'POS' else -roberta_score if roberta_label == 'NEG' else 0
    
#     # VADER score is already a numeric value between -1 and 1 (no need for mapping)
#     vader_weighted_score = vader_score  # VADER score can directly be used for weighting
    
#     # Calculate the weighted score using the defined weights for each model
#     weighted_score = (0.5 * finbert_score) + (0.3 * roberta_score) + (0.2 * vader_weighted_score)
    
#     # Final sentiment label based on the weighted score
#     if weighted_score > 0.35:
#         label = 'Positive'
#     elif weighted_score < -0.35:
#         label = 'Negative'
#     else:
#         label = 'Neutral'
    
#     # Return final sentiment label and weighted score
#     return label, weighted_score

# # ---------------------------
# # Financial Statement Functions
# # ---------------------------
# def get_financial_statements(ticker):
#     """Fetch the financial statements for a given US ticker symbol."""
#     try:
#         company = yf.Ticker(ticker)
#         balance_sheet = company.balance_sheet
#         income_statement = company.financials
#         cashflow_statement = company.cashflow
        
#         # Extracting and cleaning data (filtering required data)
#         net_income = income_statement.loc['Net Income'].iloc[0]
#         total_debt = balance_sheet.loc['Total Debt'].iloc[0]
#         revenue = income_statement.loc['Total Revenue'].iloc[0]
#         operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0]
        
#         financial_summary = {
#             "net_income": net_income,
#             "total_debt": total_debt,
#             "revenue": revenue,
#             "operating_cash_flow": operating_cash_flow
#         }
        
#         return financial_summary

#     except Exception as e:
#         logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
#         return {"error": str(e)}

# # ---------------------------
# # Analyze Financial Sentiment and Generate GPT-2 Summary
# # ---------------------------
# def analyze_financial_data(ticker):
#     financial_data = get_financial_statements(ticker)
#     sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
#     # Example GPT-2 response generation
#     gpt2_prompt = f"Based on the following financial data, {sentiment} sentiment was detected. Provide a summary.\n"
#     gpt2_prompt += f"Revenue: {financial_data['revenue']}\nNet Income: {financial_data['net_income']}\nDebt: {financial_data['total_debt']}\nOperating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     # Using GPT-2 to summarize
#     gpt2_result = generate_gpt2(gpt2_prompt)
    
#     return {
#         "financial_summary": financial_data,
#         "sentiment": sentiment,
#         "sentiment_score": sentiment_score,
#         "explanation": gpt2_result
#     }

# def generate_gpt2(prompt):
#     """Simple mockup of GPT-2's response generation."""
#     # GPT-2 would generate a detailed response
#     return f"The sentiment is {prompt} because the company's revenue is increasing, and while their debt is high, their cash flow is strong."

# # ---------------------------
# # News Fetching Functions
# # ---------------------------
# def google_query(search_term):
#     if "news" not in search_term.lower():
#         search_term += " stock news"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws"
#     return re.sub(r"\s", "+", url)

# def google_scrape_news(company_name):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         html = response.text
#     except Exception as e:
#         app.logger.error(f"Error fetching news from Google: {e}")
#         return [], "Recent News:\nNo news available."
    
#     soup = BeautifulSoup(html, "html.parser")
#     headlines = []
#     for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
#         headline = tag.get_text().strip()
#         if headline and headline not in headlines:
#             headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if len(headlines) > 4:
#         headlines = headlines[:4]
#     news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# def get_news_from_newsapi(company_name):
#     if not NEWSAPI_KEY:
#         app.logger.error("NEWSAPI_KEY is not provided.")
#         return [], ""
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": company_name + " stock",
#         "sortBy": "publishedAt",
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 4
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
#         if headlines:
#             news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#             return headlines, news_string
#     except Exception as e:
#         app.logger.error(f"NewsAPI error: {e}")
#     return [], ""

# def get_recent_stock_news(company_name, ticker):
#     stock = yf.Ticker(ticker)
#     try:
#         news_items = stock.news
#     except Exception:
#         news_items = []
#     headlines = []
#     if news_items:
#         for item in news_items:
#             if "title" in item and item["title"]:
#                 headlines.append(item["title"])
#     if not headlines:
#         headlines, news_string = get_news_from_newsapi(company_name)
#         if not headlines:
#             headlines, news_string = google_scrape_news(company_name)
#     else:
#         news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# # ---------------------------
# # Define extract_company_and_ticker Function
# # ---------------------------
# def extract_company_and_ticker(query):
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# # ---------------------------
# # API Endpoints (Preserved News Section)
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         _, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; missing ticker'}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}".'}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist  = stock.history(period="1mo")
#         info  = stock.info

#         current_price   = hist['Close'].iloc[-1]
#         open_price      = hist['Open'].iloc[-1]
#         high_price      = hist['High'].iloc[-1]
#         low_price       = hist['Low'].iloc[-1]
#         previous_close  = hist['Close'].iloc[-2] if len(hist)>1 else current_price
#         volume          = hist['Volume'].iloc[-1]

#         sma_10          = hist['Close'].rolling(10).mean().iloc[-1]
#         trend           = "up" if current_price > sma_10 else "down"
#         price_change    = (current_price - previous_close) / previous_close
#         volatility      = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change*10))
#         confidence -= min(0.1, volatility*0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name, _ = extract_company_and_ticker(ticker)
#         news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)

#         # original FinBERT-only sentiments
#         sentiments = analyze_sentiment(news_string)
#         overall_sentiment = sentiments[0]  # Sentiment from analyze_sentiment

#         # ─────────────── New: ensemble sentiment scores ───────────────
#         detailed_sentiments = []
#         for hl in news_list:
#             label, score = analyze_sentiment(hl)
#             detailed_sentiments.append({
#                 'headline': hl,
#                 'label': label,
#                 'score': round(score, 2)
#             })
#         # ────────────────────────────────────────────────────────────────

#         # Fetch financial statement sentiment
#         financial_sentiment_data = analyze_financial_data(ticker)
#         financial_sentiment = financial_sentiment_data['sentiment']
#         financial_statements_content = financial_sentiment_data['financial_summary']

#         # Rule-based decision
#         if trend == "up" and overall_sentiment == "Positive":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "Negative":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         analysis = (
#             f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} ..."
#         )

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'detailed_sentiments': detailed_sentiments,
#             'financial_statements_sentiment': financial_sentiment,
#             'financial_statements_content': financial_statements_content,
#             'analysis': analysis
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)





# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup
# import nltk
# nltk.download('vader_lexicon')

# # ─────────────────────────────────────────────────────────────────────────────
# # Correct import for the transformer pipeline
# from transformers import pipeline as _hf_pipeline
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # ─────────────────────────────────────────────────────────────────────────────

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key.

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvda': 'NVDA',
#     'amd': 'AMD',
#     'jnj': 'JNJ',
#     'pfe': 'PFE',
#     'jpm': 'JPM',
#     'gs': 'GS',
#     'ko': 'KO',
#     'pep': 'PEP',
#     'xom': 'XOM',
#     'nee': 'NEE',
#     'cvx': 'CVX',
#     'wmt': 'WMT',
#     'hd': 'HD',
#     'gme': 'GME',
#     'tsla': 'TSLA',
#     'f': 'F',
#     'coin': 'COIN',
#     'mrna': 'MRNA'
# }

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # Sentiment Analysis (FinBERT, RoBERTa, VADER)
# # ---------------------------
# finbert = _hf_pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")  # Corrected pipeline import
# roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()

# def analyze_sentiment(text):
#     """Fixed-weight ensemble sentiment analysis using FinBERT, RoBERTa, and VADER."""
    
#     # Sentiment from FinBERT
#     finbert_result = finbert(text)[0]
#     finbert_label = finbert_result['label']
#     finbert_score = finbert_result['score']
    
#     # Sentiment from RoBERTa
#     roberta_result = roberta(text)[0]
#     roberta_label = roberta_result['label']
#     roberta_score = roberta_result['score']
    
#     # Sentiment from VADER
#     vader_score = vader.polarity_scores(text)['compound']
    
#     # Map FinBERT result to score: Positive (1), Neutral (0), Negative (-1)
#     finbert_score = 1 if finbert_label == 'Positive' else -1 if finbert_label == 'Negative' else 0
    
#     # Map RoBERTa result to score: Positive (1), Neutral (0), Negative (-1)
#     roberta_score = roberta_score if roberta_label == 'POS' else -roberta_score if roberta_label == 'NEG' else 0
    
#     # VADER score is already a numeric value between -1 and 1 (no need for mapping)
#     vader_weighted_score = vader_score  # VADER score can directly be used for weighting
    
#     # Calculate the weighted score using the defined weights for each model
#     weighted_score = (0.5 * finbert_score) + (0.3 * roberta_score) + (0.2 * vader_weighted_score)
    
#     # Final sentiment label based on the weighted score
#     if weighted_score > 0.35:
#         label = 'Positive'
#     elif weighted_score < -0.35:
#         label = 'Negative'
#     else:
#         label = 'Neutral'
    
#     # Return final sentiment label and weighted score
#     return label, weighted_score

# # ---------------------------
# # Financial Statement Functions
# # ---------------------------
# # def get_financial_statements(ticker):
# #     """Fetch the financial statements for a given US ticker symbol."""
# #     try:
# #         company = yf.Ticker(ticker)
# #         balance_sheet = company.balance_sheet
# #         income_statement = company.financials
# #         cashflow_statement = company.cashflow
        
# #         # Extracting and cleaning data (filtering required data)
# #         net_income = income_statement.loc['Net Income'].iloc[0]
# #         total_debt = balance_sheet.loc['Total Debt'].iloc[0]
# #         revenue = income_statement.loc['Total Revenue'].iloc[0]
# #         operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0]
        
# #         financial_summary = {
# #             "net_income": net_income,
# #             "total_debt": total_debt,
# #             "revenue": revenue,
# #             "operating_cash_flow": operating_cash_flow
# #         }
        
# #         return financial_summary

# #     except Exception as e:
# #         logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
# #         return {"error": str(e)}

# # # ---------------------------
# # # Analyze Financial Sentiment and Generate GPT-2 Summary
# # # ---------------------------
# # def analyze_financial_data(ticker):
# #     financial_data = get_financial_statements(ticker)
# #     sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    
# #     sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
# #     # Example GPT-2 response generation
# #     gpt2_prompt = f"Based on the following financial data, {sentiment} sentiment was detected. Provide a summary.\n"
# #     gpt2_prompt += f"Revenue: {financial_data['revenue']}\nNet Income: {financial_data['net_income']}\nDebt: {financial_data['total_debt']}\nOperating Cash Flow: {financial_data['operating_cash_flow']}"
    
# #     # Using GPT-2 to summarize
# #     gpt2_result = generate_gpt2(gpt2_prompt)
    
# #     return {
# #         "financial_summary": financial_data,
# #         "sentiment": sentiment,
# #         "sentiment_score": sentiment_score,
# #         "explanation": gpt2_result
# #     }

# # def generate_gpt2(prompt):
# #     """Simple mockup of GPT-2's response generation."""
# #     # GPT-2 would generate a detailed response
# #     return f"The sentiment is {prompt} because the company's revenue is increasing, and while their debt is high, their cash flow is strong."

# def get_financial_statements(ticker):
#     """Fetch the financial statements for a given US ticker symbol."""
#     try:
#         company = yf.Ticker(ticker)
#         balance_sheet = company.balance_sheet
#         income_statement = company.financials
#         cashflow_statement = company.cashflow
        
#         # Extracting and cleaning data (filtering required data)
#         net_income = income_statement.loc['Net Income'].iloc[0]
#         total_debt = balance_sheet.loc['Total Debt'].iloc[0]
#         revenue = income_statement.loc['Total Revenue'].iloc[0]
#         operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0]
        
#         financial_summary = {
#             "net_income": net_income,
#             "total_debt": total_debt,
#             "revenue": revenue,
#             "operating_cash_flow": operating_cash_flow
#         }
        
#         return financial_summary

#     except Exception as e:
#         logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
#         return {"error": str(e)}

# # ---------------------------
# # Analyze Financial Sentiment and Generate GPT-2 Summary
# # ---------------------------
# def analyze_financial_data(ticker):
#     financial_data = get_financial_statements(ticker)
#     sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
#     # Example GPT-2 response generation
#     gpt2_prompt = f"Based on the following financial data, {sentiment} sentiment was detected. Provide a summary.\n"
#     gpt2_prompt += f"Revenue: {financial_data['revenue']}\nNet Income: {financial_data['net_income']}\nDebt: {financial_data['total_debt']}\nOperating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     # Using GPT-2 to summarize
#     gpt2_result = generate_gpt2(gpt2_prompt)
    
#     return {
#         "financial_summary": financial_data,
#         "sentiment": sentiment,
#         "sentiment_score": sentiment_score,
#         "explanation": gpt2_result
#     }

# def generate_gpt2(prompt):
#     """Simple mockup of GPT-2's response generation."""
#     # GPT-2 would generate a detailed response
#     return f"The sentiment is {prompt} because the company's revenue is increasing, and while their debt is high, their cash flow is strong."


# # ---------------------------
# # News Fetching Functions
# # ---------------------------
# def google_query(search_term):
#     if "news" not in search_term.lower():
#         search_term += " stock news"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws"
#     return re.sub(r"\s", "+", url)

# def google_scrape_news(company_name):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         html = response.text
#     except Exception as e:
#         app.logger.error(f"Error fetching news from Google: {e}")
#         return [], "Recent News:\nNo news available."
    
#     soup = BeautifulSoup(html, "html.parser")
#     headlines = []
#     for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
#         headline = tag.get_text().strip()
#         if headline and headline not in headlines:
#             headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if len(headlines) > 4:
#         headlines = headlines[:4]
#     news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# def get_news_from_newsapi(company_name):
#     if not NEWSAPI_KEY:
#         app.logger.error("NEWSAPI_KEY is not provided.")
#         return [], ""
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": company_name + " stock",
#         "sortBy": "publishedAt",
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 4
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
#         if headlines:
#             news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#             return headlines, news_string
#     except Exception as e:
#         app.logger.error(f"NewsAPI error: {e}")
#     return [], ""

# def get_recent_stock_news(company_name, ticker):
#     stock = yf.Ticker(ticker)
#     try:
#         news_items = stock.news
#     except Exception:
#         news_items = []
#     headlines = []
#     if news_items:
#         for item in news_items:
#             if "title" in item and item["title"]:
#                 headlines.append(item["title"])
#     if not headlines:
#         headlines, news_string = get_news_from_newsapi(company_name)
#         if not headlines:
#             headlines, news_string = google_scrape_news(company_name)
#     else:
#         news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# # ---------------------------
# # Define extract_company_and_ticker Function
# # ---------------------------
# def extract_company_and_ticker(query):
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# # ---------------------------
# # API Endpoints (Preserved News Section)
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         _, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; missing ticker'}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}".'}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist  = stock.history(period="1mo")
#         info  = stock.info

#         current_price   = hist['Close'].iloc[-1]
#         open_price      = hist['Open'].iloc[-1]
#         high_price      = hist['High'].iloc[-1]
#         low_price       = hist['Low'].iloc[-1]
#         previous_close  = hist['Close'].iloc[-2] if len(hist)>1 else current_price
#         volume          = hist['Volume'].iloc[-1]

#         sma_10          = hist['Close'].rolling(10).mean().iloc[-1]
#         trend           = "up" if current_price > sma_10 else "down"
#         price_change    = (current_price - previous_close) / previous_close
#         volatility      = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change*10))
#         confidence -= min(0.1, volatility*0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name, _ = extract_company_and_ticker(ticker)
#         news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)

#         # original FinBERT-only sentiments
#         sentiments = analyze_sentiment(news_string)
#         overall_sentiment = sentiments[0]  # Sentiment from analyze_sentiment

#         # ─────────────── New: ensemble sentiment scores ───────────────
#         detailed_sentiments = []
#         for hl in news_list:
#             label, score = analyze_sentiment(hl)
#             detailed_sentiments.append({
#                 'headline': hl,
#                 'label': label,
#                 'score': round(score, 2)
#             })
#         # ────────────────────────────────────────────────────────────────

#         # Fetch financial statement sentiment
#         financial_sentiment_data = analyze_financial_data(ticker)
#         financial_sentiment = financial_sentiment_data['sentiment']
#         financial_statements_content = financial_sentiment_data['financial_summary']

#         # Rule-based decision
#         if trend == "up" and overall_sentiment == "Positive":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "Negative":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         analysis = (
#             f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} ..."
#         )

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'detailed_sentiments': detailed_sentiments,
#             'financial_statements_sentiment': financial_sentiment,
#             'financial_statements_content': financial_statements_content,
#             'analysis': analysis
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)












# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup
# import nltk
# nltk.download('vader_lexicon')

# # ─────────────────────────────────────────────────────────────────────────────
# # Correct import for the transformer pipeline
# from transformers import pipeline as _hf_pipeline
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # ─────────────────────────────────────────────────────────────────────────────

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key.

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvda': 'NVDA',
#     'amd': 'AMD',
#     'jnj': 'JNJ',
#     'pfe': 'PFE',
#     'jpm': 'JPM',
#     'gs': 'GS',
#     'ko': 'KO',
#     'pep': 'PEP',
#     'xom': 'XOM',
#     'nee': 'NEE',
#     'cvx': 'CVX',
#     'wmt': 'WMT',
#     'hd': 'HD',
#     'gme': 'GME',
#     'tsla': 'TSLA',
#     'f': 'F',
#     'coin': 'COIN',
#     'mrna': 'MRNA'
# }

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # Sentiment Analysis (FinBERT, RoBERTa, VADER)
# # ---------------------------
# finbert = _hf_pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")  # Corrected pipeline import
# roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()

# def analyze_sentiment(text):
#     """Fixed-weight ensemble sentiment analysis using FinBERT, RoBERTa, and VADER."""
    
#     # Sentiment from FinBERT
#     finbert_result = finbert(text)[0]
#     finbert_label = finbert_result['label']
#     finbert_score = finbert_result['score']
    
#     # Sentiment from RoBERTa
#     roberta_result = roberta(text)[0]
#     roberta_label = roberta_result['label']
#     roberta_score = roberta_result['score']
    
#     # Sentiment from VADER
#     vader_score = vader.polarity_scores(text)['compound']
    
#     # Map FinBERT result to score: Positive (1), Neutral (0), Negative (-1)
#     finbert_score = 1 if finbert_label == 'Positive' else -1 if finbert_label == 'Negative' else 0
    
#     # Map RoBERTa result to score: Positive (1), Neutral (0), Negative (-1)
#     roberta_score = roberta_score if roberta_label == 'POS' else -roberta_score if roberta_label == 'NEG' else 0
    
#     # VADER score is already a numeric value between -1 and 1 (no need for mapping)
#     vader_weighted_score = vader_score  # VADER score can directly be used for weighting
    
#     # Calculate the weighted score using the defined weights for each model
#     weighted_score = (0.5 * finbert_score) + (0.3 * roberta_score) + (0.2 * vader_weighted_score)
    
#     # Final sentiment label based on the weighted score
#     if weighted_score > 0.35:
#         label = 'Positive'
#     elif weighted_score < -0.35:
#         label = 'Negative'
#     else:
#         label = 'Neutral'
    
#     # Return final sentiment label and weighted score
#     return label, weighted_score

# # ---------------------------
# # Financial Statement Functions
# # ---------------------------
# def get_financial_statements(ticker):
#     """Fetch the financial statements for a given US ticker symbol."""
#     try:
#         company = yf.Ticker(ticker)
#         balance_sheet = company.balance_sheet
#         income_statement = company.financials
#         cashflow_statement = company.cashflow
        
#         # Extracting and cleaning data (filtering required data)
#         net_income = income_statement.loc['Net Income'].iloc[0]
#         total_debt = balance_sheet.loc['Total Debt'].iloc[0]
#         revenue = income_statement.loc['Total Revenue'].iloc[0]
#         operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0]
        
#         financial_summary = {
#             "net_income": net_income,
#             "total_debt": total_debt,
#             "revenue": revenue,
#             "operating_cash_flow": operating_cash_flow
#         }
        
#         # Return the financial summary as a formatted string for the response
#         financial_summary_str = f"Revenue: {revenue}\nNet Income: {net_income}\nDebt: {total_debt}\nOperating Cash Flow: {operating_cash_flow}"
        
#         return financial_summary, financial_summary_str

#     except Exception as e:
#         logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
#         return {"error": str(e)}, ""

# # ---------------------------
# # Analyze Financial Sentiment and Generate GPT-2 Summary
# # ---------------------------
# def analyze_financial_data(ticker):
#     financial_data, financial_summary_str = get_financial_statements(ticker)
#     sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
#     return {
#         "financial_summary": financial_data,
#         "financial_summary_str": financial_summary_str,  # Add the string version for display
#         "sentiment": sentiment,
#         "sentiment_score": sentiment_score
#     }

# # ---------------------------
# # News Fetching Functions
# # ---------------------------
# def google_query(search_term):
#     if "news" not in search_term.lower():
#         search_term += " stock news"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws"
#     return re.sub(r"\s", "+", url)

# def google_scrape_news(company_name):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         html = response.text
#     except Exception as e:
#         app.logger.error(f"Error fetching news from Google: {e}")
#         return [], "Recent News:\nNo news available."
    
#     soup = BeautifulSoup(html, "html.parser")
#     headlines = []
#     for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
#         headline = tag.get_text().strip()
#         if headline and headline not in headlines:
#             headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if len(headlines) > 4:
#         headlines = headlines[:4]
#     news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# def get_news_from_newsapi(company_name):
#     if not NEWSAPI_KEY:
#         app.logger.error("NEWSAPI_KEY is not provided.")
#         return [], ""
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": company_name + " stock",
#         "sortBy": "publishedAt",
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 4
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
#         if headlines:
#             news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#             return headlines, news_string
#     except Exception as e:
#         app.logger.error(f"NewsAPI error: {e}")
#     return [], ""

# def get_recent_stock_news(company_name, ticker):
#     stock = yf.Ticker(ticker)
#     try:
#         news_items = stock.news
#     except Exception:
#         news_items = []
#     headlines = []
#     if news_items:
#         for item in news_items:
#             if "title" in item and item["title"]:
#                 headlines.append(item["title"])
#     if not headlines:
#         headlines, news_string = get_news_from_newsapi(company_name)
#         if not headlines:
#             headlines, news_string = google_scrape_news(company_name)
#     else:
#         news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# # ---------------------------
# # Define extract_company_and_ticker Function
# # ---------------------------
# def extract_company_and_ticker(query):
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# # ---------------------------
# # API Endpoints (Preserved News Section)
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         _, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; missing ticker'}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}".'}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist  = stock.history(period="1mo")
#         info  = stock.info

#         current_price   = hist['Close'].iloc[-1]
#         open_price      = hist['Open'].iloc[-1]
#         high_price      = hist['High'].iloc[-1]
#         low_price       = hist['Low'].iloc[-1]
#         previous_close  = hist['Close'].iloc[-2] if len(hist)>1 else current_price
#         volume          = hist['Volume'].iloc[-1]

#         sma_10          = hist['Close'].rolling(10).mean().iloc[-1]
#         trend           = "up" if current_price > sma_10 else "down"
#         price_change    = (current_price - previous_close) / previous_close
#         volatility      = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change*10))
#         confidence -= min(0.1, volatility*0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name, _ = extract_company_and_ticker(ticker)
#         news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)

#         # original FinBERT-only sentiments
#         sentiments = analyze_sentiment(news_string)
#         overall_sentiment = sentiments[0]  # Sentiment from analyze_sentiment

#         # ─────────────── New: ensemble sentiment scores ───────────────
#         detailed_sentiments = []
#         for hl in news_list:
#             label, score = analyze_sentiment(hl)
#             detailed_sentiments.append({
#                 'headline': hl,
#                 'label': label,
#                 'score': round(score, 2)
#             })
#         # ────────────────────────────────────────────────────────────────

#         # Fetch financial statement sentiment
#         financial_sentiment_data = analyze_financial_data(ticker)
#         financial_sentiment = financial_sentiment_data['sentiment']
#         financial_statements_content = financial_sentiment_data['financial_summary_str']  # Get the string version

#         # Rule-based decision
#         if trend == "up" and overall_sentiment == "Positive":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "Negative":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         analysis = (
#             f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} ..."
#         )

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'detailed_sentiments': detailed_sentiments,
#             'financial_statements_sentiment': financial_sentiment,
#             'financial_statements_content': financial_statements_content,  # Displaying content here
#             'analysis': analysis
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)


####################### MAIN ##########################

# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup
# import nltk
# nltk.download('vader_lexicon')

# # ─────────────────────────────────────────────────────────────────────────────
# # Correct import for the transformer pipeline
# from transformers import pipeline as _hf_pipeline
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # ─────────────────────────────────────────────────────────────────────────────

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key.

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvda': 'NVDA',
#     'amd': 'AMD',
#     'jnj': 'JNJ',
#     'pfe': 'PFE',
#     'jpm': 'JPM',
#     'gs': 'GS',
#     'ko': 'KO',
#     'pep': 'PEP',
#     'xom': 'XOM',
#     'nee': 'NEE',
#     'cvx': 'CVX',
#     'wmt': 'WMT',
#     'hd': 'HD',
#     'gme': 'GME',
#     'tsla': 'TSLA',
#     'f': 'F',
#     'coin': 'COIN',
#     'mrna': 'MRNA'
# }

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # Sentiment Analysis (FinBERT, RoBERTa, VADER)
# # ---------------------------
# finbert = _hf_pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")  # Corrected pipeline import
# roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()

# def analyze_sentiment(text):
#     """Fixed-weight ensemble sentiment analysis using FinBERT, RoBERTa, and VADER."""
    
#     # Sentiment from FinBERT
#     finbert_result = finbert(text)[0]
#     finbert_label = finbert_result['label']
#     finbert_score = finbert_result['score']
    
#     # Sentiment from RoBERTa
#     roberta_result = roberta(text)[0]
#     roberta_label = roberta_result['label']
#     roberta_score = roberta_result['score']
    
#     # Sentiment from VADER
#     vader_score = vader.polarity_scores(text)['compound']
    
#     # Map FinBERT result to score: Positive (1), Neutral (0), Negative (-1)
#     finbert_score = 1 if finbert_label == 'Positive' else -1 if finbert_label == 'Negative' else 0
    
#     # Map RoBERTa result to score: Positive (1), Neutral (0), Negative (-1)
#     roberta_score = roberta_score if roberta_label == 'POS' else -roberta_score if roberta_label == 'NEG' else 0
    
#     # VADER score is already a numeric value between -1 and 1 (no need for mapping)
#     vader_weighted_score = vader_score  # VADER score can directly be used for weighting
    
#     # Calculate the weighted score using the defined weights for each model
#     weighted_score = (0.5 * finbert_score) + (0.3 * roberta_score) + (0.2 * vader_weighted_score)
    
#     # Final sentiment label based on the weighted score
#     if weighted_score > 0.15:
#         label = 'Positive'
#     elif weighted_score < -0.15:
#         label = 'Negative'
#     else:
#         label = 'Neutral'
    
#     # Return final sentiment label and weighted score
#     return label, weighted_score

# # ---------------------------
# # Financial Statement Functions
# # ---------------------------
# def get_financial_statements(ticker):
#     """Fetch the financial statements for a given US ticker symbol for the last 3 years."""
#     try:
#         company = yf.Ticker(ticker)
#         balance_sheet = company.balance_sheet
#         income_statement = company.financials
#         cashflow_statement = company.cashflow
        
#         # Extracting data for the last 3 years (if available)
#         net_income = income_statement.loc['Net Income'].iloc[0:3]
#         total_debt = balance_sheet.loc['Total Debt'].iloc[0:3]
#         revenue = income_statement.loc['Total Revenue'].iloc[0:3]
#         operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0:3]
        
#         financial_summary = {
#             "net_income": net_income.tolist(),
#             "total_debt": total_debt.tolist(),
#             "revenue": revenue.tolist(),
#             "operating_cash_flow": operating_cash_flow.tolist()
#         }
        
#         financial_summary_str = f"Revenue: {revenue}\nNet Income: {net_income}\nDebt: {total_debt}\nOperating Cash Flow: {operating_cash_flow}"
        
#         return financial_summary, financial_summary_str

#     except Exception as e:
#         logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
#         return {"error": str(e)}, ""

# # ---------------------------
# # Analyze Financial Sentiment and Generate GPT-2 Summary
# # ---------------------------
# def analyze_financial_data(ticker):
#     financial_data, financial_summary_str = get_financial_statements(ticker)
#     sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
#     gpt2_prompt = f"Based on the following financial data, {sentiment} sentiment was detected. Provide a summary.\n"
#     gpt2_prompt += f"Revenue: {financial_data['revenue']}\nNet Income: {financial_data['net_income']}\nDebt: {financial_data['total_debt']}\nOperating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     gpt2_result = generate_gpt2(gpt2_prompt)
    
#     return {
#         "financial_summary": financial_data,
#         "financial_summary_str": financial_summary_str,  # Add the string version for display
#         "sentiment": sentiment,
#         "sentiment_score": sentiment_score,
#         "explanation": gpt2_result
#     }

# def generate_gpt2(prompt):
#     """Simple mockup of GPT-2's response generation."""
#     # GPT-2 would generate a detailed response
#     return f"The sentiment is {prompt} because the company's revenue is increasing, and while their debt is high, their cash flow is strong."

# # ---------------------------
# # News Fetching Functions
# # ---------------------------
# def google_query(search_term):
#     if "news" not in search_term.lower():
#         search_term += " stock news"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws"
#     return re.sub(r"\s", "+", url)

# def google_scrape_news(company_name):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         html = response.text
#     except Exception as e:
#         app.logger.error(f"Error fetching news from Google: {e}")
#         return [], "Recent News:\nNo news available."
    
#     soup = BeautifulSoup(html, "html.parser")
#     headlines = []
#     for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
#         headline = tag.get_text().strip()
#         if headline and headline not in headlines:
#             headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if len(headlines) > 4:
#         headlines = headlines[:4]
#     news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# def get_news_from_newsapi(company_name):
#     if not NEWSAPI_KEY:
#         app.logger.error("NEWSAPI_KEY is not provided.")
#         return [], ""
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": company_name + " stock",
#         "sortBy": "publishedAt",
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 4
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
#         if headlines:
#             news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#             return headlines, news_string
#     except Exception as e:
#         app.logger.error(f"NewsAPI error: {e}")
#     return [], ""

# def get_recent_stock_news(company_name, ticker):
#     stock = yf.Ticker(ticker)
#     try:
#         news_items = stock.news
#     except Exception:
#         news_items = []
#     headlines = []
#     if news_items:
#         for item in news_items:
#             if "title" in item and item["title"]:
#                 headlines.append(item["title"])
#     if not headlines:
#         headlines, news_string = get_news_from_newsapi(company_name)
#         if not headlines:
#             headlines, news_string = google_scrape_news(company_name)
#     else:
#         news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# # ---------------------------
# # Define extract_company_and_ticker Function
# # ---------------------------
# def extract_company_and_ticker(query):
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# # ---------------------------
# # API Endpoints (Preserved News Section)
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         _, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; missing ticker'}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}".'}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist  = stock.history(period="1mo")
#         info  = stock.info

#         current_price   = hist['Close'].iloc[-1]
#         open_price      = hist['Open'].iloc[-1]
#         high_price      = hist['High'].iloc[-1]
#         low_price       = hist['Low'].iloc[-1]
#         previous_close  = hist['Close'].iloc[-2] if len(hist)>1 else current_price
#         volume          = hist['Volume'].iloc[-1]

#         sma_10          = hist['Close'].rolling(10).mean().iloc[-1]
#         trend           = "up" if current_price > sma_10 else "down"
#         price_change    = (current_price - previous_close) / previous_close
#         volatility      = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change*10))
#         confidence -= min(0.1, volatility*0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name, _ = extract_company_and_ticker(ticker)
#         news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)

#         # original FinBERT-only sentiments
#         sentiments = analyze_sentiment(news_string)
#         overall_sentiment = sentiments[0]  # Sentiment from analyze_sentiment

#         # ─────────────── New: ensemble sentiment scores ───────────────
#         detailed_sentiments = []
#         for hl in news_list:
#             label, score = analyze_sentiment(hl)
#             detailed_sentiments.append({
#                 'headline': hl,
#                 'label': label,
#                 'score': round(score, 2)
#             })
#         # ────────────────────────────────────────────────────────────────

#         # Fetch financial statement sentiment
#         financial_sentiment_data = analyze_financial_data(ticker)
#         financial_sentiment = financial_sentiment_data['sentiment']
#         financial_statements_content = financial_sentiment_data['financial_summary_str']  # Get the string version

#         # Rule-based decision
#         if trend == "up" and overall_sentiment == "Positive":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "Negative":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         analysis = (
#             f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} ..."
#         )

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'detailed_sentiments': detailed_sentiments,
#             'financial_statements_sentiment': financial_sentiment,
#             'financial_statements_content': financial_statements_content,  # Displaying content here
#             'analysis': analysis
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)


# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup
# import nltk
# nltk.download('vader_lexicon')

# # ─────────────────────────────────────────────────────────────────────────────
# # Correct import for the transformer pipeline
# from transformers import pipeline as _hf_pipeline
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # ─────────────────────────────────────────────────────────────────────────────

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key.

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvda': 'NVDA',
#     'amd': 'AMD',
#     'jnj': 'JNJ',
#     'pfe': 'PFE',
#     'jpm': 'JPM',
#     'gs': 'GS',
#     'ko': 'KO',
#     'pep': 'PEP',
#     'xom': 'XOM',
#     'nee': 'NEE',
#     'cvx': 'CVX',
#     'wmt': 'WMT',
#     'hd': 'HD',
#     'gme': 'GME',
#     'tsla': 'TSLA',
#     'f': 'F',
#     'coin': 'COIN',
#     'mrna': 'MRNA'
# }

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # Sentiment Analysis (FinBERT, RoBERTa, VADER)
# # ---------------------------
# finbert = _hf_pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")  # Corrected pipeline import
# roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()

# # def analyze_sentiment(text):
# #     """Fixed-weight ensemble sentiment analysis using FinBERT, RoBERTa, and VADER."""
    
# #     # Sentiment from FinBERT
# #     finbert_result = finbert(text)[0]
# #     finbert_label = finbert_result['label']
# #     finbert_score = finbert_result['score']
    
# #     # Sentiment from RoBERTa
# #     roberta_result = roberta(text)[0]
# #     roberta_label = roberta_result['label']
# #     roberta_score = roberta_result['score']
    
# #     # Sentiment from VADER
# #     vader_score = vader.polarity_scores(text)['compound']
    
# #     # Adjust sentiment based on specific keywords (for stock acquisition news)
# #     if "increases position" in text.lower() or "purchases more shares" in text.lower() or "acquires" in text.lower():
# #         finbert_score = 1  # Boost sentiment to positive if acquiring stocks
    
# #     if "sells" in text.lower() or "decreases stake" in text.lower() or "cuts" in text.lower():
# #         finbert_score = -1  # Set sentiment to negative if selling or cutting stake

# #     # Calculate the weighted score using the defined weights for each model
# #     weighted_score = (0.5 * finbert_score) + (0.3 * roberta_score) + (0.2 * vader_score)
    
# #     # Final sentiment label based on the weighted score
# #     if weighted_score > 0.15:
# #         label = 'Positive'
# #     elif weighted_score < -0.15:
# #         label = 'Negative'
# #     else:
# #         label = 'Neutral'
    
# #     # Return final sentiment label and weighted score
# #     return label, weighted_score

# def analyze_sentiment(text):
#     """Fixed-weight ensemble sentiment analysis using FinBERT, RoBERTa, and VADER."""
    
#     # Sentiment from FinBERT
#     finbert_result = finbert(text)[0]
#     finbert_label = finbert_result['label']
#     finbert_score = finbert_result['score']
    
#     # Sentiment from RoBERTa
#     roberta_result = roberta(text)[0]
#     roberta_label = roberta_result['label']
#     roberta_score = roberta_result['score']
    
#     # Sentiment from VADER
#     vader_score = vader.polarity_scores(text)['compound']
    
#     # Flag for stock acquisitions and sales
#     acquire_keywords = ["increases position", "purchases more shares", "acquires", "buys"]
#     sell_keywords = ["sells shares", "decreases stake", "cuts position", "sells off", "sells", "cuts"]
    
#     # Check for acquisition-related news and set sentiment to Positive
#     if any(keyword in text.lower() for keyword in acquire_keywords):
#         finbert_score = 1  # Positive sentiment for acquisitions
    
#     # Check for sales-related news and set sentiment to Negative
#     elif any(keyword in text.lower() for keyword in sell_keywords):
#         finbert_score = -1  # Negative sentiment for sales
    
#     # Calculate the weighted score using the defined weights for each model
#     weighted_score = (0.5 * finbert_score) + (0.3 * roberta_score) + (0.2 * vader_score)
    
#     # Final sentiment label based on the weighted score
#     if weighted_score > 0.15:
#         label = 'Positive'
#     elif weighted_score < -0.15:
#         label = 'Negative'
#     else:
#         label = 'Neutral'
    
#     # Return final sentiment label and weighted score
#     return label, weighted_score


# # ---------------------------
# # Financial Statement Functions
# # ---------------------------
# def get_financial_statements(ticker):
#     """Fetch the financial statements for a given US ticker symbol for the last 3 years."""
#     try:
#         company = yf.Ticker(ticker)
#         balance_sheet = company.balance_sheet
#         income_statement = company.financials
#         cashflow_statement = company.cashflow
        
#         # Extracting data for the last 3 years (if available)
#         net_income = income_statement.loc['Net Income'].iloc[0:3]
#         total_debt = balance_sheet.loc['Total Debt'].iloc[0:3]
#         revenue = income_statement.loc['Total Revenue'].iloc[0:3]
#         operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0:3]
        
#         financial_summary = {
#             "net_income": net_income.tolist(),
#             "total_debt": total_debt.tolist(),
#             "revenue": revenue.tolist(),
#             "operating_cash_flow": operating_cash_flow.tolist()
#         }
        
#         financial_summary_str = f"Revenue: {revenue}\nNet Income: {net_income}\nDebt: {total_debt}\nOperating Cash Flow: {operating_cash_flow}"
        
#         return financial_summary, financial_summary_str

#     except Exception as e:
#         logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
#         return {"error": str(e)}, ""

# # ---------------------------
# # Analyze Financial Sentiment and Generate GPT-2 Summary
# # ---------------------------
# def analyze_financial_data(ticker):
#     financial_data, financial_summary_str = get_financial_statements(ticker)
#     sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
#     gpt2_prompt = f"Based on the following financial data, {sentiment} sentiment was detected. Provide a summary.\n"
#     gpt2_prompt += f"Revenue: {financial_data['revenue']}\nNet Income: {financial_data['net_income']}\nDebt: {financial_data['total_debt']}\nOperating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     gpt2_result = generate_gpt2(gpt2_prompt)
    
#     return {
#         "financial_summary": financial_data,
#         "financial_summary_str": financial_summary_str,  # Add the string version for display
#         "sentiment": sentiment,
#         "sentiment_score": sentiment_score,
#         "explanation": gpt2_result
#     }

# def generate_gpt2(prompt):
#     """Simple mockup of GPT-2's response generation."""
#     # GPT-2 would generate a detailed response
#     return f"The sentiment is {prompt} because the company's revenue is increasing, and while their debt is high, their cash flow is strong."

# # ---------------------------
# # News Fetching Functions
# # ---------------------------
# def google_query(search_term):
#     if "news" not in search_term.lower():
#         search_term += " stock news"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws"
#     return re.sub(r"\s", "+", url)

# def google_scrape_news(company_name):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         html = response.text
#     except Exception as e:
#         app.logger.error(f"Error fetching news from Google: {e}")
#         return [], "Recent News:\nNo news available."
    
#     soup = BeautifulSoup(html, "html.parser")
#     headlines = []
#     for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
#         headline = tag.get_text().strip()
#         if headline and headline not in headlines:
#             headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if len(headlines) > 4:
#         headlines = headlines[:4]
#     news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# def get_news_from_newsapi(company_name):
#     if not NEWSAPI_KEY:
#         app.logger.error("NEWSAPI_KEY is not provided.")
#         return [], ""
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": company_name + " stock",
#         "sortBy": "publishedAt",
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 4
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
#         if headlines:
#             news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#             return headlines, news_string
#     except Exception as e:
#         app.logger.error(f"NewsAPI error: {e}")
#     return [], ""

# def get_recent_stock_news(company_name, ticker):
#     stock = yf.Ticker(ticker)
#     try:
#         news_items = stock.news
#     except Exception:
#         news_items = []
#     headlines = []
#     if news_items:
#         for item in news_items:
#             if "title" in item and item["title"]:
#                 headlines.append(item["title"])
#     if not headlines:
#         headlines, news_string = get_news_from_newsapi(company_name)
#         if not headlines:
#             headlines, news_string = google_scrape_news(company_name)
#     else:
#         news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# # ---------------------------
# # Define extract_company_and_ticker Function
# # ---------------------------
# def extract_company_and_ticker(query):
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# # ---------------------------
# # API Endpoints (Preserved News Section)
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         _, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; missing ticker'}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}".'}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist  = stock.history(period="1mo")
#         info  = stock.info

#         current_price   = hist['Close'].iloc[-1]
#         open_price      = hist['Open'].iloc[-1]
#         high_price      = hist['High'].iloc[-1]
#         low_price       = hist['Low'].iloc[-1]
#         previous_close  = hist['Close'].iloc[-2] if len(hist)>1 else current_price
#         volume          = hist['Volume'].iloc[-1]

#         sma_10          = hist['Close'].rolling(10).mean().iloc[-1]
#         trend           = "up" if current_price > sma_10 else "down"
#         price_change    = (current_price - previous_close) / previous_close
#         volatility      = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change*10))
#         confidence -= min(0.1, volatility*0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name, _ = extract_company_and_ticker(ticker)
#         news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)

#         # Adjusted sentiment analysis based on improved logic
#         sentiments = analyze_sentiment(news_string)
#         overall_sentiment = sentiments[0]  # Sentiment from analyze_sentiment

#         # ─────────────── New: ensemble sentiment scores ───────────────
#         detailed_sentiments = []
#         for hl in news_list:
#             label, score = analyze_sentiment(hl)
#             detailed_sentiments.append({
#                 'headline': hl,
#                 'label': label,
#                 'score': round(score, 2)
#             })
#         # ────────────────────────────────────────────────────────────────

#         # Fetch financial statement sentiment
#         financial_sentiment_data = analyze_financial_data(ticker)
#         financial_sentiment = financial_sentiment_data['sentiment']
#         financial_statements_content = financial_sentiment_data['financial_summary_str']  # Get the string version

#         # Rule-based decision
#         if trend == "up" and overall_sentiment == "Positive":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "Negative":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         analysis = (
#             f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} ..."
#         )

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'detailed_sentiments': detailed_sentiments,
#             'financial_statements_sentiment': financial_sentiment,
#             'financial_statements_content': financial_statements_content,  # Displaying content here
#             'analysis': analysis
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)



# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import BertForSequenceClassification, BertTokenizer
# from transformers import pipeline
# import torch
# from bs4 import BeautifulSoup
# import requests
# import re
# import yfinance as yf

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key.

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # Load the Fine-Tuned Model
# # ---------------------------
# checkpoint_path = './results/checkpoint-6441'  # Path to the checkpoint directory (adjust as needed)
# tokenizer = BertTokenizer.from_pretrained(checkpoint_path)
# model = BertForSequenceClassification.from_pretrained(checkpoint_path)

# # Use the model for sentiment analysis
# sentiment_model = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# # ---------------------------
# # Sentiment Analysis Function (using the fine-tuned model)
# # ---------------------------
# def analyze_sentiment(text):
#     """Analyze sentiment using the fine-tuned model."""
    
#     # Use the fine-tuned model for sentiment analysis
#     sentiment_result = sentiment_model(text)[0]
    
#     sentiment_label = sentiment_result['label']
#     sentiment_score = sentiment_result['score']
    
#     # Adjust sentiment based on specific keywords (for stock acquisition news)
#     acquire_keywords = ["increases position", "purchases more shares", "acquires", "buys"]
#     sell_keywords = ["sells shares", "decreases stake", "cuts position", "sells off", "sells", "cuts"]
    
#     # Check for acquisition-related news and set sentiment to Positive
#     if any(keyword in text.lower() for keyword in acquire_keywords):
#         sentiment_label = "POSITIVE"
#         sentiment_score = 1  # Positive sentiment for acquisitions
    
#     # Check for sales-related news and set sentiment to Negative
#     elif any(keyword in text.lower() for keyword in sell_keywords):
#         sentiment_label = "NEGATIVE"
#         sentiment_score = -1  # Negative sentiment for sales
    
#     return sentiment_label, sentiment_score

# # ---------------------------
# # Financial Statement Functions
# # ---------------------------
# def get_financial_statements(ticker):
#     """Fetch the financial statements for a given US ticker symbol for the last 3 years."""
#     try:
#         company = yf.Ticker(ticker)
#         balance_sheet = company.balance_sheet
#         income_statement = company.financials
#         cashflow_statement = company.cashflow
        
#         # Extracting data for the last 3 years (if available)
#         net_income = income_statement.loc['Net Income'].iloc[0:3]
#         total_debt = balance_sheet.loc['Total Debt'].iloc[0:3]
#         revenue = income_statement.loc['Total Revenue'].iloc[0:3]
#         operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0:3]
        
#         financial_summary = {
#             "net_income": net_income.tolist(),
#             "total_debt": total_debt.tolist(),
#             "revenue": revenue.tolist(),
#             "operating_cash_flow": operating_cash_flow.tolist()
#         }
        
#         financial_summary_str = f"Revenue: {revenue}\nNet Income: {net_income}\nDebt: {total_debt}\nOperating Cash Flow: {operating_cash_flow}"
        
#         return financial_summary, financial_summary_str

#     except Exception as e:
#         logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
#         return {"error": str(e)}, ""

# # ---------------------------
# # Analyze Financial Sentiment and Generate GPT-2 Summary
# # ---------------------------
# def analyze_financial_data(ticker):
#     financial_data, financial_summary_str = get_financial_statements(ticker)
#     sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
#     gpt2_prompt = f"Based on the following financial data, {sentiment} sentiment was detected. Provide a summary.\n"
#     gpt2_prompt += f"Revenue: {financial_data['revenue']}\nNet Income: {financial_data['net_income']}\nDebt: {financial_data['total_debt']}\nOperating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     gpt2_result = generate_gpt2(gpt2_prompt)
    
#     return {
#         "financial_summary": financial_data,
#         "financial_summary_str": financial_summary_str,  # Add the string version for display
#         "sentiment": sentiment,
#         "sentiment_score": sentiment_score,
#         "explanation": gpt2_result
#     }

# def generate_gpt2(prompt):
#     """Simple mockup of GPT-2's response generation."""
#     return f"The sentiment is {prompt} because the company's revenue is increasing, and while their debt is high, their cash flow is strong."

# # ---------------------------
# # News Fetching Functions
# # ---------------------------
# def google_query(search_term):
#     if "news" not in search_term.lower():
#         search_term += " stock news"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws"
#     return re.sub(r"\s", "+", url)

# def google_scrape_news(company_name):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         html = response.text
#     except Exception as e:
#         app.logger.error(f"Error fetching news from Google: {e}")
#         return [], "Recent News:\nNo news available."
    
#     soup = BeautifulSoup(html, "html.parser")
#     headlines = []
#     for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
#         headline = tag.get_text().strip()
#         if headline and headline not in headlines:
#             headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if not headlines:
#         for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
#     if len(headlines) > 4:
#         headlines = headlines[:4]
#     news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# def get_news_from_newsapi(company_name):
#     if not NEWSAPI_KEY:
#         app.logger.error("NEWSAPI_KEY is not provided.")
#         return [], ""
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": company_name + " stock",
#         "sortBy": "publishedAt",
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 4
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
#         if headlines:
#             news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#             return headlines, news_string
#     except Exception as e:
#         app.logger.error(f"NewsAPI error: {e}")
#     return [], ""

# def get_recent_stock_news(company_name, ticker):
#     stock = yf.Ticker(ticker)
#     try:
#         news_items = stock.news
#     except Exception:
#         news_items = []
#     headlines = []
#     if news_items:
#         for item in news_items:
#             if "title" in item and item["title"]:
#                 headlines.append(item["title"])
#     if not headlines:
#         headlines, news_string = get_news_from_newsapi(company_name)
#         if not headlines:
#             headlines, news_string = google_scrape_news(company_name)
#     else:
#         news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
#     return headlines, news_string

# # ---------------------------
# # Define extract_company_and_ticker Function
# # ---------------------------
# def extract_company_and_ticker(query):
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# # ---------------------------
# # API Endpoints (Preserved News Section)
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys())
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         _, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; missing ticker'}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}".'}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist  = stock.history(period="1mo")
#         info  = stock.info

#         current_price   = hist['Close'].iloc[-1]
#         open_price      = hist['Open'].iloc[-1]
#         high_price      = hist['High'].iloc[-1]
#         low_price       = hist['Low'].iloc[-1]
#         previous_close  = hist['Close'].iloc[-2] if len(hist)>1 else current_price
#         volume          = hist['Volume'].iloc[-1]

#         sma_10          = hist['Close'].rolling(10).mean().iloc[-1]
#         trend           = "up" if current_price > sma_10 else "down"
#         price_change    = (current_price - previous_close) / previous_close
#         volatility      = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change*10))
#         confidence -= min(0.1, volatility*0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name, _ = extract_company_and_ticker(ticker)
#         news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)

#         # Adjusted sentiment analysis based on improved logic
#         sentiments = analyze_sentiment(news_string)
#         overall_sentiment = sentiments[0]  # Sentiment from analyze_sentiment

#         # ─────────────── New: ensemble sentiment scores ───────────────
#         detailed_sentiments = []
#         for hl in news_list:
#             label, score = analyze_sentiment(hl)
#             detailed_sentiments.append({
#                 'headline': hl,
#                 'label': label,
#                 'score': round(score, 2)
#             })
#         # ────────────────────────────────────────────────────────────────

#         # Fetch financial statement sentiment
#         financial_sentiment_data = analyze_financial_data(ticker)
#         financial_sentiment = financial_sentiment_data['sentiment']
#         financial_statements_content = financial_sentiment_data['financial_summary_str']  # Get the string version

#         # Rule-based decision
#         if trend == "up" and overall_sentiment == "Positive":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "Negative":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         analysis = (
#             f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} ..."
#         )

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'detailed_sentiments': detailed_sentiments,
#             'financial_statements_sentiment': financial_sentiment,
#             'financial_statements_content': financial_statements_content,  # Displaying content here
#             'analysis': analysis
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)


# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup
# import nltk
# from transformers import BertForSequenceClassification, BertTokenizer
# from transformers import pipeline

# nltk.download('vader_lexicon')

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Global Variables
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  # Replace with your actual NewsAPI key

# SUPPORTED_TICKERS = [
#     'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
#     'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
#     'TSLA', 'F', 'COIN', 'MRNA'
# ]

# COMPANY_NAME_TO_TICKER = {
#     'apple': 'AAPL',
#     'microsoft': 'MSFT',
#     'nvidia': 'NVDA',
#     'amd': 'AMD',
#     'johnson & johnson': 'JNJ',
#     'pfizer': 'PFE',
#     'jpmorgan': 'JPM',
#     'goldman sachs': 'GS',
#     'coca-cola': 'KO',
#     'pepsi': 'PEP',
#     'exxon': 'XOM',
#     'next era energy': 'NEE',
#     'chevron': 'CVX',
#     'walmart': 'WMT',
#     'home depot': 'HD',
#     'gamestop': 'GME',
#     'tesla': 'TSLA',
#     'ford': 'F',
#     'coinbase': 'COIN',
#     'moderna': 'MRNA'
# }

# SECTOR_MAP = {
#     'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
#     'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
#     'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
#     'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
#     'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
# }

# RISK_LEVELS = {
#     'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
#     'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
#     'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
# }

# user_profile = {
#     'available_amount': 5000.0,
#     'risk_preference': 'medium'
# }

# # ---------------------------
# # Load the Fine-Tuned Model
# # ---------------------------
# checkpoint_path = './results/checkpoint-6441'
# tokenizer = BertTokenizer.from_pretrained(checkpoint_path)
# model = BertForSequenceClassification.from_pretrained(checkpoint_path)
# sentiment_model = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# # ---------------------------
# # Sentiment Analysis Function
# # ---------------------------
# def analyze_sentiment(text):
#     """Analyze sentiment using the fine-tuned model."""
#     sentiment_result = sentiment_model(text)[0]
#     sentiment_label = sentiment_result['label']
#     sentiment_score = sentiment_result['score']
    
#     # Adjust sentiment based on specific keywords
#     acquire_keywords = ["increases position", "purchases more shares", "acquires", "buys"]
#     sell_keywords = ["sells shares", "decreases stake", "cuts position", "sells off"]
    
#     if any(keyword in text.lower() for keyword in acquire_keywords):
#         sentiment_label = "POSITIVE"
#         sentiment_score = 1.0
#     elif any(keyword in text.lower() for keyword in sell_keywords):
#         sentiment_label = "NEGATIVE"
#         sentiment_score = -1.0
    
#     return sentiment_label, sentiment_score

# # ---------------------------
# # Financial Data Functions
# # ---------------------------
# def get_financial_statements(ticker):
#     """Fetch financial statements for a given ticker."""
#     try:
#         company = yf.Ticker(ticker)
#         balance_sheet = company.balance_sheet
#         income_statement = company.financials
#         cashflow_statement = company.cashflow
        
#         net_income = income_statement.loc['Net Income'].iloc[0:3]
#         total_debt = balance_sheet.loc['Total Debt'].iloc[0:3]
#         revenue = income_statement.loc['Total Revenue'].iloc[0:3]
#         operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0:3]
        
#         financial_summary = {
#             "net_income": net_income.tolist(),
#             "total_debt": total_debt.tolist(),
#             "revenue": revenue.tolist(),
#             "operating_cash_flow": operating_cash_flow.tolist()
#         }
        
#         financial_summary_str = f"Revenue: {revenue}\nNet Income: {net_income}\nDebt: {total_debt}\nOperating Cash Flow: {operating_cash_flow}"
        
#         return financial_summary, financial_summary_str
#     except Exception as e:
#         logging.error(f"Error fetching financial data: {str(e)}")
#         return {"error": str(e)}, ""

# def analyze_financial_data(ticker):
#     """Analyze financial data and generate sentiment."""
#     financial_data, financial_summary_str = get_financial_statements(ticker)
#     sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    
#     sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
#     explanation = ""
#     if sentiment == "POSITIVE":
#         explanation = "Positive financial indicators showing growth and stability."
#     elif sentiment == "NEGATIVE":
#         explanation = "Negative financial indicators showing potential concerns."
#     else:
#         explanation = "Neutral financial performance indicators."
    
#     return {
#         "financial_summary": financial_data,
#         "financial_summary_str": financial_summary_str,
#         "sentiment": sentiment,
#         "sentiment_score": sentiment_score,
#         "explanation": explanation
#     }

# # ---------------------------
# # Enhanced News Fetching Functions
# # ---------------------------
# def get_financial_news_from_newsapi(ticker: str, company_name: str) -> tuple[list[str], str]:
#     """Fetch financial news from NewsAPI with strict filters."""
#     if not NEWSAPI_KEY:
#         return [], "NewsAPI key not configured"

#     base_params = {
#         "apiKey": NEWSAPI_KEY,
#         "language": "en",
#         "pageSize": 10,
#         "sortBy": "relevancy",
#         "excludeDomains": "twitter.com,facebook.com,youtube.com"
#     }

#     queries = [
#         f'"{ticker}" AND (earnings OR dividend OR stock OR shares OR analyst)',
#         f'"{company_name}" AND (financials OR revenue OR EBITDA OR guidance)',
#         f"{ticker} stock",
#         f"{company_name} financial",
#     ]

#     financial_domains = [
#         "bloomberg.com", "reuters.com", "cnbc.com", 
#         "marketwatch.com", "wsj.com", "ft.com",
#         "investing.com", "fool.com", "seekingalpha.com"
#     ]

#     all_headlines = []
    
#     for query in queries:
#         try:
#             params = {
#                 **base_params,
#                 "q": query,
#                 "domains": ",".join(financial_domains),
#             }

#             response = requests.get(
#                 "https://newsapi.org/v2/everything",
#                 params=params,
#                 timeout=15
#             )
#             response.raise_for_status()

#             articles = response.json().get("articles", [])
            
#             for article in articles:
#                 title = article.get("title", "")
#                 content = article.get("content", "").lower()
                
#                 financial_terms = {
#                     'stock', 'shares', 'earnings', 'dividend',
#                     'revenue', 'ebitda', 'analyst', 'price target',
#                     'upgrade', 'downgrade', 'guidance'
#                 }
                
#                 title_contains_ticker = (ticker.lower() in title.lower() or 
#                                       company_name.lower() in title.lower())
                
#                 content_contains_financial = any(
#                     term in content for term in financial_terms
#                 )
                
#                 if title_contains_ticker and content_contains_financial:
#                     all_headlines.append(title.strip())

#             if len(all_headlines) >= 5:
#                 break

#         except Exception as e:
#             app.logger.error(f"NewsAPI query failed: {str(e)}")
#             continue

#     if not all_headlines:
#         return [], "No financial news found"
    
#     seen = set()
#     unique_headlines = []
#     for hl in all_headlines:
#         lower_hl = hl.lower()
#         if lower_hl not in seen:
#             seen.add(lower_hl)
#             unique_headlines.append(hl)
    
#     final_headlines = unique_headlines[:5]
    
#     news_string = "Financial News:\n" + "\n".join(f"• {hl}" for hl in final_headlines)
    
#     return final_headlines, news_string

# def google_query(search_term):
#     """Generate Google News query URL."""
#     # if "news" not in search_term.lower():
#     #     search_term += " stock news"
#     # return f"https://www.google.com//search?q={re.sub(r'\s', '+', search_term)}&tbm=nws"

# def google_scrape_news(company_name):
#     """Scrape Google News as last resort."""
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
#     }
#     query = company_name + " stock news"
#     search_url = google_query(query)
#     try:
#         response = requests.get(search_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
#         headlines = []
        
#         for tag in soup.find_all("div", class_=lambda c: c and ("BNeawe" in c or "DY5T1d" in c)):
#             headline = tag.get_text().strip()
#             if headline and headline not in headlines:
#                 headlines.append(headline)
        
#         return headlines[:4], "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines[:4]))
#     except Exception as e:
#         app.logger.error(f"Google News error: {str(e)}")
#         return [], "Recent News:\nNo news available."

# def get_recent_stock_news(company_name: str, ticker: str) -> tuple[list[str], str]:
#     """Get stock news with priority: Yahoo > NewsAPI > Google."""
#     # First try Yahoo Finance
#     try:
#         news_items = yf.Ticker(ticker).news
#         headlines = []
#         for item in news_items:
#             title = item.get("title", "")
#             publisher = item.get("publisher", "")
#             if (ticker.lower() in title.lower() or 
#                 company_name.lower() in title.lower() or
#                 "bloomberg" in publisher.lower() or 
#                 "reuters" in publisher.lower()):
#                 headlines.append(title)
        
#         if headlines:
#             return headlines[:5], "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines[:5]))
#     except Exception as e:
#         app.logger.error(f"Yahoo Finance error: {str(e)}")

#     # Fallback to NewsAPI
#     headlines, news_str = get_financial_news_from_newsapi(ticker, company_name)
#     if headlines:
#         return headlines, news_str

#     # Last resort: Google News
#     return google_scrape_news(company_name)

# # ---------------------------
# # Helper Functions
# # ---------------------------
# def extract_company_and_ticker(query):
#     q_stripped = query.strip()
#     q_upper = q_stripped.upper()
#     if q_upper in SUPPORTED_TICKERS:
#         return q_upper, q_upper
#     query_lower = q_stripped.lower()
#     for company, ticker in COMPANY_NAME_TO_TICKER.items():
#         if company in query_lower:
#             return company.capitalize(), ticker
#     return None, None

# # ---------------------------
# # API Endpoints
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def get_supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'risk_levels': list(RISK_LEVELS.keys()),
#         'sectors': list(set(SECTOR_MAP.values()))
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_stock():
#     ticker = request.args.get('ticker', '').upper()
#     if not ticker:
#         full_query = request.args.get('query', '')
#         _, extracted_ticker = extract_company_and_ticker(full_query)
#         if extracted_ticker:
#             ticker = extracted_ticker.upper()
#         else:
#             return jsonify({'error': 'Invalid query; missing ticker'}), 400

#     if ticker not in SUPPORTED_TICKERS:
#         return jsonify({'error': f'Invalid ticker "{ticker}".'}), 400

#     amount = float(request.args.get('amount', user_profile['available_amount']))
    
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period="1mo")
#         info = stock.info

#         current_price = hist['Close'].iloc[-1]
#         open_price = hist['Open'].iloc[-1]
#         high_price = hist['High'].iloc[-1]
#         low_price = hist['Low'].iloc[-1]
#         previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
#         volume = hist['Volume'].iloc[-1]

#         sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
#         trend = "up" if current_price > sma_10 else "down"
#         price_change = (current_price - previous_close) / previous_close
#         volatility = (high_price - low_price) / open_price

#         confidence = 0.5
#         if trend == "up":
#             confidence += 0.2
#         confidence += min(0.2, max(-0.2, price_change*10))
#         confidence -= min(0.1, volatility*0.5)
#         confidence = min(0.95, max(0.05, confidence))

#         shares_possible = int(amount / current_price) if amount > 0 else 0

#         company_name, _ = extract_company_and_ticker(ticker)
#         news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)

#         # Sentiment analysis
#         overall_sentiment, sentiment_score = analyze_sentiment(news_string)

#         detailed_sentiments = []
#         for hl in news_list:
#             label, score = analyze_sentiment(hl)
#             detailed_sentiments.append({
#                 'headline': hl,
#                 'label': label,
#                 'score': round(score, 2)
#             })

#         financial_sentiment_data = analyze_financial_data(ticker)

#         # Decision logic
#         if trend == "up" and overall_sentiment == "POSITIVE":
#             decision = "Buy"
#         elif trend == "down" and overall_sentiment == "NEGATIVE":
#             decision = "Sell"
#         else:
#             decision = "Hold"

#         response = {
#             'ticker': ticker,
#             'current_price': round(current_price, 2),
#             'open_price': round(open_price, 2),
#             'high_price': round(high_price, 2),
#             'low_price': round(low_price, 2),
#             'previous_close': round(previous_close, 2),
#             'volume': int(volume),
#             'sma_10': round(sma_10, 2),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield', 0),
#             'price_change_pct': round(price_change * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'technical_confidence': round(confidence, 2),
#             'shares_possible': shares_possible,
#             'news': news_string,
#             'overall_news_sentiment': overall_sentiment,
#             'detailed_sentiments': detailed_sentiments,
#             'financial_statements_sentiment': financial_sentiment_data['sentiment'],
#             'financial_statements_content': financial_sentiment_data['financial_summary_str'],
#             'decision': decision,
#             'analysis': f"{ticker} shows {trend} trend with {overall_sentiment.lower()} sentiment. {decision} recommendation."
#         }
#         return jsonify(response)

#     except Exception as e:
#         app.logger.error(f"Analysis error: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)


import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import requests
import re
from bs4 import BeautifulSoup
import nltk
nltk.download('vader_lexicon')
from transformers import pipeline as _hf_pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import Dict, List
from config import NEWSAPI_KEY

app = Flask(__name__)
CORS(app)

# ---------------------------
# Configuration & Global Variables
# ---------------------------

SUPPORTED_TICKERS = [
    'AAPL', 'MSFT', 'NVDA', 'AMD', 'JNJ', 'PFE', 'JPM', 'GS',
    'KO', 'PEP', 'XOM', 'NEE', 'CVX', 'WMT', 'HD', 'GME',
    'TSLA', 'F', 'COIN', 'MRNA'
]

SECTOR_MAP = {
    'AAPL': 'tech', 'MSFT': 'tech', 'NVDA': 'tech', 'AMD': 'tech',
    'JNJ': 'healthcare', 'PFE': 'healthcare', 'JPM': 'financial', 'GS': 'financial',
    'KO': 'consumer', 'PEP': 'consumer', 'XOM': 'energy', 'NEE': 'utilities',
    'CVX': 'energy', 'WMT': 'retail', 'HD': 'retail', 'GME': 'retail',
    'TSLA': 'auto', 'F': 'auto', 'COIN': 'crypto', 'MRNA': 'biotech'
}

COMPANY_NAME_TO_TICKER = {
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'nvda': 'NVDA',
    'amd': 'AMD',
    'jnj': 'JNJ',
    'pfe': 'PFE',
    'jpm': 'JPM',
    'gs': 'GS',
    'ko': 'KO',
    'pep': 'PEP',
    'xom': 'XOM',
    'nee': 'NEE',
    'cvx': 'CVX',
    'wmt': 'WMT',
    'hd': 'HD',
    'gme': 'GME',
    'tsla': 'TSLA',
    'f': 'F',
    'coin': 'COIN',
    'mrna': 'MRNA'
}

RISK_LEVELS = {
    'low': ['JNJ', 'PFE', 'JPM', 'GS', 'KO', 'PEP', 'XOM', 'CVX', 'WMT', 'NEE'],
    'medium': ['AAPL', 'MSFT', 'HD', 'F', 'AMD'],
    'high': ['NVDA', 'TSLA', 'GME', 'COIN', 'MRNA']
}

user_profile = {
    'available_amount': 5000.0,
    'risk_preference': 'medium'
}

# ---------------------------
# Sentiment Analysis (FinBERT, RoBERTa, VADER)
# ---------------------------
finbert = _hf_pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")  # Corrected pipeline import
roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
vader = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Fixed-weight ensemble sentiment analysis using FinBERT, RoBERTa, and VADER."""
    
    # Sentiment from FinBERT
    finbert_result = finbert(text)[0]
    finbert_label = finbert_result['label']
    finbert_score = finbert_result['score']
    
    # Sentiment from RoBERTa
    roberta_result = roberta(text)[0]
    roberta_label = roberta_result['label']
    roberta_score = roberta_result['score']
    
    # Sentiment from VADER
    vader_score = vader.polarity_scores(text)['compound']
    
    # Map FinBERT result to score: Positive (1), Neutral (0), Negative (-1)
    finbert_score = 1 if finbert_label == 'Positive' else -1 if finbert_label == 'Negative' else 0
    
    # Map RoBERTa result to score: Positive (1), Neutral (0), Negative (-1)
    roberta_score = roberta_score if roberta_label == 'POS' else -roberta_score if roberta_label == 'NEG' else 0
    
    # VADER score is already a numeric value between -1 and 1 (no need for mapping)
    vader_weighted_score = vader_score  # VADER score can directly be used for weighting
    
    # Calculate the weighted score using the defined weights for each model
    weighted_score = (0.5 * finbert_score) + (0.3 * roberta_score) + (0.2 * vader_weighted_score)
    
    # Final sentiment label based on the weighted score
    if weighted_score > 0.15:
        label = 'Positive'
    elif weighted_score < -0.15:
        label = 'Negative'
    else:
        label = 'Neutral'
    
    # Return final sentiment label and weighted score
    return label, weighted_score

# ---------------------------
# Financial Analysis Engine
# ---------------------------
class FinancialAnalyzer:
    @staticmethod
    def analyze_trend(values: List[float]) -> str:
        """Deterministic trend analysis with percentages"""
        if len(values) < 2:  # Handle case with insufficient data
            return "insufficient data"
            
        change_pct = (values[0] - values[-1]) / values[-1]  # Latest vs oldest
        abs_change = abs(change_pct)
        
        if abs_change < 0.05:
            trend = "stable"
        elif change_pct > 0:
            trend = "growing" if abs_change > 0.1 else "slightly growing"
        else:
            trend = "declining" if abs_change > 0.1 else "slightly declining"
        
        return f"{trend} ({change_pct:+.1%})"

    @staticmethod
    def generate_insights(financial_data: Dict[str, List[float]]) -> Dict[str, str]:
        """Generate guaranteed structured insights"""
        insights = {
            "revenue_trend": FinancialAnalyzer.analyze_trend(financial_data['revenue']),
            "profitability_trend": FinancialAnalyzer.analyze_trend(financial_data['net_income']),
            "debt_trend": FinancialAnalyzer.analyze_trend(financial_data['total_debt']),
            "cashflow_trend": FinancialAnalyzer.analyze_trend(financial_data['operating_cash_flow']),
            "latest_revenue": f"${financial_data['revenue'][0]/1e9:.1f}B",
            "latest_net_income": f"${financial_data['net_income'][0]/1e9:.1f}B"
        }
        
        # Generate summary text
        insights['summary'] = (
            f"Revenue is {insights['revenue_trend']}. "
            f"Profits are {insights['profitability_trend']}. "
            f"Debt is {insights['debt_trend']}. "
            f"Cash flow is {insights['cashflow_trend']}."
        )
        
        return insights

# ---------------------------
# Financial Statement Functions
# ---------------------------
def get_financial_statements(ticker):
    """Fetch the financial statements for a given US ticker symbol for the last 3 years."""
    try:
        company = yf.Ticker(ticker)
        balance_sheet = company.balance_sheet
        income_statement = company.financials
        cashflow_statement = company.cashflow
        
        # Extracting data for the last 3 years (if available)
        net_income = income_statement.loc['Net Income'].iloc[0:3]
        total_debt = balance_sheet.loc['Total Debt'].iloc[0:3]
        revenue = income_statement.loc['Total Revenue'].iloc[0:3]
        operating_cash_flow = cashflow_statement.loc['Operating Cash Flow'].iloc[0:3]
        
        financial_summary = {
            "net_income": net_income.tolist(),
            "total_debt": total_debt.tolist(),
            "revenue": revenue.tolist(),
            "operating_cash_flow": operating_cash_flow.tolist()
        }
        
        financial_summary_str = f"Revenue: {revenue}\nNet Income: {net_income}\nDebt: {total_debt}\nOperating Cash Flow: {operating_cash_flow}"
        
        return financial_summary, financial_summary_str

    except Exception as e:
        logging.error(f"Error fetching financial data for {ticker}: {str(e)}")
        return {"error": str(e)}, ""

def analyze_financial_data(ticker):
    """Enhanced financial analysis with reliable insights"""
    financial_data, financial_summary_str = get_financial_statements(ticker)
    
    # Original sentiment analysis
    sentiment_text = f"Revenue: {financial_data['revenue']}, Debt: {financial_data['total_debt']}, Net Income: {financial_data['net_income']}, Operating Cash Flow: {financial_data['operating_cash_flow']}"
    sentiment, sentiment_score = analyze_sentiment(sentiment_text)
    
    # New reliable insights
    insights = FinancialAnalyzer.generate_insights(financial_data)
    
    return {
        "financial_summary": financial_data,
        "financial_summary_str": financial_summary_str,
        "sentiment": sentiment,
        "sentiment_score": round(sentiment_score, 2),
        "fundamental_insights": insights
    }

# ---------------------------
# News Fetching Functions
# ---------------------------
def google_query(search_term):
    if "news" not in search_term.lower():
        search_term += " stock news"
    url = f"https://www.google.com/search?q={search_term}&tbm=nws"
    return re.sub(r"\s", "+", url)

def google_scrape_news(company_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    query = company_name + " stock news"
    search_url = google_query(query)
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        app.logger.error(f"Error fetching news from Google: {e}")
        return [], "Recent News:\nNo news available."
    
    soup = BeautifulSoup(html, "html.parser")
    headlines = []
    for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
        headline = tag.get_text().strip()
        if headline and headline not in headlines:
            headlines.append(headline)
    if not headlines:
        for tag in soup.find_all("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}):
            headline = tag.get_text().strip()
            if headline and headline not in headlines:
                headlines.append(headline)
    if not headlines:
        for tag in soup.find_all("div", class_=lambda c: c and "DY5T1d" in c):
            headline = tag.get_text().strip()
            if headline and headline not in headlines:
                headlines.append(headline)
    if len(headlines) > 4:
        headlines = headlines[:4]
    news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
    return headlines, news_string

def get_news_from_newsapi(company_name):
    if not NEWSAPI_KEY:
        app.logger.error("NEWSAPI_KEY is not provided.")
        return [], ""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company_name + " stock",
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY,
        "language": "en",
        "pageSize": 4
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
        if headlines:
            news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
            return headlines, news_string
    except Exception as e:
        app.logger.error(f"NewsAPI error: {e}")
    return [], ""

def get_recent_stock_news(company_name, ticker):
    stock = yf.Ticker(ticker)
    try:
        news_items = stock.news
    except Exception:
        news_items = []
    headlines = []
    if news_items:
        for item in news_items:
            if "title" in item and item["title"]:
                headlines.append(item["title"])
    if not headlines:
        headlines, news_string = get_news_from_newsapi(company_name)
        if not headlines:
            headlines, news_string = google_scrape_news(company_name)
    else:
        news_string = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
    return headlines, news_string

# ---------------------------
# Company/Ticker Extraction
# ---------------------------
def extract_company_and_ticker(query):
    q_stripped = query.strip()
    q_upper = q_stripped.upper()
    if q_upper in SUPPORTED_TICKERS:
        return q_upper, q_upper
    query_lower = q_stripped.lower()
    for company, ticker in COMPANY_NAME_TO_TICKER.items():
        if company in query_lower:
            return company.capitalize(), ticker
    return None, None

def generate_decision(trend: str, confidence: float, news_sentiment: str, financial_insights: dict) -> dict:
    """Enhanced decision logic with financial insights"""
    # Basic rules
    if trend == "up" and news_sentiment == "Positive":
        action = "Buy"
        reasoning = "Strong technical uptrend with positive news sentiment"
    elif trend == "down" and news_sentiment == "Negative":
        action = "Sell" 
        reasoning = "Downtrend confirmed with negative news sentiment"
    else:
        action = "Hold"
        reasoning = "Mixed signals - requires further analysis"

    # Enhance with financial insights
    if "declining" in financial_insights['profitability_trend'] and action == "Buy":
        action = "Hold"
        reasoning += ", but profits are declining"
    elif "growing" in financial_insights['revenue_trend'] and action == "Hold":
        reasoning += ", though revenue is growing"
    
    return {
        'action': action,
        'reasoning': reasoning + f". Fundamentals: {financial_insights['summary']}"
    }

# ---------------------------
# API Endpoints
# ---------------------------
@app.route('/api/stocks', methods=['GET'])
def get_supported_stocks():
    return jsonify({
        'tickers': SUPPORTED_TICKERS,
        'risk_levels': list(RISK_LEVELS.keys()),
        'sectors': list(set(SECTOR_MAP.values()))
    })

@app.route('/api/analyze', methods=['GET'])
def analyze_stock():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        full_query = request.args.get('query', '')
        _, extracted_ticker = extract_company_and_ticker(full_query)
        if extracted_ticker:
            ticker = extracted_ticker.upper()
        else:
            return jsonify({'error': 'Invalid query; missing ticker'}), 400

    if ticker not in SUPPORTED_TICKERS:
        return jsonify({'error': f'Invalid ticker "{ticker}".'}), 400

    amount = float(request.args.get('amount', user_profile['available_amount']))
    
    try:
        # Technical Analysis
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        info = stock.info

        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[-1]
        high_price = hist['High'].iloc[-1]
        low_price = hist['Low'].iloc[-1]
        previous_close = hist['Close'].iloc[-2] if len(hist)>1 else current_price
        volume = hist['Volume'].iloc[-1]

        sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
        trend = "up" if current_price > sma_10 else "down"
        price_change = (current_price - previous_close) / previous_close
        volatility = (high_price - low_price) / open_price

        confidence = 0.5
        if trend == "up":
            confidence += 0.2
        confidence += min(0.2, max(-0.2, price_change*10))
        confidence -= min(0.1, volatility*0.5)
        confidence = min(0.95, max(0.05, confidence))

        shares_possible = int(amount / current_price) if amount > 0 else 0

        # News Analysis
        company_name, _ = extract_company_and_ticker(ticker)
        news_list, news_string = get_recent_stock_news(company_name or ticker, ticker)
        overall_sentiment, news_sentiment_score = analyze_sentiment(news_string)
        
        detailed_sentiments = []
        for hl in news_list:
            label, score = analyze_sentiment(hl)
            detailed_sentiments.append({
                'headline': hl,
                'label': label,
                'score': round(score, 2)
            })

        # Financial Analysis
        financial_data = analyze_financial_data(ticker)
        financial_insights = financial_data['fundamental_insights']

        # Generate Decision
        decision = generate_decision(
            trend=trend,
            confidence=confidence,
            news_sentiment=overall_sentiment,
            financial_insights=financial_insights
        )

        # Prepare Response
        response = {
            'ticker': ticker,
            'current_price': round(current_price, 2),
            'open_price': round(open_price, 2),
            'high_price': round(high_price, 2),
            'low_price': round(low_price, 2),
            'previous_close': round(previous_close, 2),
            'volume': int(volume),
            'sma_10': round(sma_10, 2),
            'pe_ratio': info.get('trailingPE'),
            'dividend_yield': info.get('dividendYield', 0),
            'price_change_pct': round(price_change * 100, 2),
            'volatility_pct': round(volatility * 100, 2),
            'trend': trend,
            'technical_confidence': round(confidence, 2),
            'shares_possible': shares_possible,
            'news': news_string,
            'overall_news_sentiment': overall_sentiment,
            'detailed_sentiments': detailed_sentiments,
            'financial_statements_sentiment': financial_data['sentiment'],
            'financial_statements_content': financial_data['financial_summary_str'],
            'fundamental_insights': financial_insights,
            'decision': decision['action'],
            'analysis': decision['reasoning']
        }
        return jsonify(response)

    except Exception as e:
        logging.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


############# ABOVE valid#############################


# import os
# import logging
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import re
# from bs4 import BeautifulSoup
# import nltk
# nltk.download('vader_lexicon')
# from transformers import pipeline as _hf_pipeline
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from typing import Dict, List, Tuple

# app = Flask(__name__)
# CORS(app)

# # ---------------------------
# # Configuration & Globals
# # ---------------------------
# NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"

# SUPPORTED_TICKERS = [
#     'AAPL','MSFT','NVDA','AMD','JNJ','PFE','JPM','GS',
#     'KO','PEP','XOM','NEE','CVX','WMT','HD','GME',
#     'TSLA','F','COIN','MRNA'
# ]

# SECTOR_MAP = {
#     'AAPL':'tech','MSFT':'tech','NVDA':'tech','AMD':'tech',
#     'JNJ':'healthcare','PFE':'healthcare','JPM':'financial','GS':'financial',
#     'KO':'consumer','PEP':'consumer','XOM':'energy','NEE':'utilities',
#     'CVX':'energy','WMT':'retail','HD':'retail','GME':'retail',
#     'TSLA':'auto','F':'auto','COIN':'crypto','MRNA':'biotech'
# }

# COMPANY_NAME_TO_TICKER = {
#     'apple':'AAPL','microsoft':'MSFT','nvidia':'NVDA','amd':'AMD',
#     'johnson & johnson':'JNJ','jnj':'JNJ','pfizer':'PFE','jpmorgan':'JPM',
#     'goldman sachs':'GS','coca cola':'KO','pepsi':'PEP','exxon':'XOM',
#     'next era energy':'NEE','chevron':'CVX','walmart':'WMT','home depot':'HD',
#     'gamestop':'GME','tesla':'TSLA','ford':'F','coinbase':'COIN','moderna':'MRNA',
#     'appl':'AAPL','micro':'MSFT','nvdia':'NVDA','xoom':'XOM','wallmart':'WMT',
#     'tesa':'TSLA','ford motor':'F','coin base':'COIN','modern':'MRNA'
# }
# _normalized_company_map = {
#     re.sub(r'[^a-z0-9\s]','',k):v for k,v in COMPANY_NAME_TO_TICKER.items()
# }

# RISK_LEVELS = {
#     'low':['JNJ','PFE','JPM','GS','KO','PEP','XOM','CVX','WMT','NEE'],
#     'medium':['AAPL','MSFT','HD','F','AMD'],
#     'high':['NVDA','TSLA','GME','COIN','MRNA']
# }

# RISK_BASED_RECOMMENDATIONS = {
#     'low': [
#         {'ticker':'JNJ','allocation':0.30,'reason':'Stable healthcare dividends'},
#         {'ticker':'KO','allocation':0.25,'reason':'Consumer staple'},
#         {'ticker':'WMT','allocation':0.25,'reason':'Resilient retail'},
#         {'ticker':'NEE','allocation':0.20,'reason':'Renewables utility'}
#     ],
#     'medium': [
#         {'ticker':'AAPL','allocation':0.35,'reason':'Tech ecosystem'},
#         {'ticker':'MSFT','allocation':0.35,'reason':'Cloud leader'},
#         {'ticker':'JPM','allocation':0.20,'reason':'Banking stability'},
#         {'ticker':'HD','allocation':0.10,'reason':'Home improvement'}
#     ],
#     'high': [
#         {'ticker':'NVDA','allocation':0.40,'reason':'AI/GPU growth'},
#         {'ticker':'TSLA','allocation':0.30,'reason':'EV upside'},
#         {'ticker':'MRNA','allocation':0.20,'reason':'mRNA biotech'},
#         {'ticker':'COIN','allocation':0.10,'reason':'Crypto exposure'}
#     ]
# }

# user_profile = {'available_amount':5000.0,'risk_preference':'medium'}

# # ---------------------------
# # Sentiment Analysis
# # ---------------------------
# finbert = _hf_pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")
# roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
# vader = SentimentIntensityAnalyzer()

# def analyze_sentiment(text: str) -> Tuple[str, float]:
#     try:
#         fb = finbert(text)[0]
#         fb_score = 1 if fb['label']=='Positive' else -1 if fb['label']=='Negative' else 0
#         rb = roberta(text)[0]
#         rb_score = rb['score'] if rb['label']=='POS' else -rb['score'] if rb['label']=='NEG' else 0
#         vd = vader.polarity_scores(text)['compound']
#         score = 0.5*fb_score + 0.3*rb_score + 0.2*vd
#         if score > 0.15: return 'Positive', score
#         if score < -0.15: return 'Negative', score
#         return 'Neutral', score
#     except:
#         return 'Neutral', 0.0

# # ---------------------------
# # Financial Analysis
# # ---------------------------
# class FinancialAnalyzer:
#     @staticmethod
#     def analyze_trend(vals: List[float]) -> str:
#         if len(vals) < 2: return "insufficient data"
#         change = (vals[0] - vals[-1]) / vals[-1]
#         pct = abs(change)
#         if pct < 0.05:
#             trend = "stable"
#         elif change > 0:
#             trend = "growing" if pct > 0.1 else "slightly growing"
#         else:
#             trend = "declining" if pct > 0.1 else "slightly declining"
#         return f"{trend} ({change:+.1%})"

#     @staticmethod
#     def generate_insights(data: Dict[str, List[float]]) -> Dict[str, str]:
#         insights = {
#             'revenue_trend': FinancialAnalyzer.analyze_trend(data['revenue']),
#             'profitability_trend': FinancialAnalyzer.analyze_trend(data['net_income']),
#             'debt_trend': FinancialAnalyzer.analyze_trend(data['total_debt']),
#             'cashflow_trend': FinancialAnalyzer.analyze_trend(data['operating_cash_flow']),
#             'latest_revenue': f"${data['revenue'][0]/1e9:.1f}B",
#             'latest_net_income': f"${data['net_income'][0]/1e9:.1f}B"
#         }
#         insights['summary'] = (
#             f"Revenue is {insights['revenue_trend']}. "
#             f"Profits are {insights['profitability_trend']}. "
#             f"Debt is {insights['debt_trend']}. "
#             f"Cash flow is {insights['cashflow_trend']}."
#         )
#         return insights

# def get_financial_statements(ticker: str) -> Tuple[Dict[str, List[float]], str]:
#     try:
#         c = yf.Ticker(ticker)
#         fin, bal, cf = c.financials, c.balance_sheet, c.cashflow
#         ni  = fin.loc['Net Income'].iloc[:3].tolist()
#         td  = bal.loc['Total Debt'].iloc[:3].tolist()
#         rv  = fin.loc['Total Revenue'].iloc[:3].tolist()
#         ocf = cf.loc['Operating Cash Flow'].iloc[:3].tolist()
#         summary = f"Revenue: {rv}\nNet Income: {ni}\nDebt: {td}\nOperating CF: {ocf}"
#         return {'net_income':ni,'total_debt':td,'revenue':rv,'operating_cash_flow':ocf}, summary
#     except:
#         return {'net_income':[],'total_debt':[],'revenue':[],'operating_cash_flow':[]}, ''

# def analyze_financial_data(ticker: str) -> Dict:
#     data, summary = get_financial_statements(ticker)
#     txt = f"Revenue:{data['revenue']},Debt:{data['total_debt']},NI:{data['net_income']},OCF:{data['operating_cash_flow']}"
#     sent, _ = analyze_sentiment(txt)
#     insights = FinancialAnalyzer.generate_insights(data)
#     return {
#         'financial_summary': data,
#         'financial_summary_str': summary,
#         'sentiment': sent,
#         'fundamental_insights': insights
#     }

# # ---------------------------
# # News Fetching
# # ---------------------------
# def google_query(q: str) -> str:
#     if 'news' not in q.lower():
#         q += ' stock news'
#     return f"https://www.google.com/search?q={'+'.join(q.split())}&tbm=nws"

# def google_scrape_news(name: str) -> Tuple[List[str], str]:
#     try:
#         r = requests.get(google_query(name), headers={'User-Agent':'Mozilla/5.0'}, timeout=5)
#         r.raise_for_status()
#         soup = BeautifulSoup(r.text, 'html.parser')
#         heads = [t.get_text().strip() for t in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')][:4]
#     except:
#         heads = []
#     s = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(heads))
#     return heads, s

# def get_news_from_newsapi(name: str) -> Tuple[List[str], str]:
#     if not NEWSAPI_KEY:
#         return [], ''
#     params = {'q': f"{name} stock", 'apiKey': NEWSAPI_KEY, 'pageSize': 4}
#     try:
#         js = requests.get("https://newsapi.org/v2/everything", params=params, timeout=5).json()
#         heads = [a['title'] for a in js.get('articles', [])][:4]
#         s = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(heads))
#         return heads, s
#     except:
#         return [], ''

# def get_recent_stock_news(name: str, ticker: str) -> Tuple[List[str], str]:
#     try:
#         yf_news = yf.Ticker(ticker).news or []
#         heads = [i['title'] for i in yf_news if i.get('title')][:4]
#     except:
#         heads = []
#     if not heads:
#         heads, s = get_news_from_newsapi(name)
#         if not heads:
#             heads, s = google_scrape_news(name)
#     else:
#         s = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(heads))
#     return heads, s

# # ---------------------------
# # Extraction & Decision
# # ---------------------------
# def extract_company_and_ticker(q: str) -> Tuple[str, str]:
#     clean = re.sub(r'[^a-z0-9\s]', '', q.lower())
#     for w in clean.split():
#         if w.upper() in SUPPORTED_TICKERS:
#             return w.upper(), w.upper()
#     for k, v in _normalized_company_map.items():
#         if k and k in clean:
#             return k, v
#     return None, None

# def generate_decision(trend, conf, news_sent, fin_ins) -> Dict:
#     if trend == 'up' and news_sent == 'Positive':
#         act, rs = 'Buy', 'Uptrend & positive news'
#     elif trend == 'down' and news_sent == 'Negative':
#         act, rs = 'Sell', 'Downtrend & negative news'
#     else:
#         act, rs = 'Hold', 'Mixed signals'
#     if 'declining' in fin_ins['profitability_trend'] and act == 'Buy':
#         act = 'Hold'
#         rs += ', profits declining'
#     elif 'growing' in fin_ins['revenue_trend'] and act == 'Hold':
#         rs += ', revenue growing'
#     return {'action': act, 'reasoning': f"{rs}. Fundamentals: {fin_ins['summary']}"}

# def get_recommendations(amount: float, risk: str) -> Dict:
#     recs = RISK_BASED_RECOMMENDATIONS.get(risk, [])
#     recommendations = []
#     allocation_plan = []
#     total = 0.0

#     for r in recs:
#         tkr       = r['ticker']
#         alloc_amt = amount * r['allocation']
#         hist      = yf.Ticker(tkr).history(period='1mo')
#         price     = hist['Close'].iloc[-1]
#         sma10     = hist['Close'].rolling(10).mean().iloc[-1]
#         trend     = 'up' if price > sma10 else 'down'
#         shares    = round(alloc_amt / price, 2) if price else 0
#         pct       = round(r['allocation'] * 100, 1)

#         # build recommendation entry
#         recommendations.append({
#             'ticker': tkr,
#             'allocation_pct': pct,
#             'allocation_amt': round(alloc_amt, 2),
#             'price': round(price, 2),
#             'shares': shares,
#             'trend': trend,
#             'reason': r['reason']
#         })

#         # build allocation_plan entry
#         allocation_plan.append({
#             'ticker': tkr,
#             'amount': round(alloc_amt, 2),
#             'shares': shares,
#             'percentage': pct
#         })

#         total += alloc_amt

#     return {
#         'total_amount': amount,
#         'risk_level': risk,
#         'invested': round(total, 2),
#         'cash_left': round(amount - total, 2),
#         'recommendations': recommendations,
#         'allocation_plan': allocation_plan
#     }

# def perform_analysis(ticker: str, amount: float) -> Dict:
#     try:
#         st = yf.Ticker(ticker)
#         h  = st.history(period='1mo')
#         cp, op, hi, lo = h['Close'].iloc[-1], h['Open'].iloc[-1], h['High'].iloc[-1], h['Low'].iloc[-1]
#         prev           = h['Close'].iloc[-2] if len(h)>1 else cp
#         vol            = int(h['Volume'].iloc[-1])
#         sma10          = h['Close'].rolling(10).mean().iloc[-1]

#         trend      = 'up' if cp > sma10 else 'down'
#         change_pct = (cp - prev) / prev
#         volatility = (hi - lo) / op if op else 0

#         confidence = min(
#             0.95,
#             max(
#                 0.05,
#                 0.5
#                 + (0.2 if trend == 'up' else -0.2)
#                 + min(0.2, max(-0.2, change_pct * 10))
#                 - min(0.1, volatility * 0.5)
#             )
#         )
#         shares = int(amount / cp) if amount > 0 else 0

#         name = next((k for k, v in COMPANY_NAME_TO_TICKER.items() if v == ticker), ticker)
#         news_list, news_str = get_recent_stock_news(name.capitalize(), ticker)
#         overall_sent, _    = analyze_sentiment(news_str)

#         fin     = analyze_financial_data(ticker)
#         fin_ins = fin['fundamental_insights']
#         dec     = generate_decision(trend, confidence, overall_sent, fin_ins)

#         return {
#             'ticker': ticker,
#             'current_price': round(cp, 2),
#             'open_price': round(op, 2),
#             'high_price': round(hi, 2),
#             'low_price': round(lo, 2),
#             'previous_close': round(prev, 2),
#             'volume': vol,
#             'sma_10': round(sma10, 2),
#             'price_change_pct': round(change_pct * 100, 2),
#             'volatility_pct': round(volatility * 100, 2),
#             'trend': trend,
#             'confidence': round(confidence, 2),
#             'technical_confidence': round(confidence, 2),   # <-- added
#             'shares_possible': shares,
#             'pe_ratio': st.info.get('trailingPE'),
#             'dividend_yield': st.info.get('dividendYield', 0),
#             'news': news_str,
#             'overall_news_sentiment': overall_sent,
#             'financial_statements_sentiment': fin['sentiment'],
#             'financial_statements_content': fin['financial_summary_str'],
#             'fundamental_insights': fin_ins,
#             'decision': dec['action'],
#             'analysis': dec['reasoning']
#         }

#     except Exception as e:
#         logging.error(f"Analysis error for {ticker}: {e}")
#         return {'error': str(e)}

# # ---------------------------
# # API Endpoints
# # ---------------------------
# @app.route('/api/stocks', methods=['GET'])
# def supported_stocks():
#     return jsonify({
#         'tickers': SUPPORTED_TICKERS,
#         'sectors': SECTOR_MAP,
#         'risk_levels': list(RISK_LEVELS.keys())
#     })

# @app.route('/api/analyze', methods=['GET'])
# def analyze_endpoint():
#     raw_t = request.args.get('ticker','').strip()
#     qry   = request.args.get('query','').strip()
#     amt   = float(request.args.get('amount', user_profile['available_amount']))

#     if raw_t and raw_t.upper() not in SUPPORTED_TICKERS:
#         qry, raw_t = raw_t, ''

#     # Static trigger for recommendations
#     if 'recommend' in qry.lower():
#         risk = request.args.get('risk', user_profile['risk_preference']).lower()
#         if risk not in RISK_LEVELS:
#             return jsonify({'error': f"Invalid risk: choose {list(RISK_LEVELS.keys())}"}), 400
#         return jsonify(get_recommendations(amt, risk))

#     ticker = raw_t.upper() if raw_t.upper() in SUPPORTED_TICKERS else None
#     if not ticker and qry:
#         _, ticker = extract_company_and_ticker(qry)
#     if not ticker:
#         return jsonify({
#             'error':'Could not identify stock',
#             'suggestions':['?ticker=AAPL','?query="recommend" to get portfolio']
#         }), 400

#     result = perform_analysis(ticker, amt)
#     return jsonify(result), (200 if 'error' not in result else 500)

# @app.route('/api/recommend', methods=['GET'])
# def recommend_endpoint():
#     amt  = float(request.args.get('amount', user_profile['available_amount']))
#     risk = request.args.get('risk', user_profile['risk_preference']).lower()
#     if risk not in RISK_LEVELS:
#         return jsonify({'error': f"Invalid risk: choose {list(RISK_LEVELS.keys())}"}), 400
#     return jsonify(get_recommendations(amt, risk))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)
