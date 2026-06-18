from database.memory import cursor
from database.memory import conn

def reset_command(bot):

    @bot.message_handler(commands=["reset"])
    def reset(message):

        user_id = message.from_user.id

        cursor.execute(
            "DELETE FROM memory WHERE user_id=?",
            (user_id,)
        )

        conn.commit()

        bot.reply_to(
            message,
            "Your memory has been erased. How tragic."
        )