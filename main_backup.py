import asyncio
import threading
from datetime import datetime, timedelta

# --- Configuration ---
TRADE_WAIT_SEC = 10  # seconds to wait for missing direction
TRADE_AMOUNT = 1.0

# --- Bot status ---
bot_status = {"demo": False, "telegram": False}

# --- Mini stats loop ---
def mini_stats_loop(status):
    import time
    while True:
        print(f"Balance: 1000 | Profit: 0 | Wins: 0 | Losses: 0 | Bot Demo: {'✅' if status['demo'] else '❌'} | Telegram: {'✅' if status['telegram'] else '❌'}")
        time.sleep(5)  # refresh rate

# --- Telegram listener stub ---
async def start_telegram(status):
    status['telegram'] = True
    while True:
        # This is where you would process signals
        await asyncio.sleep(5)

# --- Main ---
async def main():
    print("🚀 Smart Trading Bot Running...")
    
    # Start Telegram listener
    asyncio.create_task(start_telegram(bot_status))
    
    # Start mini stats in separate thread
    threading.Thread(target=mini_stats_loop, args=(bot_status,), daemon=True).start()
    
    # Keep main alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
import asyncio
import threading
from datetime import datetime, timedelta
import random

# ---------- CONFIG ----------
TRADE_AMOUNT = 1
TRADE_WAIT_SEC = 50  # default wait if signal missing direction
MINI_REFRESH = 5     # mini stats refresh in seconds

# Demo bot variables
BALANCE = 1000.0
PROFIT = 0.0
WINS = 0
LOSSES = 0
BOT_DEMO_ACTIVE = False

# Telegram listener mock channels
channels = ["Binary_Bosss", "Quotex_SuperBot", "QuotexOTCHACK"]

# Trade buffer for signals missing direction
TRADE_BUFFER = {}

# ---------- FUNCTIONS ----------
def execute_demo_trade(symbol, direction, amount):
    """Simulate a demo trade"""
    global BALANCE, PROFIT, WINS, LOSSES
    win_rate = 0.6
    payout = 0.85
    result = "WIN" if random.random() < win_rate else "LOSS"
    net = amount * payout if result == "WIN" else -amount
    BALANCE += net
    PROFIT += net
    if result == "WIN":
        WINS += 1
    else:
        LOSSES += 1
    print(f"{datetime.utcnow().strftime('%H:%M:%S')} | {symbol} {direction} {amount} | {result} | Net: {net:.2f} | Bal: {BALANCE:.2f}")

async def start_telegram(bot_status):
    """Mock Telegram listener"""
    bot_status['telegram'] = True
    while True:
        await asyncio.sleep(1)
        # Here you would add code to read Telegram signals
        # For example: parse and call schedule_trade(symbol, direction, exec_time)
        # This mock prints that listener is alive
        # print(f"📡 Listening to Telegram...")

def mini_stats_loop(bot_status):
    """Update mini stats every MINI_REFRESH seconds"""
    while True:
        demo_status = "✅" if bot_status.get("demo") else "❌"
        telegram_status = "✅" if bot_status.get("telegram") else "❌"
        print(f"Balance: {BALANCE:.2f} | Profit: {PROFIT:.2f} | Wins: {WINS} | Losses: {LOSSES} | Bot Demo: {demo_status} | Telegram: {telegram_status}")
        threading.Event().wait(MINI_REFRESH)

# ---------- MAIN ----------
async def main():
    bot_status = {"demo": False, "telegram": False}

    print("🚀 Smart Trading Bot Running...")
    for ch in channels:
        print(f"📡 Listening to {ch}")

    # Start Telegram listener
    asyncio.create_task(start_telegram(bot_status))
    # Start mini stats loop in separate thread
    threading.Thread(target=mini_stats_loop, args=(bot_status,), daemon=True).start()

    # Simulate demo bot activation
    bot_status["demo"] = True
    global BOT_DEMO_ACTIVE
    BOT_DEMO_ACTIVE = True

    # Keep main alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
