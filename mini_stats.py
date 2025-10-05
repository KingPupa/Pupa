# ~/project_tb/mini_stats.py
import time
import os

# Shared stats (later you can connect these with your main bot’s data file/db)
balance = 1000.0
profit = 0.0
wins = 0
losses = 0

def show_stats():
    os.system("clear")  # clears terminal like bash 'clear'
    print("============== Mini Live Stats ===============")
    print(f"Balance: {balance:.2f} | Profit: {profit:.2f} | Wins: {wins} | Losses: {losses}")
    print("Bot Status: Demo ✅ | Telegram ✅ | Mini Stats ✅")
    print("=============================================")

if __name__ == "__main__":
    try:
        while True:
            show_stats()
            time.sleep(2)  # refresh every 2 seconds
    except KeyboardInterrupt:
        print("\n👋 Mini Stats closed.")
