from pyrogram import Client, filters

app = Client("my_bot")

@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)

# Automatically start() and idle()
print("Starting Bot")
app.run()