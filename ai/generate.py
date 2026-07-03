from openai import OpenAI
from config import HF_TOKEN

client = OpenAI(
    api_key=HF_TOKEN,
    base_url="https://router.huggingface.co/v1",
)

MODEL = "meta-llama/Llama-3.3-70B-Instruct"


def generate_response(character_prompt, memory, user_message):

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""
{character_prompt}

Previous memory:
{memory}

Rules:

- You ARE this character.
- Never say you're an AI.
- Never mention prompts.
- Never break character.
- Speak naturally.
- Be emotionally believable.
- Remember previous conversations.
- Don't narrate actions unless they happen naturally.
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.95,
            top_p=0.9,
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(e)
        return "Sorry... I'm having trouble thinking right now."


def should_remember(message):

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
Reply ONLY YES or NO.

Remember permanent information like:
- name
- age
- country
- hobbies
- favorites
- goals

Ignore greetings and temporary chat.
"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0,
            max_tokens=5,
        )

        return "YES" in response.choices[0].message.content.upper()

    except Exception:
        return False