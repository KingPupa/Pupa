#!/data/data/com.termux/files/usr/bin/env python3
import time
import re
import threading
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from quotex_demo_bot import execute_demo_trade  # your existing demo trade function
# from quotex_live_bot import execute_live_trade  # uncomment for live trading

# --- TELEGRAM CONFIG ---
api_id = 26243332
api_hash = "2d0ec7dc609caca15b573fc2d5239424"
phone = "+254701022662"

channels = [
    "Binary_Bosss",
    "Quotex_SuperBot",
    "QuotexOTCHACK",
]  # add more channel usernames here

client = TelegramClient("project_tb_session", api_id, api_hash)

# --- TRADE SETTINGS ---
TRADE_AMOUNT = 1  # default amount
TRADE_WAIT_SEC = 55  # countdown from signal to execution
TRADE_BUFFER = {}  # store partial signals until direction appears

# --- FILES ---
BALANCE_FILE = "/data/data/com.termux/files/home/project_tb/balance.txt"
WINS_FILE = "/data/data/com.termux/files/home/project_tb/wins.txt"
LOSSES_FILE = "/data/data/com.termux/files/home/project_tb/losses.txt"
PROFIT_FILE = "/data/data/com.termux/files/home/project_tb/profit.txt"
TRADES_LOG = "/data/data/com.termux/files/home/project_tb/trades.log"

# --- HELPERS ---
def log_trade(symbol, direction, amount, result, net, bal):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"{now} | {symbol} | {direction} | {amount:.2f} | {result} | net:{net:.2f} | bal:{bal:.2f}\n"
    with open(TRADES_LOG, "a") as f:
        f.write(line)

def update_stats(result, net, balance):
    if result == "WIN":
        with open(WINS_FILE, "a") as f: f.write("1\n")
    else:
        with open(LOSSES_FILE, "a") as f: f.write("1\n")
    with open(PROFIT_FILE, "a") as f: f.write(f"{net}\n")
    with open(BALANCE_FILE, "w") as f: f.write(f"{balance:.2f}\n")

# --- TRADE EXECUTION ---
def execute_trade(symbol, direction, amount):
    # Demo trade
    bal, net, res = execute_demo_trade(symbol, direction, amount)
    update_stats(res, net, bal)
    log_trade(symbol, direction, amount, res, net, bal)
    print(f"Executed {direction} trade for {symbol} amount {amount}")

# --- TELEGRAM EVENT HANDLER ---
@client.on(events.NewMessage(chats=channels))
async def handler(event):
    text = event.raw_text
    # Extract symbol
    symbol_match = re.search(r'([A-Z]{3,5}[\/-][A-Z]{3,5})', text)
    if not symbol_match:
        return
    symbol = symbol_match.group(1)
    # Check for direction
    direction_match = re.search(r'(CALL|PUT|UP|DOWN|🔴|🟢)', text.upper())
    if direction_match:
        dir_raw = direction_match.group(1).upper()
        if dir_raw in ["CALL", "UP", "🟢"]:
            direction = "CALL"
        else:
            direction = "PUT"
        # Check if we have buffered signal
        if symbol in TRADE_BUFFER:
            # execute trade at scheduled time
            exec_time = TRADE_BUFFER[symbol]
            delay = max((exec_time - datetime.utcnow()).total_seconds(), 0)
            threading.Timer(delay, execute_trade, args=(symbol, direction, TRADE_AMOUNT)).start()
            del TRADE_BUFFER[symbol]
        else:
            # signal appeared late, execute after default wait
            threading.Timer(TRADE_WAIT_SEC, execute_trade, args=(symbol, direction, TRADE_AMOUNT)).start()
    else:
        # buffer the signal if direction missing
        TRADE_BUFFER[symbol] = datetime.utcnow() + timedelta(seconds=TRADE_WAIT_SEC)

# --- MAIN ---
async def main():
    print("🚀 Smart Trading Bot Running...")
    for ch in channels:
        print(f"📡 Listening to {ch}")
    await client.start(phone=phone)
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
#!/usr/bin/env python3
import sys
import time
from quotex_demo_bot import SESSION, BALANCE_FILE, TRADE_AMOUNT  # import only the existing variables

# --- Minimal Demo Trade Function ---
def execute_demo_trade(symbol="EURUSD", direction="call", amount=1.0):
    """
    Executes a demo trade by writing to balance.txt and trades log
    This mimics the logic inside quotex_demo_bot.py
    """
    import random
    from datetime import datetime

    # Load current balance
    try:
        with open(BALANCE_FILE, "r") as f:
            balance = float(f.read().strip())
    except:
        balance = 1000.0

    # Random win/loss outcome (50% chance)
    win = random.choice([True, False])
    payout = 0.85  # 85% payout for demo

    net = amount * payout if win else -amount
    balance += net

    # Save new balance
    with open(BALANCE_FILE, "w") as f:
        f.write(f"{balance:.2f}")

    # Log trade
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    result = "WIN" if win else "LOSS"
    print(f"=== Demo Trade Result ===")
    print(f"{timestamp} | {symbol} | {direction} | {amount} | 60s | {result} | net:{net:.2f} | bal:{balance:.2f}")

# --- MAIN ---
if __name__ == "__main__":
    print("🚀 Test Demo Bot Running...")
    execute_demo_trade(symbol="EURUSD", direction="call", amount=1.0)
