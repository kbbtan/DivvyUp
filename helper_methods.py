import textwrap
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatMember

from constants import ADD_EXPENSE, ADD_EXPENSE_PAYER, ADD_EXPENSE_PAYEE, ADD_EXPENSE_AMOUNT

def encode_callback_data(cat: str, subcat: str, data: str):
    """ This function encodes callback data which fits the pre-defined format for filtering
        i.e. cat|subcat|data

        :param str cat: category of command the callback query is for
        :param str subcat: subcategory of command the callback query is for, varies by command type
        :param int data: data returned in the callback query

        :rtype: str
        :return: string containing the formatted callback data
    """
    return f"{cat}|{subcat}|{data}"

def decode_callback_data(callback_data: str):
    """ This function decodes callback data and extracts the information from its three fields
        i.e. cat|subcat|data

        :param str callback_data: encoded callback data string

        :rtype: list
        :return: list containing decoded [cat, subcat, data]
    """
    return callback_data.split("|")

async def generate_users_inline_buttons(bot: Client, chat_id: int, subcat: str, payer: str = None) -> InlineKeyboardMarkup:
    """ This function obtains the members list of a chat and generates an InlineKeyboardMarkup
        containing InlineKeyboardButtons representing each member.
        
        :param pyrogram.Client bot: bot invokes methods for querying Telegram group information
        :param int chat_id: chat_id of the Telegram group to query
        :param subcat str: the current subcat of the /add_expense operation
        :param payer str: the payer of the transaction if they already exist

        :rtype: pyrogram.InlineKeyboardMarkup
        :return: InlineKeyboardMarkup object containing an InlineKeyboardButton for each user in the group
    """
    next_subcat = {
        ADD_EXPENSE_PAYER: ADD_EXPENSE_PAYEE,
        ADD_EXPENSE_PAYEE: ADD_EXPENSE_AMOUNT
    }

    # Add payer as part of the callback data if they already exist.
    if subcat == ADD_EXPENSE_PAYEE:
        prefix = f"{payer},"
    else:
        prefix = ""

    # Generate inline buttons.
    markup = []
    async for member in bot.get_chat_members(chat_id):
        username = member.user.username

        if subcat == ADD_EXPENSE_PAYEE:
            username += ","

        markup.append(
            [
                InlineKeyboardButton(
                    username,
                    callback_data=encode_callback_data(ADD_EXPENSE, next_subcat[subcat], f"{prefix}{username}")
                )
            ]
        )

    # Add a back button if we are entering the payee.
    if subcat == ADD_EXPENSE_PAYEE:
        markup.append(
            [
                InlineKeyboardButton(
                    "Back",
                    callback_data=encode_callback_data(ADD_EXPENSE, ADD_EXPENSE_PAYER, payer)
                )
            ]
        )

    return InlineKeyboardMarkup(markup)

async def generate_inline_buttons_add_expense_amount(bot: Client, chat_id: int, payer: str, payee: str, amount: str = "") -> InlineKeyboardMarkup:
    """ This function generates an InlineKeyboardMarkup for the ADD_EXPENSE_AMOUNT command.
        
        :param pyrogram.Client bot: bot invokes methods for querying Telegram group information
        :param int chat_id: chat_id of the Telegram group to query
        :param payer str: the current payer of the transaction
        :param payee str: the current payee of the transaction
        :param amount str: the amount entered so far for the transaction

        :rtype: pyrogram.InlineKeyboardMarkup
        :return: InlineKeyboardMarkup object containing an InlineKeyboardButton for each user in the group
    """
    # Define a static numpad keyboard.
    def callback_data(prefix: str, amount: str, key: str):
        """ This function generates callback data for the numerical keyboard in the ADD_EXPENSE_AMOUNT command.
        
            :param prefix str: the callback data so far containing payer and payee
            :param amount str: the amount entered so far for the transaction
            :param key str: the text of the key pressed

            :rtype: str
            :return: callback data for the inline keyboard button
        """
        if key == "Del":
            amount = amount[:-1]

        else:
            amount += key

        return f"{prefix}{amount}"

    callback_prefix = encode_callback_data(ADD_EXPENSE, ADD_EXPENSE_AMOUNT, f"{payer},{payee},")

    markup = [
        [InlineKeyboardButton("1", callback_data(callback_prefix, amount, "1")), InlineKeyboardButton("2", callback_data(callback_prefix, amount, "2")), InlineKeyboardButton("3", callback_data(callback_prefix, amount, "3"))],
        [InlineKeyboardButton("4", callback_data(callback_prefix, amount, "4")), InlineKeyboardButton("5", callback_data(callback_prefix, amount, "5")), InlineKeyboardButton("6", callback_data(callback_prefix, amount, "6"))],
        [InlineKeyboardButton("7", callback_data(callback_prefix, amount, "7")), InlineKeyboardButton("8", callback_data(callback_prefix, amount, "8")), InlineKeyboardButton("9", callback_data(callback_prefix, amount, "9"))],
        [InlineKeyboardButton(".", callback_data(callback_prefix, amount, ".")), InlineKeyboardButton("0", callback_data(callback_prefix, amount, "0")), InlineKeyboardButton("Del", callback_data(callback_prefix, amount, "Del"))],
        [InlineKeyboardButton("Back", encode_callback_data(ADD_EXPENSE, ADD_EXPENSE_PAYEE, payer)), InlineKeyboardButton("Submit", "f")]
    ]

    return InlineKeyboardMarkup(markup)

def generate_add_expense_message(subcat: str, payer: str = None, payee: str = None, amount: str = None) -> str:
    """ This function generates the message for the /add_expense command based on the
        current selected user(s) and payment amount.

        :param subcat str: the current subcat of the /add_expense operation (0 | 1 | 2)
        :param payer str: the username of the Telegram account paying for the expense
        :param payee str: the username of the Telegram account receiving the payment
        :param amount str: the amount being paid

        :rtype: str
        :return: string containing the message for the /add_expense command
    """
    prompts = {
        ADD_EXPENSE_PAYER: "Enter the payer:",
        ADD_EXPENSE_PAYEE: "Enter the payee:",
        ADD_EXPENSE_AMOUNT: "Enter the amount:"
    }

    message = f"""
        **Payer:**
        {payer}

        **Payee:**
        {payee}

        **Amount:**
        {amount}

        __{prompts[subcat]}__
    """
    return textwrap.dedent(message)