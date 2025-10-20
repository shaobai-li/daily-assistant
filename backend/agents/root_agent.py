from openai import OpenAI
import os
import json
import datetime

SYSTEM_PROMPT = """
You are a helpful assistant that can help me manage my inspiration library.
"""

class RootAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.json_file = "todos.json"

    def generate_response(self, user_content):
        self.messages.append({"role": "user", "content": user_content})
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages
        )
        ai_content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": ai_content})
        return ai_content

    def store_todo(self, user_content):
        # use the user_content to create a new todo item
        # save the todo item to json file

        dummy_todo = {
            "id": 37261,
            "title": "Read react tutorial",
            "description": "Read the react tutorial to learn the basics of react",
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(self.json_file, "a") as f:
            json.dump(dummy_todo, f, indent=4)

        