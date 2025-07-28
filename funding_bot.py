import requests
import time

TELEGRAM_BOT_TOKEN = "7786655117:AAHMkwbFagfCtsLD9kWJjOHm2um6EnEvYkA"
TELEGRAM_CHAT_ID = "-1002557151345"

# İzlemek istediğin coinler (Binance sembolleri)
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"]

# Funding rate sınırları (ondalık, 1.5% = 0.015)
UPPER_LIMIT = 0.015
LOWER_LIMIT = -0.015

# Önceki uyarıları tutar, tekrarı engeller
previous_alerts = {}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("Telegram mesaj gönderme hatası:", response.text)
    except Exception as e:
        print("Telegram API bağlantı hatası:", e)

def get_funding_rate(symbol):
    url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data['lastFundingRate'])

def check_funding_rates():
    for symbol in symbols:
        try:
            rate = get_funding_rate(symbol)
            rate_percent = rate * 100
            alert_key = f"{symbol}_alert"

            print(f"[{symbol}] Funding Rate: {rate_percent:.4f}%")

            if rate >= UPPER_LIMIT and previous_alerts.get(alert_key) != "high":
                msg = f"🚨 *{symbol} Funding Rate YÜKSEK!* \nOran: *{rate_percent:.4f}%*"
                send_telegram_message(msg)
                previous_alerts[alert_key] = "high"

            elif rate <= LOWER_LIMIT and previous_alerts.get(alert_key) != "low":
                msg = f"⚠️ *{symbol} Funding Rate DÜŞÜK!* \nOran: *{rate_percent:.4f}%*"
                send_telegram_message(msg)
                previous_alerts[alert_key] = "low"

            elif LOWER_LIMIT < rate < UPPER_LIMIT:
                previous_alerts[alert_key] = "normal"

        except Exception as e:
            print(f"{symbol} için hata:", e)

if __name__ == "__main__":
    print("Funding Rate Botu başladı...")
    while True:
        check_funding_rates()
        print("10 dakika bekleniyor...")
        time.sleep(600)  # 10 dakika
