import requests
import time
import asyncio
from telegram import Bot
from flask import Flask
from threading import Thread

# ==============================
# Налаштування
# ==============================
WALLET = "476e1NGic1oadzFLHAUCH4fYRHh3CBSFAXyXJpCkP4xt6JCV5M9gFFPTbWmzh2hpvnbYAahaASYkUfp9pDujeDKqTP5pzYW"  # <- твоя Monero адреса
BOT_TOKEN = "8334810664:AAG_TL5KbUvtc2yTtvMkyjniqCNDO-F0u8U"
CHAT_ID = "6052985971"  # <- твій чат ID

bot = Bot(token=BOT_TOKEN)

# ==============================
# Keep-alive сервер для хостингу
# ==============================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==============================
# Основна функція бота
# ==============================
async def check_wallet():
    while True:
        try:
            url = f"https://supportxmr.com/api/miner/{WALLET}/stats"
            r = requests.get(url, timeout=10)
            data = r.json()

            hashrate = data.get('hashrate', 0) / 1000  # KH/s
            unpaid = data.get('amtDue', 0) / 1e12      # XMR
            usd = unpaid * 170                          # приблизно $170 за XMR

            message = f"💰 LUXE WALLS\n🔥 Хешрейт: {hashrate:.1f} KH/s\n💎 Накопичено: {unpaid:.6f} XMR\n💵 ≈${usd:.2f}"
            bot.send_message(chat_id=CHAT_ID, text=message)
            print(f"[INFO] Повідомлення надіслано: {unpaid} XMR")
        except Exception as e:
            print(f"[ERROR] {e}")

        await asyncio.sleep(3600)  # чекати 1 годину

# ==============================
# Запуск бота
# ==============================
if __name__ == "__main__":
    print("🚀 LUXE Miner Bot запущено!")
    keep_alive()
    try:
        asyncio.run(check_wallet())
    except KeyboardInterrupt:
        print("Бот зупинено вручну")
