from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN"),
)

response = client.chat_completion(
    model="Qwen3.6-27B",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence."
        }
    ],
)

print(response)