import asyncio
import threading
import re
from datetime import datetime, timedelta
from telethon import TelegramClient, events

API_ID = 123456
API_HASH = "your_api_hash"
PHONE = "+2547..."
TRADE_WAIT_SEC = 50
TRADE_AMOUNT = 1

BALANCE = 1000.0
PROFIT = 0.0
WINS = 0
LOSSES = 0
BOT_STATUS = {"demo": True, "telegram": False}

client = TelegramClient("quotex_session", API_ID, API_HASH)

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

def schedule_trade(symbol, direction, exec_time=None):
    if exec_time:
        delay = max((exec_time - datetime.utcnow()).total_seconds(), 0)
    else:
        delay = TRADE_WAIT_SEC
    threading.Timer(delay, execute_demo_trade, args=(symbol, direction)).start()
    print(f"📩 Scheduled {symbol} {direction} trade in {delay}s")

def parse_symbol(msg: str):
    match = re.search(r"([A-Z]{3,4}[-/]?[A-Z]{3,4}[-]?OTC)", msg)
    return match.group(1) if match else None

def parse_direction(msg: str):
    msg = msg.lower()
    if "call" in msg or "up" in msg:
        return "CALL"
    if "put" in msg or "down" in msg:
        return "PUT"
    return None

async def handle_signal_message(message: str):
    symbol = parse_symbol(message)
    direction = parse_direction(message)

    if symbol and direction:
        schedule_trade(symbol, direction)

@client.on(events.NewMessage)
async def telegram_listener(event):
    BOT_STATUS["telegram"] = True
    msg = event.message.message
    await handle_signal_message(msg)

def mini_stats_loop():
    while True:
        status_line = (
            f"Balance: {BALANCE:.2f} | Profit: {PROFIT:.2f} | Wins: {WINS} | Losses: {LOSSES} | "
            f"Bot Demo: {'✅' if BOT_STATUS['demo'] else '❌'} | Telegram: {'✅' if BOT_STATUS['telegram'] else '❌'}"
        )
        print("\n" + "="*40)
        print(status_line)
        print("="*40)
        asyncio.run(asyncio.sleep(5))

async def main():
    print("🚀 Backup Trading Bot Running...")
    threading.Thread(target=mini_stats_loop, daemon=True).start()
    await client.start(phone=PHONE)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
