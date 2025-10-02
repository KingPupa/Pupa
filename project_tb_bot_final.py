# project_tb_bot_final.py
from telethon import TelegramClient, events
from pyquotex import Quotex
from dotenv import load_dotenv
import os
import asyncio
import time
import json

# ----------------------------
# LOAD ENV VARIABLES
# ----------------------------
load_dotenv()

# ----------------------------
# FETCH TELEGRAM CREDENTIALS
# ----------------------------
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")

# ----------------------------
# CONNECT TO QUOTEX
# ----------------------------
EMAIL = os.getenv("QUOTEX_EMAIL")
PASSWORD = os.getenv("QUOTEX_PASSWORD")
quotex = Quotex(email=EMAIL, password=PASSWORD)

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
trade_log = []

# ----------------------------
# TELEGRAM CLIENT
# ----------------------------
client = TelegramClient('project_tb_session', api_id, api_hash)

# ----------------------------
# SIGNAL PARSER
# ----------------------------
def parse_signal(message):
    parts = message.strip().split()
    if len(parts) == 3:
        action, asset, duration = parts
        action = action.upper()
        return action, asset, duration
    return None, None, None

# ----------------------------
# BALANCE & P/L TRACKING
# ----------------------------
def get_balance():
    try:
        balance = quotex.get_balance()
        return float(balance)
    except Exception as e:
        print("[ERROR] Could not fetch balance:", e)
        return None

starting_balance = get_balance()

# ----------------------------
# TRADE EXECUTION WITH SAFETY AND P/L
# ----------------------------
def can_trade():
    """Checks if safety limits (max trades and max loss) have been reached."""
    global trade_log, starting_balance

    # 1. Check for max loss
    current_balance = get_balance()
    if current_balance is not None and starting_balance is not None:
        loss = starting_balance - current_balance
        if loss >= MAX_LOSS:
            print(f"[SAFETY] MAX LOSS of ${MAX_LOSS} reached. Current session loss: ${loss:.2f}. Stopping trades.")
            return False

    # 2. Check for max trades per hour
    current_time = time.time()
    trade_log = [t for t in trade_log if current_time - t < 3600]  # 1 hour window
    if len(trade_log) >= MAX_TRADES_PER_HOUR:
        print(f"[SAFETY] MAX TRADES PER HOUR ({MAX_TRADES_PER_HOUR}) reached. Pausing trades.")
        return False

    return True

def execute_trade(action, asset, duration, amount, retries=3):
    """Executes a trade after checking safety limits, with retries."""
    global trade_log

    if not can_trade():
        return

    attempt = 0
    while attempt < retries:
        try:
            side = 1 if action.upper() == "BUY" else 0
            response = quotex.buy(amount=amount, asset=asset, direction=side, duration=duration)
            print(f"[TRADE] {action} {asset} {duration} ${amount} | Response: {response}")
            trade_log.append(time.time())

            # Log current P/L after a successful trade
            current_balance = get_balance()
            if current_balance is not None and starting_balance is not None:
                total_pl = current_balance - starting_balance
                print(f"[INFO] Total session P/L: ${total_pl:.2f}")

            return # Exit the loop on success
        except Exception as e:
            attempt += 1
            print(f"[WARN] Trade attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(1) # Wait a second before retrying

    print(f"[ERROR] All {retries} trade attempts failed for {action} {asset}. Skipping trade.")

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
# PERIODIC BALANCE MONITOR
# ----------------------------
async def balance_monitor(interval=300):
    """Periodically fetches and prints the account balance and session P/L."""
    while True:
        balance = get_balance()
        if balance is not None and starting_balance is not None:
            total_pl = balance - starting_balance
            print(f"[BALANCE] Current balance: ${balance:.2f} | Session P/L: ${total_pl:.2f}")
        await asyncio.sleep(interval)

# ----------------------------
# RUN BOT
# ----------------------------
async def main():
    if starting_balance is None:
        print("[ERROR] Could not fetch initial balance. Exiting.")
        return

    print(f"[INFO] Initial balance: ${starting_balance:.2f}. Starting bot...")

    await client.start(phone)
    print("[INFO] Project TB Bot is running with safety and P/L tracking...")

    # Start background balance monitor
    asyncio.create_task(balance_monitor())

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())