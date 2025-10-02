# Project TB Bot - Telegram Signal Trader

This script uses the Telethon library to listen for new messages in a list of specified Telegram groups. When a message matching a signal format (e.g., "BUY EURUSD 1m") is detected, it executes a trade on the Quotex platform using the `pyquotex` library.

## Setup

1.  **Install Dependencies:**
    Make sure you have Python installed. Then, install the required libraries using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Up Quotex Credentials:**
    Create a `.env` file in the root of the project by copying the `.env.example` file.
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and fill in your Quotex account details:
    ```
    QUOTEX_EMAIL="your_email@example.com"
    QUOTEX_PASSWORD="your_quotex_password"
    ```

3.  **Configure Telegram and Trading Settings:**
    Open the `project_tb_bot.py` file and edit the following values directly in the script:
    -   `api_id`: Your Telegram API ID.
    -   `api_hash`: Your Telegram API Hash.
    -   `phone`: Your phone number associated with your Telegram account.
    -   `telegram_groups`: A list of the Telegram group usernames you want to monitor.
    -   `trade_amount`: The amount (in USD) to be used for each trade.

    You can get your Telegram `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).

## Usage

Run the bot from your terminal:
```bash
python project_tb_bot.py
```

The first time you run the script, you will be prompted to enter your Telegram login details (phone number, password, and a login code sent to you by Telegram). After a successful login, a `project_tb_session.session` file will be created to store your session, so you won't have to log in again.

The bot will then connect to Quotex and start listening for messages in the specified Telegram groups. When a valid signal is detected, it will attempt to execute a trade.

### Disclaimer
Trading carries a high level of risk and may not be suitable for all investors. Before deciding to trade, you should carefully consider your investment objectives, level of experience, and risk appetite. The possibility exists that you could sustain a loss of some or all of your initial investment. You should be aware of all the risks associated with trading and seek advice from an independent financial advisor if you have any doubts. This script is for educational purposes only and is not financial advice. Use at your own risk.