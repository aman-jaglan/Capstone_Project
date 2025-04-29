
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
from typing import Dict, List, Tuple

app = Flask(__name__)
CORS(app)

# ---------------------------
# Configuration & Globals
# ---------------------------
NEWSAPI_KEY = "4c310cb414224d468ee9087dd9f208d6"

SUPPORTED_TICKERS = [
    'AAPL','MSFT','NVDA','AMD','JNJ','PFE','JPM','GS',
    'KO','PEP','XOM','NEE','CVX','WMT','HD','GME',
    'TSLA','F','COIN','MRNA'
]

SECTOR_MAP = {
    'AAPL':'tech','MSFT':'tech','NVDA':'tech','AMD':'tech',
    'JNJ':'healthcare','PFE':'healthcare','JPM':'financial','GS':'financial',
    'KO':'consumer','PEP':'consumer','XOM':'energy','NEE':'utilities',
    'CVX':'energy','WMT':'retail','HD':'retail','GME':'retail',
    'TSLA':'auto','F':'auto','COIN':'crypto','MRNA':'biotech'
}

COMPANY_NAME_TO_TICKER = {
    'apple':'AAPL','microsoft':'MSFT','nvidia':'NVDA','amd':'AMD',
    'johnson & johnson':'JNJ','jnj':'JNJ','pfizer':'PFE','jpmorgan':'JPM',
    'goldman sachs':'GS','coca cola':'KO','pepsi':'PEP','exxon':'XOM',
    'next era energy':'NEE','chevron':'CVX','walmart':'WMT','home depot':'HD',
    'gamestop':'GME','tesla':'TSLA','ford':'F','coinbase':'COIN','moderna':'MRNA',
    'appl':'AAPL','micro':'MSFT','nvdia':'NVDA','xoom':'XOM','wallmart':'WMT',
    'tesa':'TSLA','ford motor':'F','coin base':'COIN','modern':'MRNA'
}
_normalized_company_map = {
    re.sub(r'[^a-z0-9\s]','',k):v for k,v in COMPANY_NAME_TO_TICKER.items()
}

RISK_LEVELS = {
    'low':['JNJ','PFE','JPM','GS','KO','PEP','XOM','CVX','WMT','NEE'],
    'medium':['AAPL','MSFT','HD','F','AMD'],
    'high':['NVDA','TSLA','GME','COIN','MRNA']
}

RISK_BASED_RECOMMENDATIONS = {
    'low': [
        {'ticker':'JNJ','allocation':0.30,'reason':'Stable healthcare dividends'},
        {'ticker':'KO','allocation':0.25,'reason':'Consumer staple'},
        {'ticker':'WMT','allocation':0.25,'reason':'Resilient retail'},
        {'ticker':'NEE','allocation':0.20,'reason':'Renewables utility'}
    ],
    'medium': [
        {'ticker':'AAPL','allocation':0.35,'reason':'Tech ecosystem'},
        {'ticker':'MSFT','allocation':0.35,'reason':'Cloud leader'},
        {'ticker':'JPM','allocation':0.20,'reason':'Banking stability'},
        {'ticker':'HD','allocation':0.10,'reason':'Home improvement'}
    ],
    'high': [
        {'ticker':'NVDA','allocation':0.40,'reason':'AI/GPU growth'},
        {'ticker':'TSLA','allocation':0.30,'reason':'EV upside'},
        {'ticker':'MRNA','allocation':0.20,'reason':'mRNA biotech'},
        {'ticker':'COIN','allocation':0.10,'reason':'Crypto exposure'}
    ]
}

user_profile = {'available_amount':5000.0,'risk_preference':'medium'}

# ---------------------------
# Sentiment Analysis
# ---------------------------
finbert = _hf_pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")
roberta = _hf_pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
vader = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> Tuple[str, float]:
    try:
        fb = finbert(text)[0]
        fb_score = 1 if fb['label']=='Positive' else -1 if fb['label']=='Negative' else 0
        rb = roberta(text)[0]
        rb_score = rb['score'] if rb['label']=='POS' else -rb['score'] if rb['label']=='NEG' else 0
        vd = vader.polarity_scores(text)['compound']
        score = 0.5*fb_score + 0.3*rb_score + 0.2*vd
        if score > 0.15: return 'Positive', score
        if score < -0.15: return 'Negative', score
        return 'Neutral', score
    except:
        return 'Neutral', 0.0

# ---------------------------
# Financial Analysis
# ---------------------------
class FinancialAnalyzer:
    @staticmethod
    def analyze_trend(vals: List[float]) -> str:
        if len(vals) < 2: return "insufficient data"
        change = (vals[0] - vals[-1]) / vals[-1]
        pct = abs(change)
        if pct < 0.05:
            trend = "stable"
        elif change > 0:
            trend = "growing" if pct > 0.1 else "slightly growing"
        else:
            trend = "declining" if pct > 0.1 else "slightly declining"
        return f"{trend} ({change:+.1%})"

    @staticmethod
    def generate_insights(data: Dict[str, List[float]]) -> Dict[str, str]:
        insights = {
            'revenue_trend': FinancialAnalyzer.analyze_trend(data['revenue']),
            'profitability_trend': FinancialAnalyzer.analyze_trend(data['net_income']),
            'debt_trend': FinancialAnalyzer.analyze_trend(data['total_debt']),
            'cashflow_trend': FinancialAnalyzer.analyze_trend(data['operating_cash_flow']),
            'latest_revenue': f"${data['revenue'][0]/1e9:.1f}B",
            'latest_net_income': f"${data['net_income'][0]/1e9:.1f}B"
        }
        insights['summary'] = (
            f"Revenue is {insights['revenue_trend']}. "
            f"Profits are {insights['profitability_trend']}. "
            f"Debt is {insights['debt_trend']}. "
            f"Cash flow is {insights['cashflow_trend']}."
        )
        return insights

def get_financial_statements(ticker: str) -> Tuple[Dict[str, List[float]], str]:
    try:
        c = yf.Ticker(ticker)
        fin, bal, cf = c.financials, c.balance_sheet, c.cashflow
        ni  = fin.loc['Net Income'].iloc[:3].tolist()
        td  = bal.loc['Total Debt'].iloc[:3].tolist()
        rv  = fin.loc['Total Revenue'].iloc[:3].tolist()
        ocf = cf.loc['Operating Cash Flow'].iloc[:3].tolist()
        summary = f"Revenue: {rv}\nNet Income: {ni}\nDebt: {td}\nOperating CF: {ocf}"
        return {'net_income':ni,'total_debt':td,'revenue':rv,'operating_cash_flow':ocf}, summary
    except:
        return {'net_income':[],'total_debt':[],'revenue':[],'operating_cash_flow':[]}, ''

def analyze_financial_data(ticker: str) -> Dict:
    data, summary = get_financial_statements(ticker)
    txt = f"Revenue:{data['revenue']},Debt:{data['total_debt']},NI:{data['net_income']},OCF:{data['operating_cash_flow']}"
    sent, _ = analyze_sentiment(txt)
    insights = FinancialAnalyzer.generate_insights(data)
    return {
        'financial_summary': data,
        'financial_summary_str': summary,
        'sentiment': sent,
        'fundamental_insights': insights
    }

# ---------------------------
# News Fetching
# ---------------------------
def google_query(q: str) -> str:
    if 'news' not in q.lower():
        q += ' stock news'
    return f"https://www.google.com/search?q={'+'.join(q.split())}&tbm=nws"

def google_scrape_news(name: str) -> Tuple[List[str], str]:
    try:
        r = requests.get(google_query(name), headers={'User-Agent':'Mozilla/5.0'}, timeout=5)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        heads = [t.get_text().strip() for t in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')][:4]
    except:
        heads = []
    s = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(heads))
    return heads, s

def get_news_from_newsapi(name: str) -> Tuple[List[str], str]:
    if not NEWSAPI_KEY:
        return [], ''
    params = {'q': f"{name} stock", 'apiKey': NEWSAPI_KEY, 'pageSize': 4}
    try:
        js = requests.get("https://newsapi.org/v2/everything", params=params, timeout=5).json()
        heads = [a['title'] for a in js.get('articles', [])][:4]
        s = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(heads))
        return heads, s
    except:
        return [], ''

def get_recent_stock_news(name: str, ticker: str) -> Tuple[List[str], str]:
    try:
        yf_news = yf.Ticker(ticker).news or []
        heads = [i['title'] for i in yf_news if i.get('title')][:4]
    except:
        heads = []
    if not heads:
        heads, s = get_news_from_newsapi(name)
        if not heads:
            heads, s = google_scrape_news(name)
    else:
        s = "Recent News:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(heads))
    return heads, s

# ---------------------------
# Extraction & Decision
# ---------------------------
def extract_company_and_ticker(q: str) -> Tuple[str, str]:
    clean = re.sub(r'[^a-z0-9\s]', '', q.lower())
    for w in clean.split():
        if w.upper() in SUPPORTED_TICKERS:
            return w.upper(), w.upper()
    for k, v in _normalized_company_map.items():
        if k and k in clean:
            return k, v
    return None, None

def generate_decision(trend, conf, news_sent, fin_ins) -> Dict:
    if trend == 'up' and news_sent == 'Positive':
        act, rs = 'Buy', 'Uptrend & positive news'
    elif trend == 'down' and news_sent == 'Negative':
        act, rs = 'Sell', 'Downtrend & negative news'
    else:
        act, rs = 'Hold', 'Mixed signals'
    if 'declining' in fin_ins['profitability_trend'] and act == 'Buy':
        act = 'Hold'
        rs += ', profits declining'
    elif 'growing' in fin_ins['revenue_trend'] and act == 'Hold':
        rs += ', revenue growing'
    return {'action': act, 'reasoning': f"{rs}. Fundamentals: {fin_ins['summary']}"}

def get_recommendations(amount: float, risk: str) -> Dict:
    recs = RISK_BASED_RECOMMENDATIONS.get(risk, [])
    recommendations = []
    allocation_plan = []
    total = 0.0

    for r in recs:
        tkr       = r['ticker']
        alloc_amt = amount * r['allocation']
        hist      = yf.Ticker(tkr).history(period='1mo')
        price     = hist['Close'].iloc[-1]
        sma10     = hist['Close'].rolling(10).mean().iloc[-1]
        trend     = 'up' if price > sma10 else 'down'
        shares    = round(alloc_amt / price, 2) if price else 0
        pct       = round(r['allocation'] * 100, 1)

        # build recommendation entry
        recommendations.append({
            'ticker': tkr,
            'allocation_pct': pct,
            'allocation_amt': round(alloc_amt, 2),
            'price': round(price, 2),
            'shares': shares,
            'trend': trend,
            'reason': r['reason']
        })

        # build allocation_plan entry
        allocation_plan.append({
            'ticker': tkr,
            'amount': round(alloc_amt, 2),
            'shares': shares,
            'percentage': pct
        })

        total += alloc_amt

    return {
        'total_amount': amount,
        'risk_level': risk,
        'invested': round(total, 2),
        'cash_left': round(amount - total, 2),
        'recommendations': recommendations,
        'allocation_plan': allocation_plan
    }

def perform_analysis(ticker: str, amount: float) -> Dict:
    try:
        st = yf.Ticker(ticker)
        h  = st.history(period='1mo')
        cp, op, hi, lo = h['Close'].iloc[-1], h['Open'].iloc[-1], h['High'].iloc[-1], h['Low'].iloc[-1]
        prev           = h['Close'].iloc[-2] if len(h)>1 else cp
        vol            = int(h['Volume'].iloc[-1])
        sma10          = h['Close'].rolling(10).mean().iloc[-1]

        trend      = 'up' if cp > sma10 else 'down'
        change_pct = (cp - prev) / prev
        volatility = (hi - lo) / op if op else 0

        confidence = min(
            0.95,
            max(
                0.05,
                0.5
                + (0.2 if trend == 'up' else -0.2)
                + min(0.2, max(-0.2, change_pct * 10))
                - min(0.1, volatility * 0.5)
            )
        )
        shares = int(amount / cp) if amount > 0 else 0

        name = next((k for k, v in COMPANY_NAME_TO_TICKER.items() if v == ticker), ticker)
        news_list, news_str = get_recent_stock_news(name.capitalize(), ticker)
        overall_sent, _    = analyze_sentiment(news_str)

        fin     = analyze_financial_data(ticker)
        fin_ins = fin['fundamental_insights']
        dec     = generate_decision(trend, confidence, overall_sent, fin_ins)

        return {
            'ticker': ticker,
            'current_price': round(cp, 2),
            'open_price': round(op, 2),
            'high_price': round(hi, 2),
            'low_price': round(lo, 2),
            'previous_close': round(prev, 2),
            'volume': vol,
            'sma_10': round(sma10, 2),
            'price_change_pct': round(change_pct * 100, 2),
            'volatility_pct': round(volatility * 100, 2),
            'trend': trend,
            'confidence': round(confidence, 2),
            'technical_confidence': round(confidence, 2),   # <-- added
            'shares_possible': shares,
            'pe_ratio': st.info.get('trailingPE'),
            'dividend_yield': st.info.get('dividendYield', 0),
            'news': news_str,
            'overall_news_sentiment': overall_sent,
            'financial_statements_sentiment': fin['sentiment'],
            'financial_statements_content': fin['financial_summary_str'],
            'fundamental_insights': fin_ins,
            'decision': dec['action'],
            'analysis': dec['reasoning']
        }

    except Exception as e:
        logging.error(f"Analysis error for {ticker}: {e}")
        return {'error': str(e)}

# ---------------------------
# API Endpoints
# ---------------------------
@app.route('/api/stocks', methods=['GET'])
def supported_stocks():
    return jsonify({
        'tickers': SUPPORTED_TICKERS,
        'sectors': SECTOR_MAP,
        'risk_levels': list(RISK_LEVELS.keys())
    })

@app.route('/api/analyze', methods=['GET'])
def analyze_endpoint():
    raw_t = request.args.get('ticker','').strip()
    qry   = request.args.get('query','').strip()
    amt   = float(request.args.get('amount', user_profile['available_amount']))

    if raw_t and raw_t.upper() not in SUPPORTED_TICKERS:
        qry, raw_t = raw_t, ''

    # Static trigger for recommendations
    if 'recommend' in qry.lower():
        risk = request.args.get('risk', user_profile['risk_preference']).lower()
        if risk not in RISK_LEVELS:
            return jsonify({'error': f"Invalid risk: choose {list(RISK_LEVELS.keys())}"}), 400
        return jsonify(get_recommendations(amt, risk))

    ticker = raw_t.upper() if raw_t.upper() in SUPPORTED_TICKERS else None
    if not ticker and qry:
        _, ticker = extract_company_and_ticker(qry)
    if not ticker:
        return jsonify({
            'error':'Could not identify stock',
            'suggestions':['?ticker=AAPL','?query="recommend" to get portfolio']
        }), 400

    result = perform_analysis(ticker, amt)
    return jsonify(result), (200 if 'error' not in result else 500)

@app.route('/api/recommend', methods=['GET'])
def recommend_endpoint():
    amt  = float(request.args.get('amount', user_profile['available_amount']))
    risk = request.args.get('risk', user_profile['risk_preference']).lower()
    if risk not in RISK_LEVELS:
        return jsonify({'error': f"Invalid risk: choose {list(RISK_LEVELS.keys())}"}), 400
    return jsonify(get_recommendations(amt, risk))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
