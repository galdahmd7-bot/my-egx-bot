import yfinance as yf
import requests
import pandas as pd

# --- ضع بياناتك هنا ---
TOKEN = "8644601202:AAHbkrF_vQG09vfocluUk9uBTAdtu4G5gMU"
CHAT_ID = "7221584941"

def send_telegram_msg(message):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def analyze_stock(symbol):
    ticker = yf.Ticker(f"{symbol}.CA")
    # جلب بيانات 60 يوم لضمان حساب المتوسطات ونقاط الدعم بدقة
    df = ticker.history(period="60d")
    if df.empty: return None
    
    last_price = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2]
    high = df['High'].iloc[-2]
    low = df['Low'].iloc[-2]
    
    # حساب الدعم والمقاومة (Pivot Points)
    pivot = (high + low + prev_close) / 3
    res1 = (2 * pivot) - low
    sup1 = (2 * pivot) - high
    
    # تحليل فني بسيط (متوسط 5 أيام)
    sma5 = df['Close'].rolling(window=5).mean().iloc[-1]
    
    # توصية المضارب
    if last_price > res1:
        signal = "🚀 اختراق للمقاومة (إيجابي جداً)"
    elif last_price > sma5:
        signal = "🟢 شراء مضاربي (فوق المتوسط)"
    elif last_price < sup1:
        signal = "⚠️ كسر دعم (حذر)"
    else:
        signal = "🟡 منطقة عرضية (انتظار)"
        
    return {
        "price": last_price,
        "signal": signal,
        "res": res1,
        "sup": sup1
    }

# قائمة أسهمك
my_stocks = ["MCRO", "ISPH", "POUL", "MFPC"]
report = "📊 *تقرير المحلل الآلي للبورصة المصرية* 📊\n\n"

for s in my_stocks:
    res = analyze_stock(s)
    if res:
        report += f"🔹 *سهم {s}*\n"
        report += f"السعر: {res['price']:.2f} ج.م\n"
        report += f"الإشارة: {res['signal']}\n"
        report += f"المقاومة: {res['res']:.2f} | الدعم: {res['sup']:.2f}\n"
        report += "------------------------\n"

send_telegram_msg(report)
