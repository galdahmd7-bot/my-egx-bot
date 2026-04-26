import yfinance as yf
import requests
import logging

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# البيانات الصحيحة - محدّثة
TOKEN = "8644601202:AAHbkrF_vQG09vfocluUk9uBTAdtu4G5gMU"
CHAT_ID = "7221584941"

def analyze():
    stocks = ["ISPH", "MCRO", "MFPC", "POUL"]
    report = "🚀 *تقرير البورصة المصرية* 🚀\n\n"
    success_count = 0
    
    for s in stocks:
        try:
            # جلب البيانات
            data = yf.Ticker(f"{s}.CA").history(period="5d")
            
            # التحقق من وجود بيانات كافية
            if data.empty or len(data) < 2:
                logger.warning(f"بيانات غير كافية للسهم {s}")
                continue
            
            price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2]
            change = ((price - prev_price) / prev_price) * 100
            trend = "🟢 صاعد" if price > prev_price else "🔴 هابط"
            
            report += f"🔹 *{s}*: {price:.2f} ج.م ({change:+.2f}%)\n"
            report += f"الحالة: {trend}\n"
            report += "------------------------\n"
            success_count += 1
            
        except Exception as e:
            logger.error(f"خطأ في جلب بيانات {s}: {str(e)}")
            continue
    
    # التحقق من وجود بيانات للإرسال
    if success_count == 0:
        report += "⚠️ لم يتم الحصول على بيانات"
        logger.warning("لم يتم جلب أي بيانات بنجاح")
    
    # الرابط الصحيح لـ Telegram API
    final_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # إرسال الرسالة مع معالجة الأخطاء
    try:
        response = requests.post(
            final_url,
            json={
                "chat_id": CHAT_ID,
                "text": report,
                "parse_mode": "Markdown"
            },
            timeout=10
        )
        
        # التحقق من نجاح الإرسال
        if response.status_code == 200:
            logger.info("✅ تم إرسال الرسالة بنجاح")
            return True
        else:
            logger.error(f"❌ فشل الإرسال - الكود: {response.status_code}")
            logger.error(f"الرد: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error("❌ انتهاء المهلة الزمنية - Telegram API لم يستجب")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ خطأ في الاتصال: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {str(e)}")
        return False

if __name__ == "__main__":
    analyze()
