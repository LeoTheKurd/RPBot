active_character = {}

def character_command(bot):

    @bot.message_handler(commands=["character"])
    def character(message):

        bot.reply_to(
            message,
            """
Available Characters:

Wednesday
Enid
Tyler

Usage:

/character Wednesday
"""
        )