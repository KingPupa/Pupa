# Telegram Group Signal Listener & Trader

This script uses the Telethon library to listen for new messages in a specific Telegram group, parses them as trading signals, and executes a placeholder trade.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create your configuration file:**
    Rename `config.example.json` to `config.json`.

3.  **Update `config.json`:**
    Open `config.json` and fill in your API details:
    -   `"api_id"`: Your Telegram API ID.
    -   `"api_hash"`: Your Telegram API hash.
    -   `"phone"`: Your phone number associated with your Telegram account (in international format, e.g., `+1234567890`).

    You can get your `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).

4.  **Configure Target Group and Trade Amount:**
    Open `main.py` and edit the following values directly in the script:
    -   In the `@client.on(events.NewMessage(chats='YourGroupUsername'))` line, replace `'YourGroupUsername'` with the username of the target group.
    -   In the `handler` function, find the `execute_trade(...)` call and change `amount=1` to your desired test trade amount.

## Usage

Run the script from your terminal:
```bash
python main.py
```

The first time you run the script, you will be prompted for your login details. After a successful login, a `session_name.session` file will be created to store your session.

Once running, the script will listen for messages. If a message is a valid signal (e.g., `"BUY BTC 1h"`), it will be parsed, and a trade will be executed.

### Example Output

For a valid signal like `"BUY BTC 1h"`, the output will be:
```
--- EXECUTING TRADE ---
  Action: BUY
  Asset: BTC
  Duration: 1h
  Amount: $1
-----------------------
```

If a message cannot be parsed, no output will be generated.