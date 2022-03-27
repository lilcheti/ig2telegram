import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
# Remember to use your own values from my.telegram.org!
api_id = 6101711
api_hash = 'c918ae5d4cca7e972deb51a81e60aa6b'

async def main():
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        print(client.session.save())

asyncio.run(main())