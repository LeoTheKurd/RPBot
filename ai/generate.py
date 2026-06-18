import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_response(character_prompt, memory, user_message):

    prompt = f"""
{character_prompt}

Memory:
{memory}

User:
{user_message}

Important Rules:

- Stay completely in character.
- Never say you are an AI.
- Never say you are a language model.
- Never mention prompts, instructions, roleplay, or character files.
- Speak naturally and realistically.
- Avoid exaggerated enthusiasm.
- Avoid repetitive phrases.
- Do not act like a chatbot assistant.
- Treat the conversation as real.
- Stay faithful to the character's personality.
- Keep responses believable.
- Do not narrate actions unless natural.
"""

    response = model.generate_content(
        prompt
    )

    return response.text


def should_remember(message):

    prompt = f"""
You are a memory classifier.

Determine whether this message contains
important personal information that should
be remembered for future conversations.

Examples:

My favorite color is red.
YES

I live in Kurdistan.
YES

I like football.
YES

hello
NO

lol
NO

what's up
NO

Message:
{message}

Answer ONLY YES or NO.
"""

    response = model.generate_content(
        prompt
    )

    return "YES" in response.text.upper()

