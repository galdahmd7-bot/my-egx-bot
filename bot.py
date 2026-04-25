import yfinance as yf
import requests

# بياناتك (تأكد من عمل Start للبوت في تليجرام)
TOKEN = "8044601202:AAHbkfF_v0GO9vfoCluUk9uBTADtu4G3gMU"
CHAT_ID = "7221534941"

def analyze_stock(symbol):
    try:
        ticker = yf.Ticker(f"{symbol}.CA")
        # جلب بيانات كافية للتحليل
        df = ticker.history(period="10d")
        if df.empty: return None
        
        last_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        change_pct = ((last_price - prev_price) / prev_price) * 100
        
        # تحليل الاتجاه (قوة السهم)
        trend = "🟢 صاعد قوي" if last_price > prev_price else "🔴 هابط/تصحيحي"
        
        # جلب آخر خبر متاح
        news = ticker.news
        news_title = news[0]['title'] if news else "لا توجد أخبار رسمية حالياً"

        msg = (f"🔹 *سهم {symbol}*\n"
               f"💰 السعر: {last_price:.2f} ج.م ({change_pct:+.2f}%)\n"
               f"📊 الحالة: {trend}\n"
               f"📰 خبر: {news_title[:60]}...\n"
               f"------------------------\n")
        return msg
    except:
        return None

def main():
    # قائمة أسهمك المختارة بعناية
    my_stocks = ["ISPH", "MCRO", "MFPC", "POUL"]
    
    final_report = "🚀 *تقرير مضارب البورصة المصرية* 🚀\n\n"
    
    for s in my_stocks:
        result = analyze_stock(s)
        if result:
            final_report += result
    
    # إرسال التقرير النهائي
    url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": final_report, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    main()
