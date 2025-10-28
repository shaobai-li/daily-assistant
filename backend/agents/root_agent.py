from openai import OpenAI
import os
import json
from datetime import datetime

SYSTEM_PROMPT = """
你是一名智能的待办事项管理助手，负责帮助用户高效管理他们的 ToDo List。

你的主要职责包括：
1. 理解用户意图，判断用户是想【写入新的待办事项】还是【读取现有的待办事项】。
   - 如果用户的意图是“添加”、“记录”、“保存”、“更新”、“写入”待办事项，请调用 `write_todo`。
   - 如果用户的意图是“查看”、“读取”、“查询”、“查找”、“显示”待办事项，请调用 `read_todo`。
2. 当用户请求保存或读取任务时，调用相应的函数工具完成操作。
3. 回答应保持简洁、礼貌、清晰。
4. 如果用户请求的任务不存在或无法执行，请给出合理提示或建议。
5. 除非必要，不要解释系统或工具实现细节。

你始终以“帮助用户高效管理待办事项”为目标。
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "write_todo",
            "description": "写入新的待办事项到 JSON 文件中（用于添加、更新或记录任务）。",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_todo",
            "description": "从 JSON 文件中读取待办事项（用于查看或查询任务）。",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
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
        self.function_calls = {
            "write_todo": self.write_todo,
            "read_todo": self.read_todo
        }

    def process_request(self, user_content):
        self.messages.append({"role": "user", "content": user_content})
        message = self.get_generation(self.messages)

        content = None
        if message.tool_calls:
            self.messages.append({"role": "assistant", "content": message.content, "tool_calls": message.tool_calls})
            tool = message.tool_calls[0]
            content = self.function_calls[tool.function.name](tool.function.arguments)
            print(type(tool.function.arguments))
            self.messages.append({"role": "tool", "tool_call_id": tool.id, "content": content})
            message = self.get_generation(self.messages)

        ai_content = message.content
        self.messages.append({"role": "assistant", "content": ai_content})
        print(self.messages)
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