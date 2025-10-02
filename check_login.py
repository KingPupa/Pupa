from pyquotex import Quotex
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("QUOTEX_EMAIL")
PASSWORD = os.getenv("QUOTEX_PASSWORD")

try:
    quotex = Quotex(email=EMAIL, password=PASSWORD)
    balance = quotex.get_balance()
    print(f"[SUCCESS] Logged in. Current balance: ${balance}")
except Exception as e:
    print("[ERROR] Login failed:", e)