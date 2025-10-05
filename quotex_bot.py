import requests
import json
import time
import os

# ===== CONFIG =====
EMAIL = "your_email@example.com"      # <-- put your Quotex email
PASSWORD = "your_password_here"       # <-- put your Quotex password
CURRENCY_PAIR = "EURUSD_otc"          # Example asset
AMOUNT = 1                            # Amount per test trade
DIRECTION = "call"                    # "call" = up, "put" = down
EXPIRY = 60                           # Expiry in seconds (1 min)

SESSION = requests.Session()

def login():
    url = "https://api.quotex.io/v1/auth/signin"
    data = {"email": EMAIL, "password": PASSWORD}
    r = SESSION.post(url, data=data)
    if r.status_code == 200:
        print("[+] Logged in successfully")
        return True
    else:
        print("[-] Login failed:", r.text)
        return False

def get_balance():
    url = "https://api.quotex.io/v1/profile"
    r = SESSION.get(url)
    if r.status_code == 200:
        profile = r.json()
        balance = profile["data"]["balance"]
        currency = profile["data"]["currency"]
        print(f"[+] Balance: {balance} {currency}")

        # Save to file for dashboard
        with open(os.path.expanduser("~/project_tb/balance.txt"), "w") as f:
            f.write(f"{balance} {currency}")

        return balance
    else:
        print("[-] Could not fetch balance:", r.text)
        return None

def place_trade():
    url = "https://api.quotex.io/v1/trade"
    data = {
        "asset": CURRENCY_PAIR,
        "amount": AMOUNT,
        "action": DIRECTION,
        "duration": EXPIRY
    }
    r = SESSION.post(url, json=data)
    if r.status_code == 200:
        print("[+] Trade placed successfully:", r.json())
    else:
        print("[-] Trade failed:", r.text)

if __name__ == "__main__":
    if login():
        get_balance()
        print("[*] Placing test trade...")
        place_trade()
        time.sleep(5)
        get_balance()
