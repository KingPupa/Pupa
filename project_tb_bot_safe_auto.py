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
initial_balance = None  # Will be set at startup
trade_log = []

# ----------------------------
# TELEGRAM CLIENT
# ----------------------------
client = TelegramClient('project_tb_session', TELEGRAM_API_ID, TELEGRAM_API_HASH)

# ----------------------------
# BALANCE & SAFETY FUNCTIONS
# ----------------------------
def get_balance():
    """Fetches the current account balance from Quotex."""
    try:
        balance = quotex.get_balance()
        return float(balance)
    except Exception as e:
        print("[ERROR] Could not fetch balance:", e)
        return None

def can_trade():
    """Checks if safety limits have been reached."""
    global trade_log, initial_balance

    # 1. Check for max loss based on real-time balance
    current_balance = get_balance()
    if current_balance is not None and initial_balance is not None:
        loss = initial_balance - current_balance
        if loss >= MAX_LOSS:
            print(f"[SAFETY] MAX LOSS of ${MAX_LOSS} reached. Current session loss: ${loss:.2f}. Stopping trades.")
            return False

    # 2. Check for max trades per hour
    current_time = time.time()
    trade_log = [t for t in trade_log if current_time - t < 3600] # 1 hour window
    if len(trade_log) >= MAX_TRADES_PER_HOUR:
        print(f"[SAFETY] MAX TRADES PER HOUR ({MAX_TRADES_PER_HOUR}) reached. Pausing trades.")
        return False

    return True

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
# TRADE EXECUTION
# ----------------------------
def execute_trade(action, asset, duration, amount):
    """Executes a trade on Quotex after checking safety limits."""
    global trade_log

    if not can_trade():
        return

    try:
        side = 1 if action.upper() == "BUY" else 0
        response = quotex.buy(amount=amount, asset=asset, direction=side, duration=duration)
        print(f"[TRADE] {action} {asset} {duration} ${amount} | Response: {response}")
        trade_log.append(time.time())
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
    global initial_balance
    initial_balance = get_balance()
    if initial_balance is None:
        print("[ERROR] Could not fetch initial balance. Exiting.")
        return

    print(f"[INFO] Initial balance: ${initial_balance:.2f}. Starting bot...")

    await client.start(TELEGRAM_PHONE)
    print("[INFO] Project TB Safe Auto Bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())