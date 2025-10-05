# paste the script, then Ctrl+O, Enter, Ctrl+X#!/usr/bin/env python3
"""
quotex_demo_bot.py
Demo-mode trading simulator for testing dashboard & trade flow.

Features:
- "Login" (simulated)
- Place demo trades (amount, direction, duration)
- Random win/loss outcome (configurable win_rate)
- Applies payout percentage to compute profit/loss
- Updates: wins.txt, losses.txt, profit.txt, balance.txt, trades.log
- Safe: no network calls, no real broker interaction
"""

import os
import time
import random
from datetime import datetime

# ===== CONFIG =====
USER_EMAIL = "demo_user@example.com"    # just for display in logs
STARTING_BALANCE = 1000.0               # starting demo balance
BALANCE_FILE = os.path.expanduser("~/project_tb/balance.txt")
WINS_FILE = os.path.expanduser("~/project_tb/wins.txt")
LOSSES_FILE = os.path.expanduser("~/project_tb/losses.txt")
PROFIT_FILE = os.path.expanduser("~/project_tb/profit.txt")
TRADE_LOG = os.path.expanduser("~/project_tb/trades.log")

PAYOUT = 0.85       # 85% payout on winning trade (typical binary payout)
WIN_RATE = 0.5      # probability of a win in simulation (50% default)
RANDOM_SEED = None  # set to int for reproducible tests

# ===== Helpers =====
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
    # initialize stats files if missing
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

def read_stats():
    wins = int(safe_read(WINS_FILE, "0") or "0")
    losses = int(safe_read(LOSSES_FILE, "0") or "0")
    profit = float(safe_read(PROFIT_FILE, "0") or "0")
    balance_raw = safe_read(BALANCE_FILE, f"{STARTING_BALANCE:.2f}")
    # balance file may contain "123.45 USD" if you used currency, so extract number
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

# ===== Core: simulate a trade =====
def simulate_trade(asset="EURUSD", amount=1.0, direction="call", duration=60):
    wins, losses, profit, balance = read_stats()

    # check enough balance
    if amount <= 0:
        print("Amount must be > 0")
        return
    if amount > balance:
        print(f"Insufficient balance ({balance:.2f}) for amount {amount:.2f}")
        return

    # lock randomness
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED + int(time.time()))

    # determine result
    win = random.random() < WIN_RATE

    if win:
        payout_amount = amount * PAYOUT
        net = payout_amount  # profit on top of stake (common way to represent)
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

    # format and save
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    trade_id = f"DEMO-{int(time.time()*1000)}"
    log_line = (
        f"{timestamp} | {trade_id} | {asset} | {direction} | "
        f"{amount:.2f} | {duration}s | {result} | net:{net:.2f} | bal:{balance:.2f}"
    )
    log_trade(log_line)
    write_stats(wins, losses, profit, balance)

    # print summary
    print("=== Demo Trade Result ===")
    print(log_line)
    return {
        "trade_id": trade_id,
        "asset": asset,
        "direction": direction,
        "amount": amount,
        "duration": duration,
        "result": result,
        "net": net,
        "balance": balance
    }

# ===== CLI Interface =====
def print_stats():
    wins, losses, profit, balance = read_stats()
    print("---- Current Stats ----")
    print(f"Wins:    {wins}")
    print(f"Losses:  {losses}")
    print(f"Profit:  {profit:.2f}")
    print(f"Balance: {balance:.2f}")
    print("-----------------------")

def interactive_shell():
    print("Quotex DEMO bot (simulator). No network. Files updated for dashboard.")
    print(f"Stats files in ~/project_tb: {WINS_FILE}, {LOSSES_FILE}, {PROFIT_FILE}, {BALANCE_FILE}")
    print("Commands: stats | trade | setbal | reset | exit | help")
    while True:
        cmd = input("cmd> ").strip().lower()
        if cmd in ("exit", "quit"):
            print("Bye.")
            break
        if cmd == "help":
            print("Commands:")
            print("  stats                 show current stats")
            print("  trade                 run a demo trade interactively")
            print("  trade <amt> <dir>     e.g. trade 1 call  (dir: call/put)")
            print("  setbal <amount>       set balance to amount")
            print("  reset                 reset stats to starting balance and zeros")
            print("  exit                  quit")
            continue
        if cmd == "stats":
            print_stats()
            continue
        if cmd.startswith("trade"):
            parts = cmd.split()
            if len(parts) == 1:
                amt = float(input("Amount? ") or "1")
                dirn = input("Direction (call/put)? ") or "call"
            else:
                try:
                    amt = float(parts[1])
                    dirn = parts[2] if len(parts) > 2 else "call"
                except:
                    print("Invalid trade syntax. Example: trade 1 call")
                    continue
            simulate_trade(amount=amt, direction=dirn)
            continue
        if cmd.startswith("setbal"):
            parts = cmd.split()
            if len(parts) != 2:
                print("Usage: setbal <amount>")
                continue
            try:
                newbal = float(parts[1])
                wins, losses, profit, _ = read_stats()
                write_stats(wins, losses, profit, newbal)
                print(f"Balance set to {newbal:.2f}")
            except:
                print("Invalid amount")
            continue
        if cmd == "reset":
            safe_write(WINS_FILE, "0")
            safe_write(LOSSES_FILE, "0")
            safe_write(PROFIT_FILE, "0.00")
            safe_write(BALANCE_FILE, f"{STARTING_BALANCE:.2f}")
            with open(TRADE_LOG, "w") as f:
                f.write("# trades log\n")
            print("Stats reset.")
            continue
        print("Unknown command. Type help for commands.")

# ===== Main =====
if __name__ == "__main__":
    init_files()
    # If run with args, e.g. python quotex_demo_bot.py trade 1 call
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "trade":
            amt = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
            dirn = sys.argv[3] if len(sys.argv) > 3 else "call"
            simulate_trade(amount=amt, direction=dirn)
        elif cmd == "stats":
            print_stats()
        elif cmd == "reset":
            safe_write(WINS_FILE, "0")
            safe_write(LOSSES_FILE, "0")
            safe_write(PROFIT_FILE, "0.00")
            safe_write(BALANCE_FILE, f"{STARTING_BALANCE:.2f}")
            print("Reset done.")
        else:
            print("Unknown arg. Supported: trade | stats | reset")
    else:
        interactive_shell()
# --- Demo trade function ---
def execute_demo_trade(symbol, direction, amount):
    """
    Executes a demo trade (simulated) and updates stats files.
    """
    from datetime import datetime
    import random
    WIN_RATE = 0.5  # 50% chance win
    PAYOUT = 0.85   # 85% payout

    # Read current balance
    try:
        with open("balance.txt") as f:
            balance = float(f.read().strip())
    except:
        balance = 1000.0

    # Determine win/loss
    result = "WIN" if random.random() < WIN_RATE else "LOSS"
    net = amount * PAYOUT if result == "WIN" else -amount
    balance += net

    # Update stats files
    with open("balance.txt", "w") as f:
        f.write(f"{balance:.2f}")

    try:
        with open("profit.txt") as f:
            profit = float(f.read().strip())
    except:
        profit = 0.0
    profit += net
    with open("profit.txt", "w") as f:
        f.write(f"{profit:.2f}")

    try:
        with open("wins.txt") as f:
            wins = int(f.read().strip())
    except:
        wins = 0
    try:
        with open("losses.txt") as f:
            losses = int(f.read().strip())
    except:
        losses = 0

    if result == "WIN":
        wins += 1
    else:
        losses += 1

    with open("wins.txt", "w") as f:
        f.write(str(wins))
    with open("losses.txt", "w") as f:
        f.write(str(losses))

    # Print summary
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"{timestamp} | DEMO | {symbol} | {direction.upper()} | {amount} | {result} | net:{net:.2f} | bal:{balance:.2f}")
