import logging
import requests
from telegram.ext import Updater, MessageHandler, Filters

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = "8273880607:AAFweDIU9Zg_9fNh5xClotgFgFy0j0Y5WLI"
SMARTBET_KEY = "bcbwb-d634c140-f1b6-4a41-bd27-c6f18f77e2b7"  # from SmartBet dashboard

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_message(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"Received: {text}")

    # Forward message to SmartBet
    url = f"https://smartbet.io/pick.php?key={SMARTBET_KEY}&pick={text}"
    try:
        r = requests.get(url, timeout=10)
        update.message.reply_text(f"SmartBet Response: {r.text}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()