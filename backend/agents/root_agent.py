from openai import OpenAI
import os
import json
from datetime import datetime

SYSTEM_PROMPT = """
你是一名智能的任务管理助手，负责帮助用户管理他们的待办事项（ToDo List）。

你的主要职责包括：
1. 理解用户的需求，帮助他们添加、查看、编辑或读取待办事项。
2. 当用户要求你保存或读取待办事项时，调用相应的函数工具：
   - 使用 `write_todo` 来将新的待办事项写入 JSON 文件。
   - 使用 `read_todo` 来从 JSON 文件中读取指定的待办事项。
3. 在回答用户问题时，保持简洁、礼貌、清晰。
4. 如果用户请求的操作无法直接完成（例如读取不存在的任务），请给出合理的提示或建议。
5. 除非必要，不要解释系统或工具的内部实现。

你应该始终以“帮助用户高效管理待办事项”为目标。
"""


tools = [
    {
        "type": "function",
        "function": {
            "name": "write_todo",
            "description": "Write a new todo item to the json file",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the todo item"},
                    "description": {"type": "string", "description": "The description of the todo item"},                    
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_todo",
            "description": "Read a todo item from the json file",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the todo item"},
                    "description": {"type": "string", "description": "The description of the todo item"},    
                }
            }
        }
    }
]

class RootAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.json_file = "todos.json"
        self.tools = tools

    def process_request(self, user_content):
        self.messages.append({"role": "user", "content": user_content})
        message = self.get_generation(self.messages)
                
        content = None
        if message.tool_calls:
            self.messages.append(message)
            tool = message.tool_calls[0]
            content = tool.function.arguments
            self.messages.append({"role": "tool", "tool_call_id": tool.id, "content": content})
            print({"role": "tool", "tool_call_id": tool.id, "content": content})
            message = self.get_generation(self.messages)

        ai_content = message.content
        self.messages.append({"role": "assistant", "content": ai_content})
        return ai_content

    def get_generation(self, context):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=context,
            tools=self.tools
        )
        return response.choices[0].message

    def write_todo(self, user_content):
        return "Todo stored successfully"

    def read_todo(self, user_content):
        return "Todo read successfully"

    
    # def store_todo(self, user_content):
    #     # use the user_content to create a new todo item
    #     # save the todo item to json file

    #     new_dummy_todo = {
    #         "id": 37261,
    #         "title": "Read react tutorial",
    #         "description": "Read the react tutorial to learn the basics of react",
    #         "completed": False,
    #         "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     }
        
    #     todos = []
    #     if os.path.exists(self.json_file):
    #         with open(self.json_file, "r") as f:
    #             try:
    #                 todos = json.load(f)
    #             except json.JSONDecodeError:
    #                 todos = []

    #     todos.append(new_dummy_todo)

    #     with open(self.json_file, "w") as f:
    #         json.dump(todos, f, indent=4, ensure_ascii=False)
    #     return "Todo stored successfully"