from pyrogram import Client, filters
from helper_methods import generate_users_inline_buttons

bot = Client("my_bot")

@bot.on_message(filters.command("add_expense") & filters.group)
async def add_expense(client, message):
    """ This function handles calls to the /add_expense command.

        :param pyrogram.Client client: Client object representing the Telegram bot
        :param pyrogram.Message message: Message object representing the message received (/add_expense)

        :rtype: None
        :returns: None
    """
    markup = await generate_users_inline_buttons(bot, message.chat.id)

    await message.reply(
        text=message.text,
        reply_markup=markup
    )

# Automatically start() and idle()
print("Starting Bot")
bot.run()