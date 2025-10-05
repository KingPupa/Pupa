#!/usr/bin/env python3
import asyncio
import threading
from datetime import datetime, timedelta
from quotex_demo_bot import execute_demo_trade  # your existing demo trade function

# ---------------- CONFIG ----------------
TRADE_WAIT_SEC = 60          # default wait for signals before execution
TRADE_AMOUNT = 1             # default trade amount
MINI_STATS_REFRESH = 5       # mini stats refresh in seconds

# Signal buffer
TRADE_BUFFER = {}

# Bot status
bot_status = {
    "demo": False,
    "telegram": False
}

# ---------------- MINI STATS ----------------
def mini_stats_loop(status):
    import os
    while True:
        os.system('clear')
        try:
            with open("balance.txt") as f:
                balance = float(f.read().strip())
            with open("profit.txt") as f:
                profit = float(f.read().strip())
            with open("wins.txt") as f:
                wins = int(f.read().strip())
            with open("losses.txt") as f:
                losses = int(f.read().strip())
        except:
            balance = 1000
            profit = 0
            wins = 0
            losses = 0

        demo_indicator = "✅" if status["demo"] else "❌"
        telegram_indicator = "✅" if status["telegram"] else "❌"

        print(f"============ Mini Live Stats ================")
        print(f"Balance: {balance} | Profit: {profit} | Wins: {wins} | Losses: {losses}")
        print(f"Bot Demo: {demo_indicator} | Telegram: {telegram_indicator}")
        print("============================================")
        threading.Event().wait(MINI_STATS_REFRESH)

# ---------------- TELEGRAM LISTENER ----------------
async def start_telegram(status):
    from telethon import TelegramClient, events

    # Replace these with your credentials
    api_id = 26243332
    api_hash = "2d0ec7dc609caca15b573fc2d5239424"
    phone = "+254701022662"

    client = TelegramClient("quotex_session", api_id, api_hash)
    await client.start(phone=phone)
    status["telegram"] = True

    channels = [
        ("Binary_Bosss", 2111193817),
        ("Quotex_SuperBot", 1728487830),
        ("QuotexOTCHACK", 1983130297)
    ]
    for ch in channels:
        print(f"📡 Listening to {ch[0]} (id: {ch[1]})")

    @client.on(events.NewMessage(chats=[ch[1] for ch in channels]))
    async def handler(event):
        msg = event.message.message
        # Parse signal from message
        lines = msg.splitlines()
        symbol = None
        direction = None

        for line in lines:
            line_lower = line.lower()
            if "put" in line_lower or "call" in line_lower or "up" in line_lower or "down" in line_lower:
                direction = "put" if "put" in line_lower or "down" in line_lower else "call"
            if any(cur in line for cur in ["USD", "EUR", "GBP", "JPY", "BDT", "ARS"]):
                symbol = line.split()[0]

        if symbol and direction:
            # Schedule trade
            exec_time = datetime.utcnow() + timedelta(seconds=TRADE_WAIT_SEC)
            TRADE_BUFFER[symbol] = exec_time
            print(f"📩 Received signal: {symbol} {direction}, scheduled in {TRADE_WAIT_SEC}s")

            # Execute trade after wait
            delay = max((exec_time - datetime.utcnow()).total_seconds(), 0)
            threading.Timer(delay, execute_demo_trade, args=(symbol, direction, TRADE_AMOUNT)).start()

    await client.run_until_disconnected()

# ---------------- MAIN ----------------
async def main():
    print("🚀 Smart Trading Bot Running...")
    bot_status["demo"] = True

    # Start Telegram listener
    asyncio.create_task(start_telegram(bot_status))

    # Start mini stats loop in separate thread
    threading.Thread(target=mini_stats_loop, args=(bot_status,), daemon=True).start()

    # Keep main alive
    while True:
        await asyncio.sleep(1)

# ---------------- RUN ----------------
if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
import asyncio
import threading
import time
from datetime import datetime, timedelta

from quotex_demo_bot import execute_demo_trade  # Ensure this exists

# --- CONFIG ---
TRADE_WAIT_SEC = 5  # Default wait if signal arrives early
MINI_STATS_REFRESH = 5  # Refresh interval in seconds

# --- GLOBALS ---
balance = 1000.0
profit = 0.0
wins = 0
losses = 0
bot_status = {"demo": False, "telegram": False, "mini": False}
TRADE_BUFFER = {}  # buffer signals if missing direction, format: {symbol: {"time": datetime, "direction": None}}

# --- MINI STATS LOOP ---
def mini_stats_loop(bot_status):
    blink = True
    while True:
        status_demo = "✅" if bot_status["demo"] else "❌"
        status_telegram = "✅" if bot_status["telegram"] else "❌"
        status_mini = "✅" if blink and bot_status["demo"] else "❌"
        print(f"\rBalance: {balance:.2f} | Profit: {profit:.2f} | Wins: {wins} | Losses: {losses} | Bot Demo: {status_demo} | Telegram: {status_telegram}", end="")
        blink = not blink
        time.sleep(MINI_STATS_REFRESH)

# --- TRADE EXECUTION ---
def execute_trade(symbol, direction):
    """Execute the demo trade and update stats."""
    global balance, profit, wins, losses
    net = execute_demo_trade(symbol, direction)  # Should return profit/loss float
    balance += net
    profit += net
    if net > 0:
        wins += 1
    else:
        losses += 1
    print(f"\n💹 Trade executed: {symbol} {direction} | Net: {net:.2f} | Balance: {balance:.2f}")
    # Remove from buffer after execution
    if symbol in TRADE_BUFFER:
        del TRADE_BUFFER[symbol]

def schedule_trade(symbol, direction=None):
    """Schedule trade execution, handling delayed directions."""
    now = datetime.utcnow()
    if symbol in TRADE_BUFFER:
        # Update direction if it was missing
        if direction is not None and TRADE_BUFFER[symbol]["direction"] is None:
            TRADE_BUFFER[symbol]["direction"] = direction
            # Execute after wait if not already scheduled
            threading.Timer(TRADE_WAIT_SEC, execute_trade, args=(symbol, direction)).start()
            print(f"\n📩 Buffered trade executed: {symbol} {direction} after delay {TRADE_WAIT_SEC}s")
    else:
        # Buffer if direction is missing
        if direction is None:
            TRADE_BUFFER[symbol] = {"time": now, "direction": None}
            print(f"\n📩 Signal buffered for {symbol}, waiting for direction...")
        else:
            # Schedule immediately
            threading.Timer(TRADE_WAIT_SEC, execute_trade, args=(symbol, direction)).start()
            print(f"\n📩 Trade scheduled: {symbol} {direction} in {TRADE_WAIT_SEC}s")

# --- TELEGRAM LISTENER (async) ---
async def start_telegram(bot_status):
    bot_status["telegram"] = True
    print("\n📡 Telegram listener started...")
    # Mock channels
    channels = ["Binary_Bosss", "Quotex_SuperBot", "QuotexOTCHACK"]
    for ch in channels:
        print(f"📡 Listening to {ch} (mock)")
    # Replace this with real Telegram message handling
    while True:
        # Example of receiving signals in parts
        # Mock: first asset arrives
        await asyncio.sleep(10)  # Simulate message timing
        schedule_trade("USD BDT OTC")  # No direction yet
        # Mock: direction arrives 3 seconds later
        await asyncio.sleep(3)
        schedule_trade("USD BDT OTC", "CALL")

# --- MENU ---
def menu():
    while True:
        print("\n\n============================")
        print(" Smart Trading Bot - Menu")
        print("============================")
        print("1) Start Demo")
        print("2) Stop Bot")
        print("3) Restart Demo")
        print("4) Status")
        print("5) Open Full Dashboard")
        print("6) Launch Mini Live Stats")
        print("7) Exit")
        choice = input("----------------------------\nSelect option [1-7]: ")
        if choice == "1":
            start_demo()
        elif choice == "2":
            stop_bot()
        elif choice == "3":
            restart_demo()
        elif choice == "4":
            print(f"\nBalance: {balance:.2f} | Profit: {profit:.2f} | Wins: {wins} | Losses: {losses}")
        elif choice == "5":
            open_dashboard()
        elif choice == "6":
            launch_mini_stats()
        elif choice == "7":
            stop_bot()
            print("Exiting...")
            break
        else:
            print("Invalid option.")

# --- BOT CONTROL FUNCTIONS ---
def start_demo():
    if not bot_status["demo"]:
        bot_status["demo"] = True
        print("🚀 Demo bot started.")
    else:
        print("Demo bot already running.")

def stop_bot():
    bot_status["demo"] = False
    bot_status["telegram"] = False
    print("🛑 All bots stopped.")

def restart_demo():
    stop_bot()
    time.sleep(1)
    start_demo()

def launch_mini_stats():
    if not bot_status["mini"]:
        bot_status["mini"] = True
        threading.Thread(target=mini_stats_loop, args=(bot_status,), daemon=True).start()
        print("📊 Mini Live Stats launched.")
    else:
        print("Mini Live Stats already running.")

def open_dashboard():
    print("\n📈 Full Dashboard (mock)")
    print(f"Balance: {balance:.2f} | Profit: {profit:.2f} | Wins: {wins} | Losses: {losses}")
    print("Last Trades: (mock)")

# --- MAIN ---
async def main():
    print("🚀 Smart Trading Bot Running...")
    launch_mini_stats()
    await start_telegram(bot_status)
    menu()

if __name__ == "__main__":
    asyncio.run(main())
import threading
from datetime import datetime, timedelta

TRADE_BUFFER = {}
TRADE_WAIT_SEC = 5

def execute_demo_trade(symbol, direction):
    print(f"Executing trade: {symbol} {direction} at {datetime.utcnow()}")

def schedule_trade(symbol, direction, exec_time=None):
    if exec_time:
        delay = max((exec_time - datetime.utcnow()).total_seconds(), 0)
        threading.Timer(delay, execute_demo_trade, args=(symbol, direction)).start()
    else:
        threading.Timer(TRADE_WAIT_SEC, execute_demo_trade, args=(symbol, direction)).start()

def parse_symbol(message):
    # dummy parser
    if "USD" in message:
        return "USD BDT OTC"
    return None

def parse_direction(message):
    if "CALL" in message or "Up" in message:
        return "CALL"
    elif "PUT" in message or "Down" in message:
        return "PUT"
    return None

async def handle_signal_message(message):
    global TRADE_BUFFER
    symbol = parse_symbol(message)
    direction = parse_direction(message)

    if symbol and not direction:
        TRADE_BUFFER[symbol] = datetime.utcnow() + timedelta(seconds=TRADE_WAIT_SEC)
    elif symbol and direction:
        schedule_trade(symbol, direction)
        if symbol in TRADE_BUFFER:
            del TRADE_BUFFER[symbol]
    elif direction:
        for sym in list(TRADE_BUFFER):
            schedule_trade(sym, direction)
            del TRADE_BUFFER[sym]

# Example usage
import asyncio

async def main():
    print("🚀 Smart Trading Bot Running...")
    # Simulate receiving messages
    await handle_signal_message("USD BDT OTC.....")  # symbol only
    await asyncio.sleep(2)
    await handle_signal_message("Call / Up 👍")      # direction comes later
    # Keep loop alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio

async def main():
    try:
        print("🚀 Smart Trading Bot Running...")
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("\nBot task cancelled.")
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    finally:
        # Any cleanup can go here
        print("Cleaning up... Bye!")
        
if __name__ == "__main__":
    asyncio.run(main())
if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🚨 Bot stopped by user. Cleaning up...")
if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🚨 Bot stopped by user. Cleaning up...")
import asyncio
import threading
import re
from datetime import datetime, timedelta
from telethon import TelegramClient, events

# --- CONFIG ---
API_ID = 123456       # replace with your api_id
API_HASH = "your_api_hash"  # replace with your api_hash
PHONE = "+2547..."    # your phone number
TRADE_WAIT_SEC = 50   # default wait time before execution
TRADE_AMOUNT = 1      # demo trade amount

# --- GLOBAL STATE ---
BALANCE = 1000.0
PROFIT = 0.0
WINS = 0
LOSSES = 0
BOT_STATUS = {"demo": True, "telegram": False}
TRADE_BUFFER = {}   # store symbol waiting for direction

# --- TELEGRAM CLIENT ---
client = TelegramClient("quotex_session", API_ID, API_HASH)

# --- DEMO TRADE EXECUTION ---
def execute_demo_trade(symbol, direction):
    global BALANCE, PROFIT, WINS, LOSSES
    result = "WIN" if direction.lower() in ["call", "up"] else "LOSS"

    if result == "WIN":
        win_amount = TRADE_AMOUNT * 0.9
        BALANCE += win_amount
        PROFIT += win_amount
        WINS += 1
    else:
        BALANCE -= TRADE_AMOUNT
        PROFIT -= TRADE_AMOUNT
        LOSSES += 1

    print(f"✅ Trade executed: {symbol} {direction} | Result: {result} | Balance: {BALANCE:.2f}")

# --- SCHEDULER ---
def schedule_trade(symbol, direction, exec_time=None):
    if exec_time:
        delay = max((exec_time - datetime.utcnow()).total_seconds(), 0)
    else:
        delay = TRADE_WAIT_SEC
    threading.Timer(delay, execute_demo_trade, args=(symbol, direction)).start()
    print(f"📩 Scheduled {symbol} {direction} trade in {delay}s")

# --- SIGNAL PARSING ---
def parse_symbol(msg: str):
    match = re.search(r"([A-Z]{3,4}[-/]?[A-Z]{3,4}[-]?OTC)", msg)
    return match.group(1) if match else None

def parse_direction(msg: str):
    msg = msg.lower()
    if "call" in msg or "up" in msg or "🟢" in msg:
        return "CALL"
    if "put" in msg or "down" in msg or "🔴" in msg:
        return "PUT"
    return None

# --- TELEGRAM HANDLER ---
async def handle_signal_message(message: str):
    global TRADE_BUFFER
    symbol = parse_symbol(message)
    direction = parse_direction(message)

    if symbol and not direction:
        # Buffer the signal until direction arrives
        TRADE_BUFFER[symbol] = datetime.utcnow() + timedelta(seconds=TRADE_WAIT_SEC)
        print(f"🕓 Buffered symbol {symbol}, waiting for direction...")
    elif symbol and direction:
        # Immediate execution
        schedule_trade(symbol, direction)
        TRADE_BUFFER.pop(symbol, None)
    elif direction:
        # If only direction arrives, attach to buffered symbol
        for sym in list(TRADE_BUFFER.keys()):
            schedule_trade(sym, direction)
            TRADE_BUFFER.pop(sym, None)

@client.on(events.NewMessage)
async def telegram_listener(event):
    BOT_STATUS["telegram"] = True
    msg = event.message.message
    await handle_signal_message(msg)

# --- MINI STATS LOOP ---
def mini_stats_loop():
    while True:
        status_line = (
            f"Balance: {BALANCE:.2f} | Profit: {PROFIT:.2f} | Wins: {WINS} | Losses: {LOSSES} | "
            f"Bot Demo: {'✅' if BOT_STATUS['demo'] else '❌'} | Telegram: {'✅' if BOT_STATUS['telegram'] else '❌'}"
        )
        print("\n" + "="*40)
        print(status_line)
        print("="*40)
        asyncio.run(asyncio.sleep(5))  # refresh every 5s

# --- MAIN LOOP ---
async def main():
    print("🚀 Smart Trading Bot Running...")
    threading.Thread(target=mini_stats_loop, daemon=True).start()
    await client.start(phone=PHONE)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
def menu(bot_status):
    while True:
        print("============================")
        print(" Smart Trading Bot - Menu")
        print("============================")
        print("1) Start Demo")
        print("2) Stop Bot")
        print("3) Restart Demo")
        print("4) Status")
        print("5) Open Full Dashboard")
        print("6) Toggle Mini Live Stats")
        print("7) Exit")
        print("----------------------------")

        choice = input("Select option [1-7]: ").strip()

        if choice == "1":
            bot_status["demo"] = True
            print("🚀 Demo Bot Started")
        elif choice == "2":
            bot_status["demo"] = False
            print("🛑 Bot Stopped")
        elif choice == "3":
            bot_status["demo"] = False
            print("🔄 Restarting Demo Bot...")
            time.sleep(1)
            bot_status["demo"] = True
            print("🚀 Demo Bot Restarted")
        elif choice == "4":
            print("============== Bot Status ==============")
            print(f"Balance: {BALANCE:.2f} | Profit: {PROFIT:.2f} | Wins: {WINS} | Losses: {LOSSES}")
            print(f"Bot Status: Demo {'✅' if bot_status['demo'] else '❌'} | Telegram {'✅' if bot_status['telegram'] else '❌'} | Mini Stats {'✅' if MINI_STATS_RUNNING else '❌'}")
            print("========================================")
        elif choice == "5":
            print("📊 Opening Full Dashboard (future feature)...")
        elif choice == "6":
            toggle_mini_stats(bot_status)
        elif choice == "7":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option, try again.")
