from openai import OpenAI
import os
import json
from datetime import datetime

from openai.types.responses import response_audio_delta_event

ROOT_SYS_PROMPT = """
用户会输入一段文字，几乎都是下达和todo-list相关的一个或多个指令，偶尔会有对你发起的普通聊天。你的职责是：判断用户的意图，并输出一个 JSON 指令列表。
输出格式必须严格符合以下规范（不要输出多余文字）：
```json
[
    {
        "id": "数字索引",
        "用户意图分析": {
            "用户的输入": "用户输入的原始文字",
            "用户意图": "往todo-list中写入"/"从todo-list中读取"/"普通聊天",
            "指令或提问": "指令/提问/其他",
            "待办事项具体与否": "是/否",
            "原因说明": "简短说明你是如何分析用户意图的"
        }
    },
    ...
]
```
"""

INFO_EXTRACTION_SYS_PROMPT = """
你是信息提取助手，负责从用户的自然语言输入中提取出事项的核心信息，并以 JSON 格式输出。
```json
[
  {
    "事项名称": "提取用户输入的事项中最核心的任务或动作",
    "备注": "用于补充附加信息，如时间、地点、人物、条件、原因等。如果输入中没有额外说明，可留空字符串。"
  }
]
```
"""
class RootAgent:
    def __init__(self):
        # self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.json_file = "todos.json"
        self.function_calls = {
            "write_todo": self.write_todo,
            "read_todo": self.read_todo
        }

    def process_request(self, user_content):
        root_messages = [{"role": "system", "content": ROOT_SYS_PROMPT}]
        root_messages.append({"role": "user", "content": user_content})
        response_message = self.get_generation(root_messages)

        content = None
        if response_message.tool_calls:
            root_messages.append({"role": "assistant", "content": response_message.content, "tool_calls": response_message.tool_calls})
            tool = response_message.tool_calls[0]
            content = self.function_calls[tool.function.name](user_content)
            root_messages.append({"role": "tool", "tool_call_id": tool.id, "content": content})
            response_message = self.get_generation(root_messages)

        ai_content = response_message.content
        root_messages.append({"role": "assistant", "content": ai_content})
        print(ai_content)
        return ai_content

    def get_generation(self, messages):
        response = self.client.chat.completions.create(
        # model="deepseek-chat",
        model="gpt-4o-mini",
        messages=messages
        )    
        return response.choices[0].message

    def write_todo(self, user_content):

        info_extraction_messages = [{"role": "system", "content": INFO_EXTRACTION_SYS_PROMPT}]
        info_extraction_messages.append({"role": "user", "content": user_content})
        response_message = self.get_generation(info_extraction_messages)
        info = response_message.content
    
        info_extraction_messages.append({"role": "assistant", "content": info})
        print(info)
        return info

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