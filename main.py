from pyrogram import Client, filters

bot = Client("my_bot")

@bot.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)

# Automatically start() and idle()
print("Starting Bot")
bot.run()