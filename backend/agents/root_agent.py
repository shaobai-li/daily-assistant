from openai import OpenAI
import os

class RootAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

    def generate_response(self, user_message):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": user_message}]
        )
        return response.choices[0].message.content
