from telethon import TelegramClient, events
import json

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

api_id = config["api_id"]
api_hash = config["api_hash"]
phone = config["phone"]

# Create client
client = TelegramClient("session_name", api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    print(f"[{event.date}] {sender.id} -> {event.raw_text}")

async def main():
    await client.start(phone)  # will ask for your login code first time
    print("✅ Telegram listener started... Waiting for messages.")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())