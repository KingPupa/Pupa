# project_tb_bot_safe_auto.py
from telethon import TelegramClient, events
from pyquotex import Quotex
from dotenv import load_dotenv
import os
import asyncio
import time

# ----------------------------
# LOAD ENV VARIABLES
# ----------------------------
load_dotenv()
# Telegram Credentials
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
# Quotex Credentials
QUOTEX_EMAIL = os.getenv("QUOTEX_EMAIL")
QUOTEX_PASSWORD = os.getenv("QUOTEX_PASSWORD")

# ----------------------------
# CONNECT TO QUOTEX
# ----------------------------
quotex = Quotex(email=QUOTEX_EMAIL, password=QUOTEX_PASSWORD)

# ----------------------------
# BOT CONFIG
# ----------------------------
telegram_groups = ['@Binary_Bosss', '@Quotex_SuperBot', '@QuotexOTCHACK']
trade_amount = 1  # $1 per trade for testing

# ----------------------------
# SAFETY SETTINGS
# ----------------------------
MAX_TRADES_PER_HOUR = 20
MAX_LOSS = 50
current_loss = 0
trade_log = []

# ----------------------------
# TELEGRAM CLIENT
# ----------------------------
client = TelegramClient('project_tb_session', TELEGRAM_API_ID, TELEGRAM_API_HASH)

# ----------------------------
# SIGNAL PARSER
# ----------------------------
def parse_signal(message):
    """Parses messages like "BUY EURUSD 1m" """
    parts = message.strip().split()
    if len(parts) == 3:
        action, asset, duration = parts
        action = action.upper()
        return action, asset, duration
    return None, None, None

# ----------------------------
# SAFETY CHECK
# ----------------------------
def can_trade():
    """Checks if safety limits have been reached."""
    global current_loss, trade_log

    # 1. Check for max loss
    if current_loss >= MAX_LOSS:
        print(f"[SAFETY] MAX LOSS of ${MAX_LOSS} reached. Stopping trades.")
        return False

    # 2. Check for max trades per hour
    current_time = time.time()
    # Filter out trades older than an hour (3600 seconds)
    trade_log = [t for t in trade_log if current_time - t < 3600]
    if len(trade_log) >= MAX_TRADES_PER_HOUR:
        print(f"[SAFETY] MAX TRADES PER HOUR ({MAX_TRADES_PER_HOUR}) reached. Pausing trades.")
        return False

    return True

# ----------------------------
# TRADE EXECUTION
# ----------------------------
def execute_trade(action, asset, duration, amount):
    """Executes a trade on Quotex after checking safety limits."""
    global current_loss, trade_log

    if not can_trade():
        return

    try:
        side = 1 if action.upper() == "BUY" else 0
        response = quotex.buy(amount=amount, asset=asset, direction=side, duration=duration)
        print(f"[TRADE] {action} {asset} {duration} ${amount} | Response: {response}")

        # Log the trade for safety checks
        trade_log.append(time.time())
        # Assume a loss for conservative safety
        current_loss += amount
        print(f"[INFO] Current assumed loss: ${current_loss}")

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
    await client.start(TELEGRAM_PHONE)
    print("[INFO] Project TB Safe Auto Bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())