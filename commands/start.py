def start_command(bot):

    @bot.message_handler(commands=["start"])
    def start(message):

        bot.reply_to(
            message,
            """
🖤 Wednesday Addams

Commands:

/character
/reset
/help

You may speak.
"""
        )