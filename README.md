# Telegram Group Signal Listener

This script uses the Telethon library to listen for new messages in a specific Telegram group and prints them to the console.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create your configuration file:**
    Rename `config.example.json` to `config.json`.

3.  **Update `config.json`:**
    Open `config.json` and fill in your details:
    -   `"api_id"`: Your Telegram API ID.
    -   `"api_hash"`: Your Telegram API hash.
    -   `"phone"`: Your phone number associated with your Telegram account (in international format, e.g., `+1234567890`).
    -   `"group_username"`: The username of the public Telegram group you want to listen to. For private groups, you may need to use the group's ID.

    You can get your `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).

## Usage

Run the script from your terminal:
```bash
python main.py
```

The first time you run the script, you will be prompted to enter your phone number, password (if you have one), and a login code sent to you by Telegram. After a successful login, a `session_name.session` file will be created. This file stores your session, so you won't have to log in again.

Once running, the script will listen for messages in the specified group. If a message is a valid signal (composed of three parts: action, asset, and duration), it will be parsed and printed in a structured format.

### Example Output

For a valid signal like `"BUY BTC 1h"`, the output will be:
```
New Signal Received:
  Action: BUY
  Asset: BTC
  Duration: 1h
```

If a message cannot be parsed, the script will print the original message, indicating that it could not be parsed.