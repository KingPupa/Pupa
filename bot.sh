#!/bin/bash

# Path to your project folder
PROJECT_DIR="$HOME/project_tb"
MAIN_FILE="main.py"
PID_FILE="$PROJECT_DIR/bot.pid"

cd "$PROJECT_DIR" || exit

start_bot() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "🚫 Bot is already running."
    else
        echo "🚀 Starting Smart Trading Bot..."
        nohup python3 "$MAIN_FILE" > bot.log 2>&1 &
        echo $! > "$PID_FILE"
        echo "✅ Bot started with PID $(cat $PID_FILE)"
    fi
}

stop_bot() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        kill $(cat "$PID_FILE")
        rm "$PID_FILE"
        echo "🛑 Bot stopped."
    else
        echo "⚠️ Bot is not running."
    fi
}

status_bot() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "✅ Bot is running (PID $(cat $PID_FILE))"
    else
        echo "⚠️ Bot is not running."
    fi
}

case "$1" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        stop_bot
        start_bot
        ;;
    status)
        status_bot
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        ;;
esac
#!/bin/bash

BOT_PATH=~/project_tb/main.py
PID_FILE=~/project_tb/bot.pid
MODE_FILE=~/project_tb/mode.txt   # Stores current mode (DEMO or REAL)

start() {
    if [ -f "$PID_FILE" ]; then
        echo "🟢 Bot already running."
        return
    fi
    nohup python3 $BOT_PATH > ~/project_tb/bot.log 2>&1 &
    echo $! > $PID_FILE
    echo "🚀 Bot started in $(cat $MODE_FILE) mode with PID $(cat $PID_FILE)"
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "⚠️ Bot is not running."
        return
    fi
    kill $(cat $PID_FILE) && rm -f $PID_FILE
    echo "🛑 Bot stopped."
}

status() {
    if [ -f "$PID_FILE" ] && ps -p $(cat $PID_FILE) > /dev/null; then
        echo "✅ Bot is running (PID $(cat $PID_FILE)), Mode: $(cat $MODE_FILE)"
    else
        echo "⚠️ Bot is not running."
    fi
}

set_mode() {
    echo "$1" > $MODE_FILE
    echo "Mode set to $1"
}

start_demo() {
    set_mode DEMO
    start
}

start_real() {
    set_mode REAL
    start
}

restart() {
    stop
    start
}

case "$1" in
start) start ;;
stop) stop ;;
status) status ;;
restart) restart ;;
demo) start_demo ;;
real) start_real ;;
*) echo "Usage: $0 {start|stop|status|restart|demo|real}" ;;
esac
#!/bin/bash

MAIN_PY="$HOME/project_tb/main.py"
PID_FILE="$HOME/project_tb/bot.pid"
MODE_FILE="$HOME/project_tb/mode.txt"

start_bot() {
    mode=$1
    echo "$mode" > $MODE_FILE
    if [ -f "$PID_FILE" ]; then
        pid=$(cat $PID_FILE)
        if kill -0 $pid 2>/dev/null; then
            echo "🟢 Bot already running (PID $pid)"
            return
        fi
    fi
    echo "🚀 Starting Smart Trading Bot in $mode mode..."
    python3 $MAIN_PY &
    echo $! > $PID_FILE
    echo "✅ Bot started with PID $(cat $PID_FILE)"
}

stop_bot() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat $PID_FILE)
        if kill -0 $pid 2>/dev/null; then
            kill $pid
            echo "🛑 Bot stopped."
        else
            echo "⚠️ Bot is not running."
        fi
        rm -f $PID_FILE
    else
        echo "⚠️ Bot is not running."
    fi
}

status_bot() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat $PID_FILE)
        if kill -0 $pid 2>/dev/null; then
            echo "✅ Bot is running (PID $pid)"
        else
            echo "⚠️ Bot is not running."
        fi
    else
        echo "⚠️ Bot is not running."
    fi
}

# Read last mode if exists
LAST_MODE="DEMO"
if [ -f "$MODE_FILE" ]; then
    LAST_MODE=$(cat $MODE_FILE)
fi

case "$1" in
    start)
        start_bot "DEMO"
        ;;
    stop)
        stop_bot
        ;;
    restart)
        stop_bot
        start_bot "$LAST_MODE"
        ;;
    status)
        status_bot
        ;;
    demo)
        stop_bot
        start_bot "DEMO"
        ;;
    real)
        stop_bot
        start_bot "REAL"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|demo|real}"
        ;;
esac
#!/bin/bash

MAIN_PY="$HOME/project_tb/main.py"
PID_FILE="$HOME/project_tb/bot.pid"
MODE_FILE="$HOME/project_tb/mode.txt"

start_bot() {
    mode=$1
    echo "$mode" > $MODE_FILE
    if [ -f "$PID_FILE" ]; then
        pid=$(cat $PID_FILE)
        if kill -0 $pid 2>/dev/null; then
            echo "🟢 Bot already running (PID $pid)"
            return
        fi
    fi
    echo "🚀 Starting Smart Trading Bot in $mode mode..."
    python3 $MAIN_PY &
    echo $! > $PID_FILE
    echo "✅ Bot started with PID $(cat $PID_FILE)"
}

stop_bot() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat $PID_FILE)
        if kill -0 $pid 2>/dev/null; then
            kill $pid
            echo "🛑 Bot stopped."
        else
            echo "⚠️ Bot is not running."
        fi
        rm -f $PID_FILE
    else
        echo "⚠️ Bot is not running."
    fi
}

status_bot() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat $PID_FILE)
        if kill -0 $pid 2>/dev/null; then
            echo "✅ Bot is running (PID $pid)"
        else
            echo "⚠️ Bot is not running."
        fi
    else
        echo "⚠️ Bot is not running."
    fi
}

case "$1" in
    start|demo)
        stop_bot
        start_bot "DEMO"
        ;;
    real)
        stop_bot
        start_bot "REAL"
        ;;
    stop)
        stop_bot
        ;;
    restart)
        stop_bot
        start_bot "DEMO"
        ;;
    status)
        status_bot
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|demo|real}"
        ;;
esac
