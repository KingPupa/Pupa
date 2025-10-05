#!/bin/bash
# ================= Delete Old Smart Trading Bot Files =================

echo "Stopping all running bot processes..."
pkill -f quotex_demo_bot.py
pkill -f quotex_live_bot.py
pkill -f quotex_demo_telegram.py
pkill -f mini_live_stats.sh

echo "Deleting old menu and dashboard scripts..."
rm -f ~/project_tb/shortcuts
rm -f ~/project_tb/mini_live_stats.sh
rm -f ~/project_tb/live_dashboard.sh

echo "Deleting old trade, signal, and stats logs..."
rm -f ~/project_tb/balance.txt
rm -f ~/project_tb/wins.txt
rm -f ~/project_tb/losses.txt
rm -f ~/project_tb/profit.txt
rm -f ~/project_tb/trades.log
rm -f ~/project_tb/signals.log

echo "Old bot setup successfully deleted."
