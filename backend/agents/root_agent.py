from openai import OpenAI
import os

SYSTEM_PROMPT = """
You are a helpful assistant that can help me manage my inspiration library.
"""

class RootAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def generate_response(self, user_content):
        self.messages.append({"role": "user", "content": user_content})
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages
        )
        ai_content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": ai_content})
        return ai_content