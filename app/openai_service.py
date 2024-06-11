import openai
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_ai_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()
