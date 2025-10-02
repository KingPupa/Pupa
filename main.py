import json
from telethon import TelegramClient, events

# Load configuration from config.json
try:
    with open('config.json') as config_file:
        config = json.load(config_file)
    api_id = config['api_id']
    api_hash = config['api_hash']
    phone = config['phone']
    group_username = config['group_username']
except FileNotFoundError:
    print("Error: config.json not found. Please create it from config.example.json.")
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

@client.on(events.NewMessage(chats=group_username))
async def handler(event):
    """Listens for new messages, parses them, and prints the structured data."""
    message_text = event.message.message
    action, asset, duration = parse_signal(message_text)

    if action:
        print(f"New Signal Received:")
        print(f"  Action: {action}")
        print(f"  Asset: {asset}")
        print(f"  Duration: {duration}")
    else:
        print(f"Received a message that could not be parsed: {message_text}")

async def main():
    """Starts the Telegram client."""
    # You will be asked for your phone number, password, and a login code the first time.
    await client.start(phone)
    print("✅ Client started. Waiting for messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())