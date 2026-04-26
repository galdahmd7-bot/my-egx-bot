import requests
import time

API_KEY = "d7n6vhhr01qppri3q6g0d7n6vhhr01qppri3q6gg"
TOKEN = "8644601202:AAHbkrF_vQG09vfocluUk9uBTAdtu4G5gMU"
CHAT_ID = "7221584941"

stocks = ["MCRO", "ISPH", "MFPC", "POUL", "ARAB"]

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg})

def get_price(symbol):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        data = requests.get(url).json()
        return data.get("c"), data.get("pc")
    except:
        return None, None

def get_news(symbol):
    try:
        url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2024-01-01&to=2026-12-31&token={API_KEY}"
        data = requests.get(url).json()
        if len(data) > 0:
            return data[0]['headline']
    except:
        return "لا يوجد خبر"
    return "لا يوجد خبر"

def analyze(symbol):
    price, prev = get_price(symbol)

    if not price or not prev:
        return

    change = ((price - prev) / prev) * 100

    if change > 1:
        trend = "📈 صاعد قوي"
        rec = "🔥 شراء"
    elif change < -1:
        trend = "📉 هابط"
        rec = "❌ بيع"
    else:
        trend = "⏸️ عرضي"
        rec = "⚠️ انتظار"

    news = get_news(symbol)

    msg = f"""
📊 {symbol}
السعر: {price}

التغير: {change:.2f}%
{trend}

📰 {news}

✅ التوصية: {rec}
"""

    send(msg)

while True:
    for s in stocks:
        analyze(s)
    time.sleep(300)
