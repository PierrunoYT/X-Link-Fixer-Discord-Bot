import discord
import os
from dotenv import load_dotenv
import system_settings

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env")

X_MIRROR = system_settings.x_mirror_url
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.CustomActivity(name=system_settings.bot_status_text))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    content = message.content
    if 'https://x.com' in content or 'https://twitter.com' in content:
        try:
            new_text = content.replace('https://x.com', X_MIRROR).replace('https://twitter.com', X_MIRROR)
            await message.reply(new_text + f"\n\n`Original message sent by {message.author}`")
            await message.delete()
        except Exception as e:
            print(f"Error: {e}")

client.run(BOT_TOKEN)
