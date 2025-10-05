#!/data/data/com.termux/files/usr/bin/bash

PROJECT_DIR=~/project_tb

while true; do
    clear
    echo "============================"
    echo " Smart Trading Bot - Dashboard"
    echo "============================"

    # Read stats from trades.log
    WINS=$(grep -c "Profit" $PROJECT_DIR/trades.log 2>/dev/null || echo 0)
    LOSSES=$(grep -c "Loss" $PROJECT_DIR/trades.log 2>/dev/null || echo 0)
    PROFIT=$(awk -F '|' '{sum += $7} END {print sum}' $PROJECT_DIR/trades.log 2>/dev/null || echo 0)

    echo "Wins: $WINS"
    echo "Losses: $LOSSES"
    echo "Profit: $PROFIT$"

    echo "----------------------------"
    echo "Press Ctrl+C to exit dashboard"
    sleep 2
done
#!/data/data/com.termux/files/usr/bin/bash

LOG_FILE="$HOME/project_tb/trades.log"

while true; do
    clear
    echo "=========================="
    echo " Smart Trading Bot - Dashboard"
    echo "=========================="

    if [ ! -f "$LOG_FILE" ]; then
        echo "No trades logged yet."
        sleep 2
        continue
    fi

    # Count Wins and Losses
    WINS=$(grep -c "Profit" "$LOG_FILE")
    LOSSES=$(grep -c "Loss" "$LOG_FILE")
    
    # Calculate total profit
    TOTAL=$(awk -F '|' '{sum+=$7} END {print sum+0}' "$LOG_FILE")  # Column 7 = profit_loss

    echo "Wins: $WINS"
    echo "Losses: $LOSSES"
    echo "Profit: ${TOTAL}$"
    echo "----------------------------"
    echo "Press Ctrl+C to exit dashboard"

    sleep 2
done
