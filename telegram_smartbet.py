import requests
import time
import telebot

# === CONFIGURATION ===
BOT_TOKEN = "8273880607:AAFweDIU9Zg_9fNh5xClotgFgFy0j0Y5WLI"  # your Telegram bot token
SMARTBET_KEY = "bcbwb-d634c140-f1b6-4a41-bd27-c6f18f77e2b7"    # your SmartBet.io Bot ID
SMARTBET_URL = "https://smartbet.io/postpick.php"               # main SmartBet endpoint
TELEGRAM_CHAT_ID = "7827479245"  # Optional if you want to receive confirmation messages

bot = telebot.TeleBot(BOT_TOKEN)

# === FUNCTION TO PLACE BET ===
def place_bet_on_smartbet(pick_text):
    try:
        payload = {"key": SMARTBET_KEY, "pick": pick_text}
        response = requests.get(SMARTBET_URL, params=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Bet sent successfully: {pick_text}")
            return True
        else:
            print(f"⚠️ SmartBet API error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending pick: {e}")
        return False


# === TELEGRAM MESSAGE HANDLER ===
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    pick_text = message.text.strip()
    success = place_bet_on_smartbet(pick_text)
    if TELEGRAM_CHAT_ID and success:
        bot.send_message(TELEGRAM_CHAT_ID, f"✅ Bet placed: {pick_text}")

# === RUN BOT ===
print("🤖 Telegram-SmartBet Bot running...")
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot error: {e}")
        time.sleep(10)
