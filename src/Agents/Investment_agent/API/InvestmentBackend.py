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

app = Flask(__name__)
CORS(app)

# ---------------------------
# Configuration & Global Variables
# ---------------------------
# Replace with your actual NewsAPI key.
NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"  

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

# Mapping of common company names for natural language queries.
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

def extract_company_and_ticker(query):
    """
    If the query exactly matches a supported ticker (case-insensitive), return it.
    Otherwise, search for any supported company name.
    """
    q_stripped = query.strip()
    q_upper = q_stripped.upper()
    if q_upper in SUPPORTED_TICKERS:
        return q_upper, q_upper
    query_lower = q_stripped.lower()
    for company, ticker in COMPANY_NAME_TO_TICKER.items():
        if company in query_lower:
            return company.capitalize(), ticker
    return None, None

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
# News Fetching Functions
# ---------------------------
def google_query(search_term):
    """
    Construct a Google news search URL (using tbm=nws).
    """
    if "news" not in search_term.lower():
        search_term += " stock news"
    url = f"https://www.google.com/search?q={search_term}&tbm=nws"
    return re.sub(r"\s", "+", url)

def google_scrape_news(company_name):
    """
    Fallback method: Scrape headlines from Google News search results.
    Tries multiple selectors to capture headlines.
    """
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
    # Primary selector
    for tag in soup.find_all("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}):
        headline = tag.get_text().strip()
        if headline and headline not in headlines:
            headlines.append(headline)
    # Fallback selectors
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
    """
    Use NewsAPI to fetch recent news headlines.
    """
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
    """
    Attempt to fetch news using yfinance’s built‑in news first.
    If none are returned, then try NewsAPI and fall back to Google scraping.
    """
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
# FinBERT-based Sentiment Analysis
# ---------------------------
from transformers import pipeline
finbert = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

def analyze_news_sentiment(news_list):
    """
    Use FinBERT to analyze each headline.
    Returns a list of sentiment dictionaries.
    """
    sentiments = []
    for headline in news_list:
        try:
            result = finbert(headline)[0]
            sentiments.append(result)
        except Exception:
            sentiments.append({"label": "Neutral", "score": 0.0})
    return sentiments

def aggregate_sentiments(sentiments):
    """
    Aggregates individual sentiment scores to produce an overall sentiment.
    """
    if not sentiments:
        return "Neutral"
    positive = sum(s['score'] for s in sentiments if s['label'].lower() == 'positive')
    negative = sum(s['score'] for s in sentiments if s['label'].lower() == 'negative')
    neutral = sum(s['score'] for s in sentiments if s['label'].lower() == 'neutral')
    total = positive + negative + neutral
    pos_pct = positive / total if total > 0 else 0
    neg_pct = negative / total if total > 0 else 0
    if pos_pct > neg_pct:
        return "Positive"
    elif neg_pct > pos_pct:
        return "Negative"
    else:
        return "Neutral"

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
    # First try to get ticker from "ticker" parameter.
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        full_query = request.args.get('query', '')
        company, extracted_ticker = extract_company_and_ticker(full_query)
        if extracted_ticker:
            ticker = extracted_ticker.upper()
        else:
            return jsonify({'error': 'Invalid query; no supported company name found. Try one of: ' + ", ".join(SUPPORTED_TICKERS)}), 400

    if ticker not in SUPPORTED_TICKERS:
        return jsonify({'error': f'Invalid ticker "{ticker}". Try: ' + ", ".join(SUPPORTED_TICKERS)}), 400

    amount = float(request.args.get('amount', user_profile['available_amount']))
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        info = stock.info

        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[-1]
        high_price = hist['High'].iloc[-1]
        low_price = hist['Low'].iloc[-1]
        previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        volume = hist['Volume'].iloc[-1]

        sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
        trend = "up" if current_price > sma_10 else "down"
        price_change = (current_price - previous_close) / previous_close
        volatility = (high_price - low_price) / open_price

        confidence = 0.5
        if trend == "up":
            confidence += 0.2
        confidence += min(0.2, max(-0.2, price_change * 10))
        confidence -= min(0.1, volatility * 0.5)
        confidence = min(0.95, max(0.05, confidence))

        shares_possible = int(amount / current_price) if amount > 0 else 0

        company_name = info.get('shortName', ticker)
        news_list, news_string = get_recent_stock_news(company_name, ticker)
        sentiments = analyze_news_sentiment(news_list)
        overall_sentiment = aggregate_sentiments(sentiments)

        # Rule-based decision
        if trend == "up" and overall_sentiment == "Positive":
            decision = "Buy"
        elif trend == "down" and overall_sentiment == "Negative":
            decision = "Sell"
        else:
            decision = "Hold"

        # ---- Added Detailed Technical Explanation ----
        detailed_explanation = "\n\n📊 Detailed Technical Explanation:\n"
        detailed_explanation += f"🔸 10-Day SMA: ${sma_10:.2f}. This is the average closing price over the last 10 days. "
        if current_price < sma_10:
            detailed_explanation += f"Since the current price (${current_price:.2f}) is below the SMA, it indicates a DOWN trend.\n"
        else:
            detailed_explanation += f"Since the current price (${current_price:.2f}) is above the SMA, it indicates an UP trend.\n"
        pe_ratio = info.get('trailingPE', 'N/A')
        detailed_explanation += f"🔸 PE Ratio: {pe_ratio}. The PE ratio typically ranges between 15 and 30 for mature companies. A value in this range suggests moderate valuation.\n"
        dividend_yield = info.get('dividendYield', 0)
        detailed_explanation += f"🔸 Dividend Yield: {(dividend_yield * 100):.2f}%. Normally, dividend yields are below 5%; an unusually high yield may indicate potential red flags.\n"
        detailed_explanation += f"🔸 Price Change: {price_change*100:.2f}%. This is the percentage change from the previous close. "
        if price_change < 0:
            detailed_explanation += "A negative value indicates a recent price decline.\n"
        else:
            detailed_explanation += "A positive value indicates an increase in price.\n"
        detailed_explanation += f"🔸 Volatility: {volatility*100:.2f}%. This measures how much the stock price fluctuates during the trading day; higher volatility means larger price swings.\n"
        # ---- End of Detailed Explanation ----

        analysis = (
            f"Based on technical analysis, {ticker} is trading at ${current_price:.2f} with a {trend.upper()} trend "
            f"and a technical confidence score of {confidence:.2f}. The 10-Day SMA is ${sma_10:.2f}, with a price change of {price_change*100:.2f}% "
            f"and volatility of {volatility*100:.2f}%. Recent news sentiment is {overall_sentiment}. With an investment amount of ${amount:.2f}, "
            f"you could purchase up to {shares_possible} shares. Overall, the recommendation is to {decision}. Please consider your risk tolerance before making any decision."
        )
        analysis += detailed_explanation

        response = {
            'ticker': ticker,
            'current_price': round(current_price, 2),
            'open_price': round(open_price, 2),
            'high_price': round(high_price, 2),
            'low_price': round(low_price, 2),
            'previous_close': round(previous_close, 2),
            'volume': int(volume),
            'sma_10': round(sma_10, 2),
            'pe_ratio': pe_ratio,
            'dividend_yield': dividend_yield,
            'price_change_pct': round(price_change * 100, 2),
            'volatility_pct': round(volatility * 100, 2),
            'trend': trend,
            'technical_confidence': round(confidence, 2),
            'shares_possible': shares_possible,
            'news': news_string,
            'overall_news_sentiment': overall_sentiment,
            'analysis': analysis
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend', methods=['GET'])
def recommend_stocks():
    try:
        amount = float(request.args.get('amount', user_profile['available_amount']))
        risk = request.args.get('risk', user_profile['risk_preference'])
        if risk not in RISK_LEVELS:
            return jsonify({'error': 'Invalid risk level'}), 400

        candidates = []
        for ticker in RISK_LEVELS[risk]:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1mo")
                current_price = hist['Close'].iloc[-1]
                previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                sma_10 = hist['Close'].rolling(10).mean().iloc[-1]
                price_change = (current_price - previous_close) / previous_close
                price_change_3d = (current_price - hist['Close'].iloc[-4]) / hist['Close'].iloc[-4] if len(hist) >= 4 else 0
                is_uptrend = current_price > sma_10
                is_recovering = price_change_3d > 0

                confidence = 0.5
                if is_uptrend:
                    confidence += 0.3
                elif not is_recovering:
                    confidence -= 0.1
                else:
                    confidence += 0.1
                confidence += min(0.2, price_change_3d * 3)
                confidence = max(0.2, min(0.9, confidence))
                
                candidates.append({
                    'ticker': ticker,
                    'price': round(current_price, 2),
                    'confidence': confidence,
                    'trend': 'up' if is_uptrend else ('recovering' if is_recovering else 'down'),
                    'sector': SECTOR_MAP.get(ticker, 'other')
                })
            except Exception as e:
                app.logger.error(f"Error processing {ticker}: {str(e)}")
                continue

        candidates.sort(key=lambda x: x['confidence'], reverse=True)
        top_picks = candidates[:3]
        if not top_picks:
            return jsonify({
                'status': 'success',
                'recommendations': [],
                'allocation_plan': []
            })

        total_confidence = sum(x['confidence'] for x in top_picks)
        allocation = []
        for stock in top_picks:
            weight = stock['confidence'] / total_confidence
            allocated = round(amount * weight, 2)
            shares = max(1, int(allocated / stock['price']))
            allocation.append({
                'ticker': stock['ticker'],
                'amount': allocated,
                'shares': shares,
                'percentage': round(weight * 100, 1)
            })
            stock['shares'] = shares

        return jsonify({
            'status': 'success',
            'recommendations': top_picks,
            'allocation_plan': allocation
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to generate recommendations'
        }), 500

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    try:
        data = request.get_json()
        user_profile['available_amount'] = float(data.get('amount', 5000.0))
        user_profile['risk_preference'] = data.get('risk', 'medium')
        return jsonify({'status': 'profile_updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)



