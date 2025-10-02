# Project TB Final Auto-Trader

This script is an automated Telegram signal trader for the Quotex platform. It uses the Telethon library to monitor specified Telegram groups for trading signals and the `pyquotex` library to execute them. It includes safety features to limit trading frequency and maximum potential loss.

## Features
- **Automated Trading**: Listens to multiple Telegram groups and automatically places trades on Quotex when a valid signal is detected.
- **Environment-based Configuration**: All sensitive credentials (Telegram and Quotex) are managed via a `.env` file for improved security.
- **Periodic Balance & P/L Monitoring**: Prints the current account balance and the total session profit/loss to the console every 5 minutes (by default).
- **Trade Retries**: Automatically retries a failed trade a configurable number of times, making the bot more resilient to temporary API errors.
- **Safety Limits**:
  - `MAX_TRADES_PER_HOUR`: Limits the number of trades the bot can place within a rolling one-hour window.
  - `MAX_LOSS`: Stops the bot from trading if the real-time account balance drops below the starting balance by this amount. This provides an accurate, real-time stop-loss for the session.

## Setup

1.  **Install Dependencies:**
    Make sure you have Python installed. Then, install the required libraries using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Up Credentials:**
    Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Open the new `.env` file and fill in your credentials for both Telegram and Quotex.

3.  **Verify Quotex Login (Optional but Recommended):**
    Before running the main bot, you can verify that your Quotex credentials are correct by running the `check_login.py` script:
    ```bash
    python check_login.py
    ```
    If successful, it will print your current account balance. If not, it will print an error, and you should double-check your `.env` file.

4.  **Configure Bot Settings:**
    Open `project_tb_bot_final.py` and configure the following settings to your preference:
    -   `telegram_groups`: A Python list of the Telegram group usernames you want to monitor (e.g., `['@GroupName1', '@GroupName2']`).
    -   `trade_amount`: The amount (in USD) to be used for each trade.
    -   `TRADE_RETRIES`: The number of times to retry a failed trade attempt.
    -   `MAX_TRADES_PER_HOUR`: The maximum number of trades to execute in one hour.
    -   `MAX_LOSS`: The maximum amount of money the bot is allowed to lose in a session before stopping.

## Usage

Run the bot from your terminal:
```bash
python project_tb_bot_final.py
```

The first time you run the script, you will be prompted to enter your Telegram login details (phone number, password, and a login code sent to you by Telegram). After a successful login, a `project_tb_session.session` file will be created to store your session, so you won't have to log in again.

The bot will then connect to Quotex and start listening for messages. When a valid signal is detected and safety limits have not been reached, it will attempt to execute a trade.

### Disclaimer
Trading carries a high level of risk and may not be suitable for all investors. Before deciding to trade, you should carefully consider your investment objectives, level of experience, and risk appetite. The possibility exists that you could sustain a loss of some or all of your initial investment. You should be aware of all the risks associated with trading and seek advice from an independent financial advisor if you have any doubts. This script is for educational purposes only and is not financial advice. Use at your own risk.