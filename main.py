import json
from telethon import TelegramClient, events
from datetime import datetime

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

api_id = config['api_id']
api_hash = config['api_hash']
phone = config['phone']

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage)
async def my_event_handler(event):
    """Handles new messages and prints them."""
    sender = await event.get_sender()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Safely get sender's username, first_name, or "Unknown"
    sender_name = "Unknown"
    if sender:
        sender_name = getattr(sender, 'username', None) or getattr(sender, 'first_name', "Unknown")

    print(f"{timestamp} - {sender_name}: {event.text}")

async def main():
    """Main function to start the client."""
    # Start the client with the provided phone number
    await client.start(phone)
    print("Client Created...")
    # Run the client until disconnected
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())