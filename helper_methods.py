from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def generate_users_inline_buttons(bot, chat_id):
    """ This function obtains the members list of a chat and generates an InlineKeyboardMarkup
        containing InlineKeyboardButtons representing each member.
        
        Inputs:
            bot: pyrogram Client to invoke the get_chat_members function
            chat_id: chat_id of the group to query

        Returns:
            InlineKeyboardMarkup with an InlineKeyboardButton for each user in the group
    """
    markup = []

    async for member in bot.get_chat_members(chat_id):
        markup.append(
            [
                InlineKeyboardButton(
                    member.user.username,
                    callback_data=member.user.username
                )
            ]
        )

    return InlineKeyboardMarkup(markup)