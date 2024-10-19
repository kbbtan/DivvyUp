from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from constants import ADD_EXPENSE, ADD_EXPENSE_PAYER, ADD_EXPENSE_PAYEE, ADD_EXPENSE_AMOUNT
from constants import DEFAULT_ERROR_MESSAGE
from helper_methods import generate_users_inline_buttons, generate_inline_buttons_add_expense_amount, generate_add_expense_message, decode_callback_data

bot = Client("my_bot")

# /add_expense command
@bot.on_message(filters.command("add_expense") & filters.group)
async def add_expense(client: Client, message: Message) -> None:
    """ This function handles calls to the /add_expense command.

        :param pyrogram.Client client: Client object representing the Telegram bot
        :param pyrogram.Message message: Message object representing the message received (/add_expense)

        :rtype: None
        :returns: None
    """
    markup = await generate_users_inline_buttons(bot, message.chat.id, ADD_EXPENSE_PAYER)

    await message.reply(
        text=generate_add_expense_message(ADD_EXPENSE_PAYER),
        reply_markup=markup
    )

# /add_expense callback handlers
@bot.on_callback_query(filters.regex(f"{ADD_EXPENSE}\|\d*\|.*"))
async def add_expense_callbacks(client: Client, callback_query: CallbackQuery):
    cat, subcat, data = decode_callback_data(callback_query.data)
    origin_message = callback_query.message

    # User is entering payer.
    if subcat == ADD_EXPENSE_PAYER:
        markup = await generate_users_inline_buttons(bot, origin_message.chat.id, ADD_EXPENSE_PAYER)

        await origin_message.edit_text(
            text=generate_add_expense_message(ADD_EXPENSE_PAYER),
            reply_markup=markup
        )

    # User is entering payee.
    elif subcat == ADD_EXPENSE_PAYEE:
        payer = data
        markup = await generate_users_inline_buttons(bot, origin_message.chat.id, ADD_EXPENSE_PAYEE, payer)

        await origin_message.edit_text(
            text=generate_add_expense_message(ADD_EXPENSE_PAYEE, payer),
            reply_markup=markup
        )

    # User is entering amount.
    elif subcat == ADD_EXPENSE_AMOUNT:
        payer, payee, amount = data.split(",")
        markup = await generate_inline_buttons_add_expense_amount(bot, origin_message.chat.id, payer, payee, amount)

        await origin_message.edit_text(
            text=generate_add_expense_message(ADD_EXPENSE_AMOUNT, payer, payee, amount),
            reply_markup=markup
        )

    else:
        await callback_query.answer(
            DEFAULT_ERROR_MESSAGE,
            show_alert=True
        )
    

# Automatically start() and idle()
print("Starting Bot")
bot.run()