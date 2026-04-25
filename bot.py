import yfinance as yf
import requests

# البيانات الصحيحة
TOKEN = "8044601202:AAHbkfF_v0GO9vfoCluUk9uBTADtu4G3gMU"
CHAT_ID = "7221534941"

def analyze():
    stocks = ["ISPH", "MCRO", "MFPC", "POUL"]
    report = "🚀 *تقرير البورصة المصرية* 🚀\n\n"
    
    for s in stocks:
        try:
            # جلب البيانات
            data = yf.Ticker(f"{s}.CA").history(period="5d")
            if data.empty: continue
            
            price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2]
            change = ((price - prev_price) / prev_price) * 100
            trend = "🟢 صاعد" if price > prev_price else "🔴 هابط"
            
            report += f"🔹 *{s}*: {price:.2f} ج.م ({change:+.2f}%)\n"
            report += f"الحالة: {trend}\n"
            report += "------------------------\n"
        except:
            continue
    
    # الرابط النهائي مكتوب يدوياً بالكامل لتجنب أخطاء التابلت
    final_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # إرسال الرسالة
    requests.post(final_url, json={
        "chat_id": CHAT_ID,
        "text": report,
        "parse_mode": "Markdown"
    })

if __name__ == "__main__":
    analyze()