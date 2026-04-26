import requests
import time
import statistics

TOKEN = "PUT_TOKEN"
CHAT_ID = "PUT_CHAT_ID"

stocks = ["MCRO.CA","ISPH.CA","MFPC.CA","POUL.CA","ARAB.CA"]

# كلمات تحليل الخبر
positive_words = ["ربح", "نمو", "توسعات", "زيادة", "اتفاق"]
negative_words = ["خسارة", "تراجع", "ديون", "هبوط", "مشاكل"]

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg})

def get_prices(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=5m&range=1d"
    data = requests.get(url).json()
    prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
    volumes = data['chart']['result'][0]['indicators']['quote'][0]['volume']
    return prices, volumes

def ema(prices, n):
    k = 2/(n+1)
    e = prices[0]
    for p in prices:
        e = p*k + e*(1-k)
    return e

def rsi(prices):
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))
    avg_gain = sum(gains)/len(gains) if gains else 0.1
    avg_loss = sum(losses)/len(losses) if losses else 0.1
    rs = avg_gain / avg_loss
    return 100 - (100/(1+rs))

def get_news():
    try:
        url = "https://www.mubasher.info/api/1/news"
        res = requests.get(url).json()
        if "data" in res:
            return res["data"][:5]
    except:
        return []
    return []

def analyze_news(news_list):
    score = 0
    text = ""

    for n in news_list:
        title = n.get("title", "")
        text += f"\n📰 {title}"

        for w in positive_words:
            if w in title:
                score += 1
        for w in negative_words:
            if w in title:
                score -= 1

    if score > 1:
        sentiment = "إيجابي 🔥"
    elif score < -1:
        sentiment = "سلبي ❌"
    else:
        sentiment = "محايد ⚠️"

    return sentiment, text

def analyze(symbol, sentiment):
    prices, volumes = get_prices(symbol)
    if len(prices) < 20:
        return None

    last = prices[-1]
    ema9 = ema(prices, 9)
    ema21 = ema(prices, 21)
    r = rsi(prices)

    support = min(prices[-20:])
    resistance = max(prices[-20:])

    score = 0
    msg = f"\n📊 {symbol}\nالسعر: {last:.2f}"

    if ema9 > ema21:
        score += 1
        msg += "\n📈 صاعد"
    else:
        msg += "\n📉 هابط"

    if 50 < r < 65:
        score += 1
        msg += "\n⚡ زخم جيد"

    if abs(last - support) < 0.03:
        score += 1
        msg += "\n🟢 دعم"

    if sentiment == "إيجابي 🔥":
        score += 1

    # التوقع
    if score >= 3:
        forecast = "🚀 صعود متوقع"
    elif score <= 1:
        forecast = "📉 هبوط متوقع"
    else:
        forecast = "⏸️ عرضي"

    msg += f"\n🔮 التوقع: {forecast}"

    return msg

while True:
    news_list = get_news()
    sentiment, news_text = analyze_news(news_list)

    send(f"🧠 تحليل الأخبار: {sentiment}\n{news_text}")

    for s in stocks:
        try:
            result = analyze(s, sentiment)
            if result:
                send(result)
        except:
            pass

    time.sleep(300)
