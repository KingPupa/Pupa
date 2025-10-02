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

@client.on(events.NewMessage(chats=group_username))
async def handler(event):
    """Listens for new messages in a specific chat and prints them."""
    message = event.message.message
    print("New Signal:", message)

async def main():
    """Starts the Telegram client."""
    # You will be asked for your phone number, password, and a login code the first time.
    await client.start(phone)
    print("✅ Client started. Waiting for messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())