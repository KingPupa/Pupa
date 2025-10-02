import json
from telethon import TelegramClient, events

# Load configuration from config.json
try:
    with open('config.json') as config_file:
        config = json.load(config_file)
    api_id = config['api_id']
    api_hash = config['api_hash']
    phone = config['phone']
except FileNotFoundError:
    print("Error: config.json not found. Please create it.")
    exit()
except KeyError as e:
    print(f"Error: Missing key in config.json: {e}")
    exit()

# Create client
client = TelegramClient('session_name', api_id, api_hash)

def parse_signal(message):
    """Parses a signal message into action, asset, and duration."""
    parts = message.split()
    if len(parts) == 3:
        action, asset, duration = parts
        return action, asset, duration
    return None, None, None

def execute_trade(action, asset, duration, amount):
    """Placeholder function to execute a trade."""
    # In a real application, this would connect to a broker's API.
    print(f"--- EXECUTING TRADE ---")
    print(f"  Action: {action}")
    print(f"  Asset: {asset}")
    print(f"  Duration: {duration}")
    print(f"  Amount: ${amount}")
    print(f"-----------------------")

@client.on(events.NewMessage(chats='YourGroupUsername'))
async def handler(event):
    message = event.message.message
    action, asset, duration = parse_signal(message)
    if action:
        execute_trade(action, asset, duration, amount=1)  # test amount

async def main():
    """Starts the Telegram client."""
    # You will be asked for your phone number, password, and a login code the first time.
    await client.start(phone)
    print("✅ Client started. Waiting for messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())