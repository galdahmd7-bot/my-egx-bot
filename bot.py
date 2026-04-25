import yfinance as yf
import requests

TOKEN = "8044601202:AAHbkfF_v0GO9vfoCluUk9uBTADtu4G3gMU"
CHAT_ID = "7221534941"

def send_telegram_msg(message):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload)
        print(f"Status: {r.status_code}")
    except:
        print("Error")

def analyze(symbol):
    t = yf.Ticker(f"{symbol}.CA")
    df = t.history(period="10d")
    if df.empty: return None
    lp = df['Close'].iloc[-1]
    p = (df['High'].iloc[-2] + df['Low'].iloc[-2] + df['Close'].iloc[-2]) / 3
    r1 = (2 * p) - df['Low'].iloc[-2]
    s1 = (2 * p) - df['High'].iloc[-2]
    sig = "🟢 شراء" if lp > p else "🔴 مراقبة"
    return f"🔹 *{symbol}*: {lp:.2f}\nالإشارة: {sig}\nمقاومة: {r1:.2f} | دعم: {s1:.2f}\n"

stocks = ["MCRO", "ISPH", "POUL", "MFPC"]
report = "📊 *تقرير البورصة المصرية* 📊\n\n"
for s in stocks:
    res = analyze(s)
    if res: report += res + "----------\n"

send_telegram_msg(report)
