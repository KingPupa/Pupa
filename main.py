from telethon import TelegramClient, events

# Configuration
api_id = 26243332
api_hash = "2d0ec7dc609caca15b573fc2d5239424"
phone = "+254701022662"

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