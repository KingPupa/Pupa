# project_tb_bot.py
from telethon import TelegramClient, events
from pyquotex import Quotex
from dotenv import load_dotenv
import os
import asyncio

# ----------------------------
# LOAD ENV VARIABLES
# ----------------------------
load_dotenv()
EMAIL = os.getenv("QUOTEX_EMAIL")
PASSWORD = os.getenv("QUOTEX_PASSWORD")

# ----------------------------
# CONNECT TO QUOTEX
# ----------------------------
quotex = Quotex(email=EMAIL, password=PASSWORD)

# ----------------------------
# TELEGRAM CONFIG
# ----------------------------
api_id = YOUR_API_ID          # Replace with your Telegram API ID
api_hash = 'YOUR_API_HASH'    # Replace with your Telegram API Hash
phone = 'YOUR_PHONE_NUMBER'   # Replace with your phone number

# Telegram groups to monitor
telegram_groups = ['@Binary_Bosss', '@Quotex_SuperBot', '@QuotexOTCHACK']

# Test trade amount (start small!)
trade_amount = 1  # $1 per trade for testing

# ----------------------------
# TELEGRAM CLIENT
# ----------------------------
client = TelegramClient('project_tb_session', api_id, api_hash)

# ----------------------------
# SIGNAL PARSER
# ----------------------------
def parse_signal(message):
    """
    Parses messages like "BUY EURUSD 1m"
    Returns: action, asset, duration
    """
    parts = message.strip().split()
    if len(parts) == 3:
        action, asset, duration = parts
        action = action.upper()
        return action, asset, duration
    return None, None, None

# ----------------------------
# TRADE EXECUTION
# ----------------------------
def execute_trade(action, asset, duration, amount):
    try:
        side = 1 if action.upper() == "BUY" else 0
        response = quotex.buy(amount=amount, asset=asset, direction=side, duration=duration)
        print(f"[TRADE] {action} {asset} {duration} ${amount} | Response: {response}")
    except Exception as e:
        print("[ERROR] Trade failed:", e)

# ----------------------------
# TELEGRAM EVENT HANDLER
# ----------------------------
@client.on(events.NewMessage(chats=telegram_groups))
async def handle_new_signal(event):
    message = event.message.message
    print(f"[INFO] New Signal Received: {message}")

    action, asset, duration = parse_signal(message)
    if action:
        execute_trade(action, asset, duration, trade_amount)
    else:
        print("[WARN] Could not parse signal:", message)

# ----------------------------
# RUN BOT
# ----------------------------
async def main():
    await client.start(phone)
    print("[INFO] Project TB Bot is running on dev_testing branch...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())