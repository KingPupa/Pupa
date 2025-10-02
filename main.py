from telethon import TelegramClient, events

# Configuration
# Replace with your own values
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'

# Create client
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats='YourGroupUsername'))
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