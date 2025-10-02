# Telegram Group Signal Listener

This script uses the Telethon library to listen for new messages in a specific Telegram group and prints them to the console.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure the script:**
    Open `main.py` and replace the placeholder values with your own:
    -   `'YOUR_API_ID'`: Your Telegram API ID.
    -   `'YOUR_API_HASH'`: Your Telegram API hash.
    -   `'YOUR_PHONE_NUMBER'`: Your phone number associated with your Telegram account (in international format, e.g., `+1234567890`).
    -   `'YourGroupUsername'`: The username of the public Telegram group you want to listen to. For private groups, you may need to use the group's ID.

    You can get your `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).

## Usage

Run the script from your terminal:
```bash
python main.py
```

The first time you run the script, you will be prompted to enter your phone number, password (if you have one), and a login code sent to you by Telegram. After a successful login, a `session_name.session` file will be created. This file stores your session, so you won't have to log in again.

Once running, the script will print "New Signal:" followed by the message text for every new message in the specified group.