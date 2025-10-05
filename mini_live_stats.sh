#!/bin/bash
REFRESH_INTERVAL=5
while true; do
    clear
    BALANCE=$(cat ~/project_tb/balance.txt 2>/dev/null || echo "0")
    WINS=$(cat ~/project_tb/wins.txt 2>/dev/null || echo "0")
    LOSSES=$(cat ~/project_tb/losses.txt 2>/dev/null || echo "0")
    PROFIT=$(cat ~/project_tb/profit.txt 2>/dev/null || echo "0")
    DEMO_RUNNING=$(pgrep -f quotex_demo_bot.py >/dev/null && echo "✅" || echo "❌")
    LIVE_RUNNING=$(pgrep -f quotex_live_bot.py >/dev/null && echo "✅" || echo "❌")
    TELEGRAM_RUNNING=$(pgrep -f quotex_demo_telegram.py >/dev/null && echo "✅" || echo "❌")

    echo "================ Mini Live Stats ================"
    echo "Balance: $BALANCE | Profit: $PROFIT | Wins: $WINS | Losses: $LOSSES"
    echo "Bot Status: Demo $DEMO_RUNNING | Live $LIVE_RUNNING | Telegram $TELEGRAM_RUNNING"
    echo "================================================"
    echo "---------------- Last 5 Trades ----------------"
    tail -n 5 ~/project_tb/trades.log 2>/dev/null || echo "No trades yet."
    echo "---------------- Last 5 Signals ----------------"
    tail -n 5 ~/project_tb/signals.log 2>/dev/null || echo "No signals yet."
    echo "================================================"
    echo "Press Ctrl+C to exit"
    sleep $REFRESH_INTERVAL
done
