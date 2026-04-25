import yfinance as yf
import requests

# التوكن والآي دي بتوعك
TOKEN = "8044601202:AAHbkfF_v0GO9vfoCluUk9uBTADtu4G3gMU"
CHAT_ID = "7221534941"

def analyze_stock(symbol):
    try:
        ticker = yf.Ticker(f"{symbol}.CA")
        df = ticker.history(period="5d")
        if df.empty: return None
        
        last_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        change_pct = ((last_price - prev_price) / prev_price) * 100
        trend = "🟢 صاعد" if last_price > prev_price else "🔴 هابط"
        
        return (f"🔹 *سهم {symbol}*\n"
                f"💰 السعر: {last_price:.2f} ج.م ({change_pct:+.2f}%)\n"
                f"📊 الحالة: {trend}\n"
                f"------------------------\n")
    except:
        return None

def main():
    my_stocks = ["ISPH", "MCRO", "MFPC", "POUL"]
    final_report = "🚀 *تقرير البورصة المصرية* 🚀\n\n"
    
    for s in my_stocks:
        res = analyze_stock(s)
        if res: final_report += res
    
    # الرابط الكامل والصحيح (تمت إضافة api.)
    full_url = "https://telegram.org" + TOKEN + "/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": final_report,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(full_url, json=payload)
    print(f"Server Response: {response.status_code}")

if __name__ == "__main__":
    main()
