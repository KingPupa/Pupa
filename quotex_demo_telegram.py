# Paste the script, Ctrl+O, Enter, Ctrl+X#!/usr/bin/env python3
"""
Quotex DEMO bot + Telegram signals listener
- API_ID, API_HASH from https://my.telegram.org
- Executes demo trades automatically on incoming signals
- Logs signals to signals.log
"""

import os
import random
from datetime import datetime
import re
import asyncio
from telethon import TelegramClient, events

# ===== CONFIG =====
API_ID = 26243332
API_HASH = "2d0ec7dc609caca15b573fc2d5239424"
SESSION_NAME = "quotex_session"
GROUP_ID = -1001234567890  # Replace with your Telegram group ID

STARTING_BALANCE = 1000.0
BALANCE_FILE = os.path.expanduser("~/project_tb/balance.txt")
WINS_FILE = os.path.expanduser("~/project_tb/wins.txt")
LOSSES_FILE = os.path.expanduser("~/project_tb/losses.txt")
PROFIT_FILE = os.path.expanduser("~/project_tb/profit.txt")
TRADE_LOG = os.path.expanduser("~/project_tb/trades.log")
SIGNAL_LOG = os.path.expanduser("~/project_tb/signals.log")

PAYOUT = 0.85
WIN_RATE = 0.5
RANDOM_SEED = None

# ===== File Helpers =====
def safe_write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(str(text))
    os.replace(tmp, path)

def safe_read(path, default="0"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return str(default)

def init_files():
    if safe_read(BALANCE_FILE) == "0":
        safe_write(BALANCE_FILE, f"{STARTING_BALANCE:.2f}")
    if not os.path.exists(WINS_FILE):
        safe_write(WINS_FILE, "0")
    if not os.path.exists(LOSSES_FILE):
        safe_write(LOSSES_FILE, "0")
    if not os.path.exists(PROFIT_FILE):
        safe_write(PROFIT_FILE, "0.00")
    if not os.path.exists(TRADE_LOG):
        with open(TRADE_LOG, "w") as f:
            f.write("# trades log\n")
    if not os.path.exists(SIGNAL_LOG):
        with open(SIGNAL_LOG, "w") as f:
            f.write("# signals log\n")

def read_stats():
    wins = int(safe_read(WINS_FILE, "0") or "0")
    losses = int(safe_read(LOSSES_FILE, "0") or "0")
    profit = float(safe_read(PROFIT_FILE, "0") or "0")
    balance_raw = safe_read(BALANCE_FILE, f"{STARTING_BALANCE:.2f}")
    try:
        balance = float(balance_raw.split()[0])
    except:
        balance = float(balance_raw or STARTING_BALANCE)
    return wins, losses, profit, balance

def write_stats(wins, losses, profit, balance):
    safe_write(WINS_FILE, str(wins))
    safe_write(LOSSES_FILE, str(losses))
    safe_write(PROFIT_FILE, f"{profit:.2f}")
    safe_write(BALANCE_FILE, f"{balance:.2f}")

def log_trade(data: str):
    with open(TRADE_LOG, "a") as f:
        f.write(data + "\n")

def log_signal(data: str):
    with open(SIGNAL_LOG, "a") as f:
        f.write(data + "\n")

# ===== Demo Trade Function =====
def simulate_trade(amount=1.0, direction="call", asset="EURUSD"):
    wins, losses, profit, balance = read_stats()
    if amount <= 0 or amount > balance:
        print(f"[!] Invalid trade amount: {amount}, balance: {balance:.2f}")
        return

    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED + int(datetime.utcnow().timestamp()))

    win = random.random() < WIN_RATE

    if win:
        net = amount * PAYOUT
        balance += net
        profit += net
        wins += 1
        result = "WIN"
    else:
        net = -amount
        balance += net
        profit += net
        losses += 1
        result = "LOSS"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trade_id = f"DEMO-{int(datetime.utcnow().timestamp()*1000)}"
    log_line = f"{timestamp} | {trade_id} | {asset} | {direction} | {amount:.2f} | net:{net:.2f} | bal:{balance:.2f} | {result}"
    log_trade(log_line)
    write_stats(wins, losses, profit, balance)
    print(f"[Demo Trade] {log_line}")
    return {
        "trade_id": trade_id,
        "asset": asset,
        "direction": direction,
        "amount": amount,
        "result": result,
        "balance": balance
    }

# ===== Parse Telegram Signals =====
def parse_signal(msg: str):
    msg = msg.upper().replace("BUY","CALL").replace("SELL","PUT")
    # Look for pattern: ASSET DIR AMOUNT (e.g. EURUSD CALL 1$ or GBPJPY PUT 2)
    match = re.search(r"([A-Z]{6})\s+(CALL|PUT)\s+(\$?\d+)", msg)
    if match:
        asset, direction, amount = match.groups()
        amount = float(amount.replace("$",""))
        return asset, direction.lower(), amount
    return None

# ===== Telegram Client Setup =====
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats=GROUP_ID))
async def signal_handler(event):
    raw_msg = event.message.message.strip()
    parsed = parse_signal(raw_msg)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if parsed:
        asset, direction, amount = parsed
        log_signal(f"{timestamp} | {raw_msg} | Parsed: {asset} {direction} {amount}")
        print(f"[Signal Received] {raw_msg} → {asset} {direction} {amount}")
        simulate_trade(amount=amount, direction=direction, asset=asset)
    else:
        log_signal(f"{timestamp} | {raw_msg} | Unrecognized format")
        print(f"[Signal Ignored] {raw_msg}")

# ===== Run Bot =====
if __name__ == "__main__":
    init_files()
    print("Quotex DEMO bot + Telegram listener running...")
    print(f"Stats files: {BALANCE_FILE}, {WINS_FILE}, {LOSSES_FILE}, {PROFIT_FILE}")
    print(f"Signals log: {SIGNAL_LOG}")
    print("Listening for Telegram signals... Press Ctrl+C to exit.")
    client.start()
    client.run_until_disconnected()
