import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_ai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
