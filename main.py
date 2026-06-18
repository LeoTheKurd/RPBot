import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

import json

from config import BOT_TOKEN
from ai.generate import generate_response
from database.memory import save_memory
from database.memory import get_memory
from database.memory import get_long_memory
from database.memory import save_long_memory



bot = telebot.TeleBot(BOT_TOKEN)
active_character = {}

with open(
    "character_data.json",
    "r",
    encoding="utf-8"
) as f:

    CHARACTER_DATA = json.load(f)

character_prompts = {}

for character_id in CHARACTER_DATA:

    with open(
        f"characters/{character_id}.txt",
        "r",
        encoding="utf-8"
    ) as f:

        character_prompts[character_id] = f.read()


@bot.message_handler(commands=["start"])
def start(message):

    parts = message.text.split()

    if len(parts) > 1:

        character_id = parts[1].lower()

        if character_id in CHARACTER_DATA:

            active_character[
                message.from_user.id
            ] = character_id

            bot.reply_to(
                message,
                f"You are now chatting with {CHARACTER_DATA[character_id]['name']}."
            )

            return

    bot.reply_to(
        message,
        "Choose a character from Character Hub."
    )


@bot.message_handler(commands=["remember"])
def remember(message):

    user_id = message.from_user.id

    text = message.text.replace(
        "/remember",
        ""
    ).strip()

    if not text:

        bot.reply_to(
            message,
            "Tell me something to remember."
        )

        return

    save_long_memory(
        user_id,
        text
    )

    bot.reply_to(
        message,
        "I'll remember that."
    )


@bot.message_handler(commands=["memory"])
def memory_command(message):

    user_id = message.from_user.id

    memories = get_long_memory(user_id)

    if not memories:

        bot.reply_to(
            message,
            "I remember nothing about you."
        )

        return

    bot.reply_to(
        message,
        f"Things I remember:\n\n{memories}"
    )


@bot.message_handler(commands=["characters"])
def characters(message):

    text = "Available Characters:\n\n"

    for key, character in CHARACTER_DATA.items():

        text += (
            f"{character['name']}\n"
            f"{character['description']}\n\n"
        )

    bot.reply_to(
        message,
        text
    )

@bot.message_handler(commands=["characters"])
def characters(message):

    text = "Available Characters:\n\n"

    for key, character in CHARACTER_DATA.items():

        text += (
            f"{character['name']}\n"
            f"{character['description']}\n\n"
        )

    bot.reply_to(
        message,
        text
    )

@bot.message_handler(commands=["character"])
def character_menu(message):

    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(
            "Nevermore",
            callback_data="universe_nevermore"
        )
    )

    markup.row(
        InlineKeyboardButton(
            "GTA V",
            callback_data="universe_gtav"
        )
    )

    markup.row(
        InlineKeyboardButton(
            "RDR2",
            callback_data="universe_rdr2"
        )
    )

    bot.send_message(
        message.chat.id,
        "Choose a Universe",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    if call.data == "universe_nevermore":

        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(
                "Wednesday",
                callback_data="character_wednesday"
            ),
            InlineKeyboardButton(
                "Enid",
                callback_data="character_enid"
            )
        )

        markup.row(
            InlineKeyboardButton(
                "Tyler",
                callback_data="character_tyler"
            ),
            InlineKeyboardButton(
                "Xavier",
                callback_data="character_xavier"
            )
        )

        bot.edit_message_text(
            "Choose a Character",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data.startswith("character_"):

        character_id = call.data.replace(
            "character_",
            ""
        )

        active_character[
            call.from_user.id
        ] = character_id

        bot.edit_message_text(
            f"You are now chatting with {CHARACTER_DATA[character_id]['name']}.",
            call.message.chat.id,
            call.message.message_id
        )        

@bot.message_handler(content_types=["web_app_data"])
def handle_webapp_data(message):

    user_id = message.from_user.id

    data = json.loads(
        message.web_app_data.data
    )

    character_id = data.get(
        "character"
    )

    if character_id not in CHARACTER_DATA:

        bot.send_message(
            message.chat.id,
            "Invalid character."
        )

        return

    active_character[user_id] = (
        character_id
    )

    bot.send_message(
        message.chat.id,
        f"You are now chatting with {CHARACTER_DATA[character_id]['name']}."
    )

    
@bot.message_handler(func=lambda m: True)
def chat(message):

    print(message)

    user_id = message.from_user.id

    bot.send_chat_action(
        message.chat.id,
        "typing"
    )

    memory = get_memory(user_id)

    character_id = active_character.get(
        user_id,
        "wednesday"
    )

    response = generate_response(
        character_prompts[character_id],
        memory,
        message.text
    )

    save_memory(
        user_id,
        f"User: {message.text}"
    )

    save_memory(
        user_id,
        f"Wednesday: {response}"
    )

    bot.reply_to(
        message,
        response
    )


print("Bot Running")

bot.infinity_polling()