# project_tb_bot.py
from telethon import TelegramClient, events
from pyquotex import Quotex
from dotenv import load_dotenv
import os
import asyncio
import time
import datetime

# ----------------------------
# LOAD ENV VARIABLES
# ----------------------------
load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")

EMAIL = os.getenv("QUOTEX_EMAIL")
PASSWORD = os.getenv("QUOTEX_PASSWORD")

# ----------------------------
# CONNECT TO QUOTEX
# ----------------------------
quotex = Quotex(email=EMAIL, password=PASSWORD)

# ----------------------------
# TELEGRAM CONFIG
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
starting_balance = None

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
        return action.upper(), asset, duration
    return None, None, None

# ----------------------------
# BALANCE / P&L TRACKING
# ----------------------------
def get_balance():
    try:
        balance = quotex.get_balance()
        return float(balance)
    except Exception as e:
        print("[ERROR] Could not fetch balance:", e)
        return None

# ----------------------------
# TRADE EXECUTION
# ----------------------------
def can_trade():
    current_time = time.time()
    global trade_log
    trade_log = [t for t in trade_log if current_time - t < 3600]  # last 1 hour
    return len(trade_log) < MAX_TRADES_PER_HOUR

def execute_trade(action, asset, duration, amount, retries=3):
    global current_loss, starting_balance
    if current_loss >= MAX_LOSS:
        print("[ALERT] Stop-loss triggered. No more trades until reset.")
        return
    if not can_trade():
        print("[WARN] Max trades per hour reached. Skipping trade.")
        return

    attempt = 0
    while attempt < retries:
        try:
            pre_balance = get_balance()
            side = 1 if action == "BUY" else 0
            response = quotex.buy(amount=amount, asset=asset, direction=side, duration=duration)
            trade_log.append(time.time())

            post_balance = get_balance()
            if pre_balance and post_balance:
                trade_pl = post_balance - pre_balance
                current_loss += max(0, -trade_pl)
                total_pl = post_balance - starting_balance
                print(f"[INFO] Trade P/L: ${trade_pl:.2f} | Total P/L: ${total_pl:.2f}")

            print(f"[TRADE] {action} {asset} {duration} ${amount} | Response: {response}")
            return
        except Exception as e:
            attempt += 1
            print(f"[WARN] Trade attempt {attempt} failed: {e}")
    print("[ERROR] All retries failed. Skipping trade.")

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
            print(f"[BALANCE] Current: ${balance:.2f} | Session P/L: ${total_pl:.2f}")
        await asyncio.sleep(interval)

# ----------------------------
# DAILY RESET TASK
# ----------------------------
async def daily_reset():
    global current_loss, starting_balance
    while True:
        now = datetime.datetime.now()
        next_reset = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_time = (next_reset - now).total_seconds()
        await asyncio.sleep(wait_time)
        current_loss = 0
        starting_balance = get_balance()
        print("[RESET] Daily stop-loss and P/L tracking reset.")

# ----------------------------
# RUN BOT
# ----------------------------
async def main():
    global starting_balance
    try:
        balance = quotex.get_balance()
        starting_balance = float(balance)

        # Mask email for safety
        masked_email = EMAIL[:3] + "****" + EMAIL[EMAIL.find("@"):]
        print(f"[SUCCESS] Logged into Quotex as {masked_email} | Balance: ${balance}")
    except Exception as e:
        print("[ERROR] Could not log in to Quotex:", e)
        return

    # Mask phone number for safety
    masked_phone = phone[:5] + "****" + phone[-2:]
    print(f"[INFO] Telegram session starting for {masked_phone}")

    await client.start(phone)
    print("[INFO] Project TB Bot is running...")

    asyncio.create_task(balance_monitor())
    asyncio.create_task(daily_reset())
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())