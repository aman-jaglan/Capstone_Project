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
# from config import NEWSAPI_KEY

NEWS_API_KEY = "632d8de4fdb040e9a6cac989633a303e"  # Replace with your actual NewsAPI key.

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
    if not NEWS_API_KEY:
        app.logger.error("NEWSAPI_KEY is not provided.")
        return [], ""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company_name + " stock",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
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
    app.run(port=5001, debug=True, use_reloader=False)